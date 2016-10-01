import unittest
from logreader import main


# things to test:
# start stamp same as the earliest stamp in file
# start stamp before the earliest stamp in file
# start stamp between two existing stamps in file
# start stamp same as the last stamp as file
# start stamp and end stamp are after the last stamp in file
# start stamp is after the end stamp
# start stamp and end stamp are the same
# end stamp is the same as the last stamp in file
# end stamp is after the last stamp in file
# end stamp is between two existing stamps in file
# end stamp same as the last stamp as file
# file is empty
# line doesn't start with a valid pattern

class TestStringMethods(unittest.TestCase):
    def test_empty(self):
        params = ["-s", "0000-00-00 00:00:00.000 -0000", "-e", "0000-00-00 00:00:00.040 -0000", "SimpleLog"]
        print(params)
        main(params)
