import re
import datetime
import os

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

def replaceFirstAndLast(s, fromN, toN):
  res = s
  first = re.compile("first", re.IGNORECASE)
  res = first.sub(str(fromN), res)
  last = re.compile("last", re.IGNORECASE)
  res = last.sub(str(toN), res)
  return res

def replaceMonthNames(s):
  res = s
  for idx, month in enumerate(MONTHS):
    monthName = re.compile(month, re.IGNORECASE)
    res = monthName.sub(str(idx+1), res)
  return res

def replaceDaysNames(s):
  res = s
  for idx, day in enumerate(DAYS):
    dayName = re.compile(day, re.IGNORECASE)
    res = dayName.sub(str(idx), res)
  return res


def numbersList(s, rangeFrom, rangeTo):
  l = []
  s = replaceFirstAndLast(s, rangeFrom, rangeTo)
  if rangeTo == 12:
    s = replaceMonthNames(s)
  elif rangeTo == 6:
    s = replaceDaysNames(s)
  arr = s.split(',')
  for elem in arr:
    if elem == '*':
      l += list(range(rangeFrom, rangeTo+1))
    elif "-" in elem:
      [fromN, toN] = elem.split('-');
      l += list(range(int(fromN), int(toN)+1))
    else:
      l += [int(elem)]
  return l

def isToRun(dt, cronLine):
  line = cronLine
  arr = line.split()
  [minutes, hours, dayOfMonth, month, dayOfWeek] = arr[0:5]
  if (not '*' in dayOfMonth) or (not '*' in month):
    if ('*' in dayOfWeek):
      dayOfWeek = "8" # out of range
  
  if (not '*' in dayOfWeek):
    if ('*' in dayOfMonth) and ('*' in month):
      month = "13" # out of range
  
  minutesList = numbersList(minutes, 0, 59)
  hoursList = numbersList(hours, 0, 59)
  daysOfMonthList = numbersList(dayOfMonth, 1, 31)
  monthsList = numbersList(month, 1, 12)
  daysOfWeekList = numbersList(dayOfWeek, 0, 6)
  
  curMinute = dt.minute
  curHour = dt.hour
  curDay = dt.day
  curMonth = dt.month
  curWeekday = dt.isoweekday()
  
  if (
    curMinute in minutesList and
    curHour in hoursList and
    ((curDay in daysOfMonthList and curMonth in monthsList) or
    (curWeekday in daysOfWeekList))
  ):
    return True
  return False

def parseLine(line):
  if not line.startswith("#") and len(line) > 0:
    arr = line.split()
    command = " ".join(arr[5:])
    now = datetime.datetime.now()
    if isToRun(now, line):
      print (command)
      #os.system(command)

#
#file1 = open('crontab', 'r')
#Lines = file1.readlines()
#
#for line in Lines:
#  parseLine(line.strip())
#