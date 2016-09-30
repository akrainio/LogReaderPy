import sys, getopt, re
from time import strptime, mktime

def main(params):
    def gettime(date):
        formatted = date[:19] + date[23:]
        millisec = float(date[19:23])
        time = mktime(strptime(formatted, format)) + millisec
        return time


    def nexttime(offset):
        # if offset == 0:
        #     return gettime(infile.read(29))
        while True:
            offset = nextlineloc(offset)
            infile.seek(offset)
            date = infile.read(29)
            if re.match("^(19|20)\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d (-|\+)\d{4}", date) is not None:
                return gettime(date)


    def nextlineloc(offset):
        while True:
            if offset == insize: return insize
            if offset >= insize or offset < 0:
                print("LogReader: nextlineloc: Location " + offset.__str__() + " is outside of file, largest "
                                                                               "possible location is " + insize.__str__())
                exit(2)
            infile.seek(offset)
            got = infile.read(1)
            offset += 1
            if got == "\n":
                infile.seek(offset)
                if (infile.read(1)) == "\n":
                    offset += 1
                return offset


    def thislineloc(offset):
        while True:
            if offset == 0: return offset
            if offset >= insize or offset < 0:
                print("LogReader: thislineloc: Location " + offset.__str__() + " is outside of file, largest "
                                                                               "possible location is " + insize.__str__())
                exit(2)
            offset -= 1
            infile.seek(offset)
            got = infile.read(1)
            if got == "\n":
                date = infile.read(29)
                if re.match("^(19|20)\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d (-|\+)\d{4}", date) is not None:
                    return offset + 1


    def find(time, isstart):
        prevtime = -1
        currtime = 0
        min = 0
        max = insize
        mid = int((min + max) / 2)
        while prevtime != currtime:
            prevtime = currtime
            currtime = nexttime(mid)
            if currtime > time:
                max = mid
                mid = int((min + max) / 2)
            elif currtime < time:
                min = mid
                mid = int((min + max) / 2)
            elif currtime == time:
                return nextlineloc(mid)
        if isstart:
            return nextlineloc(mid)
        else:
            return thislineloc(mid)

    outfile = sys.__stdout__
    startstamp = None
    endstamp = None
    infile = None
    format = "%Y-%m-%d %H:%M:%S %z"
    cursor = 0

    try:
        opts, args = getopt.getopt(params, "ho:s:e:", ["help", "output=", "start=", "end="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    infilename = args[0]
    try:
        infile = open(infilename, "r")
    except IOError as err:
        print("logreader: I/O error({0}): {1}: {2}".format(err.errno, err.strerror))
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
        startstamp = nexttime(0)
    if endstamp is None:
        endstamp = thislineloc(insize)
    if startstamp > endstamp:
        tempStamp = endstamp
        endstamp = startstamp
        startstamp = tempStamp
    startLoc = find(startstamp, True)
    endLoc = nextlineloc(find(endstamp, False))
    print(startLoc)
    print(endLoc)
    infile.seek(startLoc)
    x = 0
    while x < endLoc - startLoc:
        x += 1
        got = infile.read(1)
        if got == '\n':
            x += 1
        outfile.write(got)
    infile.close()
    outfile.close()

main(sys.argv[1:])