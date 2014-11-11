__author__ = 'gzs3049'
# coding=utf-8

import unittest
from JsonParser import JsonParser

JSONDOCS = [
    # http://json.org/JSON_checker/test/fail2.json
    '{"key":["Unclosed array"}',
    # http://json.org/JSON_checker/test/fail3.json
    '{unquoted_key: "keys must be quoted}',
    # http://json.org/JSON_checker/test/fail4.json
    '{"back":["extra comma",]}',
    # http://json.org/JSON_checker/test/fail5.json
    '{"back":["double extra comma",,]}',
    # http://json.org/JSON_checker/test/fail6.json
    '{"back":[   , "<-- missing value"]}',
    # http://json.org/JSON_checker/test/fail7.json
    '{"back":["Comma after the close"],}',
    # http://json.org/JSON_checker/test/fail8.json
    '{"back":["Extra close"]]}',
    # http://json.org/JSON_checker/test/fail9.json
    '{"Extra comma": true,}',
    # http://json.org/JSON_checker/test/fail10.json
    '{"Extra value after close": true} "misplaced quoted value"',
    # http://json.org/JSON_checker/test/fail11.json
    '{"Illegal expression": 1 + 2}',
    # http://json.org/JSON_checker/test/fail12.json
    '{"Illegal invocation": alert()}',
    # http://json.org/JSON_checker/test/fail13.json
    '{"Numbers cannot have leading zeroes": 013}',
    # http://json.org/JSON_checker/test/fail14.json
    '{"Numbers cannot be hex": 0x14}',
    # http://json.org/JSON_checker/test/fail15.json
    '{"back":["Illegal backslash escape: \\x15"]}',
    # http://json.org/JSON_checker/test/fail16.json
    '{"back":["Illegal backslash escape: \\\'"]}',
    # http://json.org/JSON_checker/test/fail17.json
    '{"back":["Illegal backslash escape: \\017"]}',
    # http://json.org/JSON_checker/test/fail19.json
    '{"Missing colon" null}',
    # http://json.org/JSON_checker/test/fail20.json
    '{"Double colon":: null}',
    # http://json.org/JSON_checker/test/fail21.json
    '{"Comma instead of colon", null}',
    # http://json.org/JSON_checker/test/fail22.json
    '{"back":["Colon instead of comma": false]}',
    # http://json.org/JSON_checker/test/fail23.json
    '{"back":["Bad value", truth]}',
    # http://json.org/JSON_checker/test/fail24.json
    "{\"back\":['single quote']}"
]


class FailTest(unittest.TestCase):
    def setUp(self):
        self.jp = JsonParser()

    def test_fail_example(self):
        for key, value in enumerate(JSONDOCS):
            try:
                self.jp.load(value)
            except Exception as err:
                print "Testcase {}: content raise exception: {}".format(key + 1, err.message)
                continue
            else:
                self.fail("ValueError has no been raise when try {}".format(value))
        print "FailTest has finished!"

if __name__ == '__main__':
    unittest.main()

