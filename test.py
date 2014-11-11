__author__ = 'gzs3058'
# encoding=utf-8

from JsonParser import JsonParser

jsons = [
    ('{"a":123}', "a", 123),  # 数字
    ('{"a":"hello"}', "a", "hello"),  # 字符串
    ('{"a":"\\t\\t\\n"}', "a", "\t\t\n"),  #tab和换行
    ('{"a": 1e1}', "a", 10),  #数字
    ('{"a": "\\u6709\\u611f\\u800c\\u53d1\\u3002\\u3002"}', "a", u"\u6709\u611f\u800c\u53d1\u3002\u3002"),  #unicode
    ('{"a  ": 123}', "a  ", 123),  #空格和tab
    ('{ "a" : 123    	}', "a", 123),  #空格和tab
    ('{"a":[1,2,3]}', "a", [1, 2, 3]),  #数组
    ('{"a":[1,2,"aaa"]}', "a", [1, 2, "aaa"]),  #数组
    ('{"a": "a\\\\"}', "a", "a\\"),  #反斜杠
    ('{"d{": "}dd"}', "d{", "}dd"),  # {}
    ('{"d,": ",dd"}', "d,", ",dd"),  # ,
    ('{"d\\\"": "\\\"dd"}', "d\"", "\"dd"),  # "
    ('{"a": {"a": {"a": 123}}}', "a", {"a": {"a": 123}}),  #嵌套
    ('{"a": {"a": {"a": 123, "b": [1,2,3]}}}', "a", {"a": {"a": 123, "b": [1, 2, 3]}}),  #嵌套
    ("""
{ "ab{" : "}123" }
""", "ab{", "}123"),  #复杂类型
]

s = '{"a": {"a": {"a": 123, "b": [1,2,3]}}}'



import json
a = JsonParser()

a.load(s)

for item in jsons:
    json.dumps(item[0])
    print item[0]
    a.load(item[0])
    assert a.dict.keys()[0] == item[1]
    print "k", item,
    assert a.dict[item[1]] == item[2]
    print "v"
