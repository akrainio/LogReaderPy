import sys, getopt, re
from time import strptime, mktime

def main(params):
    def gettime(date):
        formatted = date[:19] + date[23:]
        millisec = float(date[19:23])
        time = mktime(strptime(formatted, format)) + millisec
        return time

    def get_line_info(where):
        offset = where
        while offset != 0:
            infile.seek(offset - 1)
            if infile.read(1) == '\n':
                break
            offset -= 1
        infile.seek(offset)
        date = infile.read(29)
        if re.match("^(19|20)\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d (-|\+)\d{4}", date) is not None:
            time = gettime(date)
        else:
            print("logreader: getline: '" + date + "' does not match date pattern")
            sys.exit(2)
        end_offset = where
        while end_offset < insize:
            infile.seek(end_offset)
            if infile.read(1) == '\n':
                break
            end_offset += 1
        return offset, end_offset + 1, time


    def find(time, is_start):
        min = 0
        max = insize
        mid = int((min + max) / 2)
        p_mid = None
        c_start, c_end, c_time = get_line_info(mid)
        while p_mid != mid:
            p_mid = mid
            if c_time > time:
                max = c_start
            elif c_time < time:
                min = c_end
            elif c_time == time:
                return c_start
            mid = int((min + max) / 2)
            c_start, c_end, c_time = get_line_info(mid)
        if is_start:
            return c_start
        else:
            if c_time < time:
                return c_end
            else:
                return c_start

    outfile = sys.__stdout__
    startstamp = None
    endstamp = None
    infile = None
    format = "%Y-%m-%d %H:%M:%S %z"

    try:
        opts, args = getopt.getopt(params, "ho:s:e:", ["help", "output=", "start=", "end="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    infilename = args[0]
    try:
        infile = open(infilename, "r")
    except IOError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            print("logreader: -o <outputfile> -s <starttimestamp> -e <endtimestamp>")
        elif o in ('-o', '--outputfile'):
            try:
                outfile = open(a, "w")
            except IOError as err:
                print("I/O error({0}): {1}".format(err.errno, err.strerror))
                sys.exit(2)
        elif o in ('-s', '--start'):
            startstamp = gettime(a)
        elif o in ('-e', '--end'):
            endstamp = gettime(a)
        else:
            print("logreader: Unhandled option '" + a + "'")

    infile.seek(0, 2)
    insize = infile.tell()
    if startstamp is None:
        startstamp = get_line_info(0)[2]
    if endstamp is not None:
        if startstamp > endstamp:
            tempStamp = endstamp
            endstamp = startstamp
            startstamp = tempStamp
        endLoc = find(endstamp, False)
    else:
        endLoc = insize
    startLoc = find(startstamp, True)
    infile.seek(startLoc)
    x = 0
    while x < endLoc - startLoc:
        x += 1
        got = infile.read(1)
        outfile.write(got)
    infile.seek(insize - 1)
    if infile.read(1) is not "\n":
        outfile.write("\n")
    infile.close()
    outfile.close()

if __name__ == '__main__':
    main(sys.argv[1:])