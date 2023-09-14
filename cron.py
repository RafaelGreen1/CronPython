import re
import datetime
import os

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

def replaceMonthNames(s):
  res = s
  for idx, month in enumerate(MONTHS):
    monthName = re.compile(re.escape(month), re.IGNORECASE)
    res = monthName.sub(str(idx+1), res)
  return res

def replaceDaysNames(s):
  res = s
  for idx, day in enumerate(DAYS):
    dayName = re.compile(re.escape(day), re.IGNORECASE)
    res = dayName.sub(str(idx), res)
  return res


def numbersList(s, rangeFrom, rangeTo):
  l = []
  if rangeTo == 12:
    s = replaceMonthNames(s)
  elif rangeTo == 6:
    s = replaceDaysNames(s)
  arr = s.split(',')
  for elem in arr:
    if elem == '*':
      l += list(range(rangeFrom, rangeTo))
    elif "-" in elem:
      [fromN, toN] = elem.split('-');
      l += list(range(int(fromN), int(toN)+1))
    else:
      l += [int(elem)]
  return l

def parseLine(line):
  if not line.startswith("#") and len(line) > 0:
    arr = line.split()
    minutesList = numbersList(arr[0], 0, 59)
    hoursList = numbersList(arr[1], 0, 59)
    daysOfMonthList = numbersList(arr[2], 1, 31)
    monthsList = numbersList(arr[3], 1, 12)
    daysOfWeekList = numbersList(arr[4], 0, 6)
    command = " ".join(arr[5:])
    now = datetime.datetime.now()
    curMinute = now.minute
    curHour = now.hour
    curDay = now.day
    curMonth = now.month
    curWeekday = now.isoweekday()
    if (
      curMinute in minutesList and
      curHour in hoursList and
      ((curDay in daysOfMonthList and curMonth in monthsList) or
      (curWeekday in daysOfWeekList))
    ):
      print (command)
      #os.system(command)

file1 = open('crontab', 'r')
Lines = file1.readlines()

for line in Lines:
  parseLine(line.strip())
