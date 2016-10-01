# LogReaderPy
Tool that extracts fragment of a log file based on timestamps. Implements
binary search to efficiently process very large files.
## Usage
~~~
logreader.py [-o <outfile>] [-s <startstamp>] [-e <endstamp>] [-h] <infile>

    outfile: specifies output file, stdout by default
    startstamp: specifies start time, beginning of file by default
    endstamp: specifies end time, end of file by default
    infile: specifies log to be processed
~~~