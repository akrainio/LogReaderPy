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

def set_params(log, start, end):
    if start is None:
        if end is None:
            return ["-o", "TestOut", log]
        else:
            return ["-e", "2000-10-10 00:00:00." + end + " -0000", "-o", "TestOut", log]
    elif end is None:
        return ["-s", "2000-10-10 00:00:00." + start + " -0000", "-o", "TestOut", log]
    else:
        return ["-s", "2000-10-10 00:00:00." + start + " -0000", "-e", "2000-10-10 00:00:00." + end + " -0000", "-o",
                "TestOut", log]


def assert_lines(test, lines, exp_log, act_log):
    exp_log = open(exp_log, "r")
    act_log = open(act_log, "r")
    i = 0
    while i < lines[1]:
        expected = exp_log.readline()
        if lines[0] <= i + 1 <= lines[1]:
            test.assertEquals(expected, act_log.readline())
        i += 1
    exp_log.close()
    act_log.close()


simple_log = "./TestLogs/SimpleLog"
simple_log_top = "./TestLogs/SimpleLog_TopHeavy"
which_log = simple_log_top


class TestStringMethods(unittest.TestCase):
    def test_empty(self):
        params = set

    def test_from_start(self):
        params = set_params(which_log, "001", None)
        main(params)
        assert_lines(self, [1, 5], which_log, "TestOut")

    def test_before_start(self):
        params = set_params(which_log, "000", None)
        main(params)
        assert_lines(self, [1, 5], which_log, "TestOut")


    def test_between_empty(self):
        params = set_params(which_log, "003", "019")
        main(params)
        assert_lines(self, [1, 1], "./TestLogs/EmptyLog", "TestOut")

