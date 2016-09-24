import sys, getopt
from time import strptime, mktime

format = "%Y-%m-%d %H:%M:%S %z"
cursor = 0
infile = open(sys.argv[1], "r")
outfile = open(sys.argv[2], "w")


def gettime(date):
    formatted = date[:19] + date[23:]
    millisec = float(date[19:23])
    time = mktime(strptime(formatted, format)) + millisec
    return time


testing = gettime(sys.argv[3])
startStamp = gettime(sys.argv[3])
endStamp = gettime(sys.argv[4])
infile.seek(0, 2)
insize = infile.tell()


def nexttime(offset):
    if offset == 0:
        return gettime(infile.read(29))
    offset = nextlineloc(offset)
    infile.seek(offset)
    date = infile.read(29)
    return gettime(date)


def nextlineloc(loc):
    while True:
        if loc == insize: return insize
        if loc >= insize or loc < 0:
            print("LogReader: nextlineloc: Location " + loc.__str__() + " is outside of file, largest "
                                                                        "possible location is " + insize.__str__())
            exit(2)
        infile.seek(loc)
        got = infile.read(1)
        loc += 1
        if got == "\n":
            infile.seek(loc)
            if (infile.read(1)) == "\n":
                loc += 1
            return loc


def thislineloc(loc):
    while True:
        if loc == 0: return loc
        if loc >= insize or loc < 0:
            print("LogReader: thislineloc: Location " + loc.__str__() + " is outside of file, largest "
                                                                        "possible location is " + insize.__str__())
            exit(2)
        loc -= 1
        infile.seek(loc)
        got = infile.read(1)
        if got == "\n":
            return loc + 1


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


if sys.argv.__len__() != 5:
    print("LogReader: Usage: inputFile, outputFile, startTimeStamp, endTimeStamp")
    sys.exit(2)
if startStamp > endStamp:
    tempStamp = endStamp
    endStamp = startStamp
    startStamp = tempStamp
startLoc = find(startStamp, True)
endLoc = nextlineloc(find(endStamp, False))
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
