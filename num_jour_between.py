# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:47:01 2020

@author: Adèle
"""


from datetime import datetime, date, timedelta


def num_jour_between(date1,date2):
    y1 = date1.year
    m1 = date1.month
    d1 = date1.day
    y2 = date2.year
    m2 = date2.month
    d2 = date2.day
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    date_str1 = "%s-%s-%s 00:00:00" %(y1,m1,d1)
    date_str2 = "%s-%s-%s 00:00:00" %(y2,m2,d2)
    to_dt = datetime.strptime(date_str2, DATETIME_FORMAT)
    from_dt = datetime.strptime(date_str1, DATETIME_FORMAT)
    timedelta = to_dt - from_dt
    diff_day = timedelta.days #+ float(timedelta.seconds) / 86400
    return int(diff_day+1)