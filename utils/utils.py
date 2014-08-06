#-*- coding:utf-8 -*-
import datetime

days1 = [31,28,31,30,31,30,31,31,30,31,30,31]
days2 = [31,29,31,30,31,30,31,31,30,31,30,31]

def isLeapYear(year):
    return year % 400 == 0 or year % 4 == 0 and year % 100 != 0

def getDaysOfMonth(year, month):
    if isLeapYear(year):
        return days2[month-1]
    else:
        return days1[month-1]

def getDaysOfYear(year):
    if isLeapYear(year):
        return sum(days2)
    else:
        return sum(days1)

def getTimeDelta(year,month,day,hour,minute):
    today = datetime.datetime.today()
    delta = today - datetime.datetime(year,month,day,hour,minute)
    daysOflastYear = getDaysOfYear(today.year)
    daysOflastMonth = getDaysOfMonth(today.year,today.month)
    if delta.days > daysOflastYear:
        return "%d年前" % (delta.days / daysOflastYear)
    elif delta.days > daysOflastMonth:
        return "%d个月前" % (delta.days / daysOflastMonth)
    elif delta.days > 0:
        return "%d天前" % delta.days
    elif delta.days == 0:
        if delta.seconds > 3600:
            return "%d小时前" % (delta.seconds / 3600)
        elif delta.seconds > 60:
            return "%d分钟前" % (delta.seconds / 60)
    else:
        return "刚刚"
