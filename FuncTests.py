__author__ = 'gzs3058'
#encoding=utf-8

import filecmp
import unittest
import json
from JsonParser import JsonParser
test_json_str = r'''
    {
        "Ch": "中文",
        "integer": 1234567890,
        "real": -9876.543210,
        "e": 0.123456789e-12,
        "E": 1.234567890E+34,
        "":  23456789012E66,
        "zero": 0,
        "one": 1,
        "space": " ",
        "quote": "\"",
        "backslash": "\\",
        "controls": "\b\f\n\r\t",
        "slash": "/ & \/",
        "alpha": "abcdefghijklmnopqrstuvwyz",
        "ALPHA": "ABCDEFGHIJKLMNOPQRSTUVWYZ",
        "digit": "0123456789",
        "0123456789": "digit",
        "special": "`1~!@#$%^&*()_+-={':[,]}|;.</>?",
        "hex": "\u0123\u4567\u89AB\uCDEF\uabcd\uef4A",
        "true": true,
        "false": false,
        "null": null,
        "array":[  ],
        "object":{  },
        "address": "50 St. James Street",
        "url": "http://www.JSON.org/",
        "comment": "// /* <!-- --",
        "# -- --> */": " ",
        " s p a c e d " :[1,2 , 3

,

4 , 5        ,          6           ,7        ],"compact":[1,2,3,4,5,6,7],
        "jsontext": "{\"object with 1 member\":[\"array with 1 element\"]}",
        "quotes": "&#34; \u0022 %22 0x22 034 &#x22;",
        "\/\\\"\uCAFE\uBABE\uAB98\uFCDE\ubcda\uef4A\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"
: "A key can be any string"
    }
'''


class TestCases(unittest.TestCase):
    def setUp(self):
        self.jp = JsonParser()

    def test_basic(self):
        a1 = JsonParser()
        a2 = JsonParser()
        a3 = JsonParser()

        a1.load(test_json_str)
        d1 = a1.dumpDict()

        a2.loadDict(d1)
        a2.dumpJson('jsonfile.txt')

        a3.loadJson('jsonfile.txt')
        d3 = a3.dumpDict()
        self.assertEqual(d1, d3)

    def test_load(self):
        self.jp.load(test_json_str)
        self.assertEqual(self.jp.dict, json.loads(test_json_str))

    def test_dump(self):
        self.assertEqual(self.jp.dump(), json.dumps(self.jp.dict))

    def test_loadJson(self):
        f = 'jsonfile.txt'
        self.jp.loadJson(f)
        with open(f, 'r+') as fb:
            self.assertEqual(self.jp.dict, json.load(fb))

    def test_dumpJson(self):
        f = 'jsonfile1.txt'
        f2 = 'jsonfile2.txt'
        self.jp.load(test_json_str)
        self.jp.dumpJson(f)
        with open(f2, 'w+') as fb:
            json.dump(self.jp.dict, fb)
        self.assertEqual(True, filecmp.cmp(f, f2))

    def test_loadDict(self):
        d1 = {'a': 1, 'b': ['c', 2, 3], 'd':  {'e': True}}
        d2 = {'a': 1, False: 2, 3: 'd'}
        self.jp.loadDict(d1)
        self.assertEqual(d1, self.jp.dict)
        self.assertFalse(d1 is self.jp.dict)
        self.jp.loadDict(d2)
        for key in self.jp.dict.keys():
            self.assertEqual(True, isinstance(key, str))

    def test_dumpDict(self):
        d = self.jp.dumpDict()
        self.assertEqual(d, self.jp.dict)
        self.assertFalse(d is self.jp.dict)

    def test_getitem(self):
        d = {'test': 'getitem'}
        self.jp.loadDict(d)
        self.assertEqual(d['test'], self.jp['test'])

    def test_setitem(self):
        self.jp['test'] = 'getitem'
        dic = self.jp.dumpDict()
        self.assertEqual(dic['test'], 'getitem')

    def test_update(self):
        d1 = {'a': 1, 'b': 2}
        d2 = {'b': 3, 'c': 4}
        self.jp.loadDict(d1)
        self.assertEqual(self.jp.update(d2), d1.update(d2))


if __name__ == '__main__':
    unittest.main()




