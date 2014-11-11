# -*- coding: utf-8 -*-
__author__ = 'gzs3058'
import datetime
import time
import sys

if len(sys.argv) > 1:
    date = time.strptime(sys.argv[1], '%Y-%m-%d')
    today = datetime.datetime(*date[:3])
    yesterday = today - datetime.timedelta(days=1)

else:
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)



hourstable = [' 00', ' 01', ' 02', ' 03', ' 04',
              ' 05', ' 06', ' 07', ' 08', ' 09',
              ' 10', ' 11', ' 12', ' 13', ' 14',
              ' 15', ' 16', ' 17', ' 18', ' 19',
              ' 20', ' 21', ' 22', ' 23']

with open('score.log', 'r+') as f:
    records = f.readlines()
times = []
scoretoday = []
scoreyesterday = []
scored = {}
for record in records:      # 提取每行的日期与小时
    times.append(record[22:35])
print 'Score difference between '+str(today)[:10] + ' and ' + str(yesterday)[:10]
print 'hour---difference '
for hour in hourstable[:24]:
    try:
        lines = (times.index(str(yesterday)[:10] + hour), times.index(str(today)[:10] + hour))   # 相邻两天的每小时的第一分钟数据所在的位置
    except ValueError:
        print 'No match data afer '+str(int(hour)) + ':00'
        break
    else:
        scoretoday.append(int(records[lines[0]][72:75]) * 50)
        scoreyesterday.append(int(records[lines[1]][72:75]) * 50)
        scored[hour] =  scoretoday[int(hour)] - scoreyesterday[int(hour)]    # 找出在线差值
        print hour, '---', scored[hour]
if scoretoday != []:
    print '\n' + 'The highest score at ' + str(today)[:10] + ' is :', max(scoretoday)



