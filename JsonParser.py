__author__ = 'gzs3058'
#encoding=utf-8

def dict_decoder(s):
    """ 对表示object类型的json字符串进行递归解析 """
    dic = {}
    s = s.replace('\n', '').strip()
    if not s.endswith('}'):
        raise SyntaxError('Object Syntax Error')
    number1 = 0
    number2 = 0
    number3 = 0
    start = 0
    for i, j in enumerate(s[:]):
        if j == '{' and number3 % 2 == 0:
            number1 += 1
        elif j == '['and number3 % 2 == 0:
            number2 += 1
        elif j == '"' and qout_is_valid(s, i):
            number3 += 1
        elif j == '}' and number3 % 2 == 0 and i != len(s) - 1:
            number1 -= 1
        elif j == ']' and number3 % 2 == 0:
            number2 -= 1
        # 找出分隔字典中的项的逗号的位置
        elif (j == ',' and number1 % 2 == 1 and number2 == 0 and number3 % 2 == 0) or i == len(s) - 1:
            # 找出相邻两个合符规范的双引号，即找出字典的key
            qout1 = s[start:i].find('"')
            if qout1 == -1 and i == len(s) - 1:         # 判断是否为空字典
                if dic == {}:
                    return dic
                else:
                    raise SyntaxError('Extra Comma')
            qout1 += start
            qout2 = qout1 + 1 + s[qout1+1:i].index('"')
            while not qout_is_valid(s, qout2):          # 判断是否有效的双引号
                qout2 = qout2 + 1 + s[qout2+1:i].index('"')

            colon = qout2 + s[qout2:i].index(':')
            if colon > qout2+1:
                assert s[qout2+1:colon].isspace()
            k = colon + 1
            while s[k] == ' ':
                k += 1

            # 根据value的类型进行对应解析
            s1 = str_process(s[qout1+1:qout2])
            if s[k] == '{':
                dic[s1] = dict_decoder(s[k:i])
            elif s[k] == '[':
                dic[s1] = list_decoder(s[k:i])
            elif s[k] == '"':
                dic[s1] = str_decoder(s[k:i])
            elif s[k].isdigit() or s[k] == '-':
                dic[s1] = number_decoder(s[k:i])
            elif s[k:i].strip() == 'true':
                dic[s1] = True
            elif s[k:i].strip() == 'false':
                dic[s1] = False
            elif s[k:i].strip() == 'null':
                dic[s1] = None
            else:
                raise SyntaxError('Object Syntax Error')
            start = i+1
    return dic


def list_decoder(s):
    """ 对表示array类型的json字符串进行递归解析 """
    lis = []
    s = s.strip()
    if not s.endswith(']'):
        raise SyntaxError('Array Syntax Error')
    number1 = 0
    number2 = 0
    number3 = 0
    start = 0
    check_first_comma = False      # 标记是否检查了第一个逗号
    for i, j in enumerate(s):
        if j == '{' and number3 % 2 == 0:
            number1 += 1
        elif j == '[':
            number2 += 1 and number3 % 2 == 0
        elif j == '"' and qout_is_valid(s, i):
            number3 += 1
        elif j == '}' and number3 % 2 == 0 and i != len(s) - 1:
            number1 -= 1
        elif j == ']' and number3 % 2 == 0 and i != len(s) - 1:
            number2 -= 1
        # 找出分隔列表中的项的逗号的位置
        elif (j == ',' and number1 % 2 == 0 and number2 == 1 and number3 % 2 == 0) or i == len(s) - 1:
            k = start + 1
            if not check_first_comma and j == ',':     # 检查第一个逗号前是否有元素
                if s[k:i].strip() == "":
                    raise SyntaxError('Array Syntax Error')
                else:
                    check_first_comma = True
            while s[k] == ' ':
                k += 1
            # 根据item类型进行对应解释
            if s[k] == '{':
                lis.append(dict_decoder(s[k:i]))
            elif s[k] == '[':
                lis.append((list_decoder(s[k:i])))
            elif s[k] == '"':
                lis.append((str_decoder(s[k:i])))
            elif s[k].isdigit() or s[k] == '-':
                lis.append(number_decoder(s[k:i]))
            elif s[k:k+4] == 'true':
                lis.append(True)
            elif s[k:k+5] == 'false':
                lis.append(False)
            elif s[k:k+4] == 'null':
                lis.append(None)
            elif k == i and lis == []:
                pass
            else:
                raise SyntaxError("Array Syntax Error")
            start = i
    return lis


def str_decoder(s):
    s = s.strip()
    if not s.endswith('"'):
        raise SyntaxError('String missing "')
    return str_process(s[1:s.rindex('"')])


def number_decoder(s):
    """ 对表示number类型的json字符串进行解析 """
    if s.startswith('-') and len(s) > 2 and s[1:].startswith('0') and s[2].isdigit() or\
        s.startswith('0') and len(s) > 1 and s[1].isdigit():
        raise SyntaxError('Numbers cannot have leading zeroes')
    number_of_radix_point = s.count('.')
    number_of_e = s.count('E') + s.count('e')
    if number_of_radix_point == 0 and number_of_e == 0:      # 表示整数
        try:
            num = int(s)
        except ValueError:
            raise ValueError('Not a number')
        else:
            return num
    elif number_of_radix_point == 1 or number_of_e == 1:     # 表示浮点数
        try:
            num = float(s)
            if num == float('inf'):
                raise FloatingPointError('Out of float limit')
        except ValueError:
            raise ValueError('Not a number')
        else:
            return num
    else:
        raise ValueError('Not a number')


def unicode_parser(s):
    """ 检查是否一个有效的unicode编码 """
    for i in range(2, len(s)):
        if '9' >= s[i] >= '0' or 'F' >= s[i] >= 'A' or 'f' >= s[i] >= 'a':
            pass
        else:
            raise SyntaxError("Wrong unicode expression")
    return s.decode('unicode_escape')


def qout_is_valid(s, i):
    """ 判断双引号是否有效 """
    valid = True
    assert i >= 0
    num = 0
    while i > 0 and s[i - 1] == '\\':
        num += 1
        i -= 1
    if num % 2 == 1:
        valid = False
    return valid


def control_character_check(s):
    """ 检查字符串中是否含有控制字符 """
    for control_character in control_character_list:
        if control_character in s.decode('utf-8'):
            raise SyntaxError('Invalid control character')


control_character_list = [
    u'\u0001', u'\u0002', u'\u0003', u'\u0004', u'\u0005', u'\u0006',
    u'\u0007', u'\u0008', u'\u0009', u'\u000A', u'\u000B', u'\u000C',
    u'\u000D', u'\u000E', u'\u000F', u'\u0010', u'\u0011', u'\u0012',
    u'\u0013', u'\u0014', u'\u0015', u'\u0016', u'\u0017', u'\u0018',
    u'\u0019', u'\u001A', u'\u001B', u'\u001C', u'\u001D', u'\u001E',
    u'\u001F'
]


escape_decode_table = {
    '\\"': '"', '\\\\': '\\', '\\/': '/', '\\u': '\u', '\\b': '\x08',
    '\\f': '\x0c', '\\n': '\n', '\\r': '\r', '\\t': '\t'
}

def str_process1(s):
    control_character_check(s)
    sc = s
    idx = sc.find('\\')
    qout = sc.find('"')
    if qout >= 0 and (idx > qout or idx == -1):
            raise SyntaxError("Unexpected qout")
    sc = s.decode('unicode_escape')
    try:
        s1 = str(sc).decode('utf-8')
    except UnicodeEncodeError:
        return sc
    else:
        return s1.decode()


def str_process(s):
    """ 处理转义字符 """
    control_character_check(s)
    sc = s
    idx = sc.find('\\')
    qout = sc.find('"')
    if qout >= 0 and (idx > qout or idx == -1):
            raise SyntaxError("Unexpected qout")
    offset = 0
    while idx >= 0:                    # 根据escape_decode_table进行键值替换
        idx += offset
        if idx + 2 <= len(s) and s[idx:idx+2] in escape_decode_table.keys():
            if s[idx:idx+2] == '\\u':
                s = s[:idx] + unicode_parser(s[idx:idx+6]) + s[idx + 6:]
            else:
                s = s[:idx] + escape_decode_table[s[idx:idx+2]] + s[idx + 2:]
        else:
            raise SyntaxError("Unexpected exsape")
        sc = s[idx+1:]
        offset = idx + 1
        idx = sc.find('\\')
        qout = sc.find('"')
        if qout >= 0 and (idx > qout or idx == -1):
            raise SyntaxError("Unexpected qout")
    try:
        s1 = s.decode('utf-8')       # 处理中文字符
    except UnicodeEncodeError:
        return s
    else:
        return s1


def dict_encoder(d):
    """ 把python字典转换成json字符串 """
    s = ''
    for item in d.items():
        if isinstance(item[1], str):
            item = (item[0], item[1].decode())
        assert type(item[1]) in encoder_table.keys()
        encoder = encoder_table[type(item[1])]              # 根据值的不同类型调用不同的转换器
        if item == d.items()[-1]:
            s = s + str_encoder(item[0]) + ': ' + encoder(item[1])
        else:
            s = s + str_encoder(item[0]) + ': ' + encoder(item[1]) + ', '
    return '{' + s + '}'


def list_encoder(l):
    """ 把python列表转换成json字符串 """
    str = ''
    for element in l:
        assert type(element) in encoder_table.keys()
        encoder = encoder_table[type(element)]            # 根据项的不同类型调用不同的转换器
        if element == l[-1]:
            str += encoder(element)
        else:
            str = str + encoder(element) + ', '
    return '[' + str + ']'


def str_encoder(s):
    """ 把python字符串转换成json字符串 """
    s1 = s.encode('unicode_escape')
    s1 = s1.replace('"', '\\"')
    s1 = s1.replace('\\x08', '\\b')
    s1 = s1.replace('\\x0c', '\\f')
    return '"' + s1 + '"'


def other_encoder(s):
    """ 其他类型的转换 """
    if s is True:
        return 'true'
    elif s is False:
        return 'false'
    elif s is None:
        return 'null'


def num_encoder(s):
    """ 把python数值转换成jsaon字符串 """
    return str(s)


encoder_table = {
    type({}): dict_encoder, type([]): list_encoder,
    type(''.decode()): str_encoder, type(1): num_encoder,
    type(1.0): num_encoder, type(True): other_encoder,
    type(False): other_encoder, type(None): other_encoder,
}


def list_copy(l):
    l_copy = []
    for item in l:
        if isinstance(item, list):
            l_copy.append(list_copy(item))
        elif isinstance(item, dict):
            l_copy.append(dict_copy(item))
        else:
            l_copy.append(item)
    return l_copy


def dict_copy(d):
    d_copy = {}
    for item in d.items():
        if isinstance(item[1], list):
            d_copy[item[0]] = list_copy(item[1])
        elif isinstance(item[1], dict):
            d_copy[item[0]] = dict_copy(item[1])
        else:
            d_copy[item[0]] = item[1]
    return d_copy



class JsonParser(object):
    def __init__(self):
        self.dict = {}

    def load(self, s):
        self.dict = dict_decoder(s)

    def dump(self):
        return dict_encoder(self.dict)

    def loadJson(self, f):
        try:
            with open(f, 'r') as fb:
                self.dict = dict_decoder(fb.read())
        except IOError:
            raise IOError("Can't open the file")

    def dumpJson(self, f):
        try:
            with open(f, 'w+') as fb:
                fb.write(dict_encoder(self.dict))
        except IOError:
            raise IOError("Can't write to the file")

    def loadDict(self, d):
        d_copy = dict_copy(d)
        #d_copy = d.copy()
        for key in d_copy.keys():
            if not (isinstance(key, unicode) or isinstance(key, str)):
                del d_copy[key]
        self.dict = d_copy

    def dumpDict(self):
        return self.dict.copy()


    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def update(self, d):
        self.dict.update(d)



JSON = r'''
    {
        "integer": "中文",
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


