#! /usr/bin/env python3
import sys
import time
import signal
import datetime
import requests
import math
print ("+++Importing core.py")
from safe_core import *
from settings import *
print ("+++Importing ZDaemon")
from ZDaemon import *
import api_poloniex
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from sys import argv

def banner(string):
    print("-"*72)
    print("|"+"{:^70s}".format(string)+"|")
    print("-"*72)

banner("starting zcashd")
zd = ZDaemon()
print("-"*72)


print(" Accuracy:",accuracy)
print("     Pair:",pair)

# Human time (GMT): Tuesday, August 1, 2017 12:00:00 AM # 1501545600
# startTime = 1501545600
print("StartTime:", startTime," - ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startTime)))

# [now] time
# endTime = int(time.time())
print("  endTime:", endTime," - ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(endTime)))

# period = 300 # 300, 900-15min, 1800 - 30min, 7200-2hr, 14400-4hr, and 86400-24hr
print("   Period:", period)

try:
    conn = api_poloniex.poloniex(api_key,api_secret)
    print("Polo API Connection Sucessful >> " + conn.APIKey)
except:
    print("Polo API Connection Failed >> ")
    pause()
    sys.exit(0)

def gethist(historicalData, pair, startTime, endTime):
    print('-'*72)
    print('>> GetHist')
    # historicalData = conn.api_query("returnChartData",{"currencyPair":pair,"start":startTime,"end":endTime,"period":period})
    price_hist = []
    for x in range(len(historicalData)):
        # print("Start>> ", x, historicalData[x]))
        # occur = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(historicalData[x]["date"]))) # convert UNIX Time to String
        # calendar ,time = occur.split(" ") # split date and time
        # year, month, day = calendar.split("-") # split date
        # print(year, month, day)
        # hour, minute, second = time.split(":") # spilt time
        # print(hour, minute, second)

        price_hist.append([ \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(historicalData[x]["date"])).split(" ")[0].split("-")[0],\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(historicalData[x]["date"])).split(" ")[0].split("-")[1],\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(historicalData[x]["date"])).split(" ")[0].split("-")[2],\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(historicalData[x]["date"])).split(" ")[1].split(":")[0],\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(historicalData[x]["date"])).split(" ")[1].split(":")[1],\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(historicalData[x]["date"])).split(" ")[1].split(":")[2],\
            # year,\
            # month,\
            # day,\
            # hour,\
            # minute,\
            # second,\
            # "{:11s}".format("Outgoing" if translist[x]["category"] == "send" else ("Transparent" if translist[x]["address"][0] == "t" else "Hidden")),\
            # '{:10s}'.format("Received" if translist[x]["category"] == "receive" else "Sent"),\
            # "{:11s}".format("Confirmed" if translist[x]["confirmations"] > 6 else "Unconfirmed"),\
            '{:8.2f}'.format(historicalData[x]["high"]),\
            '{:8.2f}'.format(historicalData[x]["low"]),\
            '{:8.2f}'.format(historicalData[x]["open"]),\
            '{:8.2f}'.format(historicalData[x]["close"]),\
            '{:19.6f}'.format(historicalData[x]["volume"]),\
            #'{:13d}'.format(test[x]["time"]),\
            # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(translist[x]["time"])),\
            # "{:35s}".format("Outgoing" if translist[x]["category"] == "send" else translist[x]["address"]),\
            # '{:64s}'.format(translist[x]["txid"])
            ])
        # print(price_hist[x])
    # print(len(price_hist))
    print("Historical entries obtained:", len(price_hist))
    print('-'*72)
    return price_hist

def year(inlist):
    print( ">> Year Average")

    labels = ['year','month','day','hour','minute','second','high','low','open','close', 'volume']

    vals = ['high','low','open','close', 'volume','average'] # Colums that will be averaged

    df = pd.DataFrame.from_records(inlist, columns=labels)
    df[['year','month','day','hour','minute','second']] = df[['year','month','day','hour','minute','second']].astype(int)
    df[['high','low','open','close', 'volume']] = df[['high','low','open','close', 'volume']].astype(float)
    df['average'] = df.high.add(df.low).div(2)

    # print(df.head())
    df = df.groupby(['year','month','day','hour','minute','second'])[vals].mean()\
        .groupby(['year','month','day','hour','minute',])[vals].mean()\
        .groupby(['year','month','day','hour',])[vals].mean()\
        .groupby(['year','month','day',])[vals].mean()\
        .groupby(['year','month',])[vals].mean()\
        .groupby(['year',])[vals].mean()

    # print(df.head())

    # print(df.head())

    # print(df.head().dtypes)
    # print(df[['high','low']])
    # print(df.values.tolist())
    # print(df.to_dict('index'))
    #
    df = df.reset_index()
    # df.rename(columns = {'index':'year'}, inplace = True)
    # df['year'] = df['year'].astype(int)


    # return df.to_dict('index')
    return df

def month(inlist):
    print( ">> Month Average")
    labels = ['year','month','day','hour','minute','second','high','low','open','close', 'volume']

    vals = ['high','low','open','close', 'volume','average'] # Colums that will be averaged

    df = pd.DataFrame.from_records(inlist, columns=labels)
    df[['year','month','day','hour','minute','second']] = df[['year','month','day','hour','minute','second']].astype(int)
    df[['high','low','open','close', 'volume']] = df[['high','low','open','close', 'volume']].astype(float)
    df['average'] = df.high.add(df.low).div(2)

    # print(df.head())
    df = df.groupby(['year','month','day','hour','minute','second'])[vals].mean()\
        .groupby(['year','month','day','hour','minute',])[vals].mean()\
        .groupby(['year','month','day','hour',])[vals].mean()\
        .groupby(['year','month','day',])[vals].mean()\
        .groupby(['year','month',])[vals].mean()\
        # .groupby(['year',])[vals].mean()

    # print(df.head())
    df = df.reset_index()
    # df.rename(columns = {'index':'year'}, inplace = True)

    # return df.to_dict('index')
    return df

def day(inlist):
    print( ">> Day Average")
    labels = ['year','month','day','hour','minute','second','high','low','open','close', 'volume']

    vals = ['high','low','open','close', 'volume','average'] # Colums that will be averaged

    df = pd.DataFrame.from_records(inlist, columns=labels)
    df[['year','month','day','hour','minute','second']] = df[['year','month','day','hour','minute','second']].astype(int)
    df[['high','low','open','close', 'volume']] = df[['high','low','open','close', 'volume']].astype(float)
    df['average'] = df.high.add(df.low).div(2)

    # print(df.head())
    df = df.groupby(['year','month','day','hour','minute','second'])[vals].mean()\
        .groupby(['year','month','day','hour','minute',])[vals].mean()\
        .groupby(['year','month','day','hour',])[vals].mean()\
        .groupby(['year','month','day',])[vals].mean()\
        # .groupby(['year','month',])[vals].mean()\
        # .groupby(['year',])[vals].mean()

    # print(df.head())
    df = df.reset_index()
    # return df.to_dict('index')
    return df

def hour(inlist):
    print( ">> Hour Average")
    labels = ['year','month','day','hour','minute','second','high','low','open','close', 'volume']

    vals = ['high','low','open','close', 'volume','average'] # Colums that will be averaged

    df = pd.DataFrame.from_records(inlist, columns=labels)
    df[['year','month','day','hour','minute','second']] = df[['year','month','day','hour','minute','second']].astype(int)
    df[['high','low','open','close', 'volume']] = df[['high','low','open','close', 'volume']].astype(float)
    df['average'] = df.high.add(df.low).div(2)

    # print(df.head())
    df = df.groupby(['year','month','day','hour','minute','second'])[vals].mean()\
        .groupby(['year','month','day','hour','minute',])[vals].mean()\
        .groupby(['year','month','day','hour',])[vals].mean()\
        # .groupby(['year','month','day',])[vals].mean()\
        # .groupby(['year','month',])[vals].mean()\
        # .groupby(['year',])[vals].mean()

    # print(df.head())

    # print(type(df))
    # df.to_cvs('out.cvs')
    df = df.reset_index()
    # return df.to_dict('index')
    return df

def minute(inlist):
    print( ">> Minute Average")
    labels = ['year','month','day','hour','minute','second','high','low','open','close', 'volume']

    vals = ['high','low','open','close', 'volume','average'] # Colums that will be averaged

    df = pd.DataFrame.from_records(inlist, columns=labels)
    df[['year','month','day','hour','minute','second']] = df[['year','month','day','hour','minute','second']].astype(int)
    df[['high','low','open','close', 'volume']] = df[['high','low','open','close', 'volume']].astype(float)
    df['average'] = df.high.add(df.low).div(2)

    # print(df.head())
    df = df.groupby(['year','month','day','hour','minute','second'])[vals].mean()\
        .groupby(['year','month','day','hour','minute',])[vals].mean()\
        # .groupby(['year','month','day','hour',])[vals].mean()\
        # .groupby(['year','month','day',])[vals].mean()\
        # .groupby(['year','month',])[vals].mean()\
        # .groupby(['year',])[vals].mean()

    # print(df.head())
    df = df.reset_index()
    # return df.to_dict('index')
    return df

def second(inlist):
    print( ">> Second Average")
    labels = ['year','month','day','hour','minute','second','high','low','open','close', 'volume']

    vals = ['high','low','open','close', 'volume','average'] # Colums that will be averaged

    df = pd.DataFrame.from_records(inlist, columns=labels)
    df[['year','month','day','hour','minute','second']] = df[['year','month','day','hour','minute','second']].astype(int)
    df[['high','low','open','close', 'volume']] = df[['high','low','open','close', 'volume']].astype(float)
    df['average'] = df.high.add(df.low).div(2)

    # print(df.head())
    df = df.groupby(['year','month','day','hour','minute','second'])[vals].mean()\
        # .groupby(['year','month','day','hour','minute',])[vals].mean()\
        # .groupby(['year','month','day','hour',])[vals].mean()\
        # .groupby(['year','month','day',])[vals].mean()\
        # .groupby(['year','month',])[vals].mean()\
        # .groupby(['year',])[vals].mean()

    # print(df.head())
    df = df.reset_index()
    # return df.to_dict('index')
    return df

def avg_finder(rate , inlist):
    # print("Avg HR Func", rate)
    switcher = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second
    }
    # Get the function from switcher dictionary
    func = switcher.get(rate, lambda: "nothing")
    # Execute the function
    return func(inlist)

def test_avg(price_hist):
    avg_year = avg_finder("year", price_hist)
    print(avg_year)
    # for key, value in avg_year.items():
    #     print(key, value)
    pause()

    avg_month = avg_finder("month", price_hist)
    print(avg_month)
    # for key, value in avg_month.items():
    #     print(key, value)
    pause()

    avg_day = avg_finder("day", price_hist)
    print(avg_day)
    # for key, value in avg_day.items():
    #     print(key, value)
    pause()

    avg_hour = avg_finder("hour", price_hist) # 300 = 4 samples/hour
    print(avg_hour)
    # for key, value in avg_hour.items():
    #     print(key, value)
    pause()

    avg_minute = avg_finder("minute", price_hist)
    print(avg_minute)
    # for key, value in avg_minute.items():
    #     print(key, value)
    pause()

    #Useless due to min window of about 300 period on polo api
    avg_second = avg_finder("second", price_hist)
    print(avg_second)
    # for key, value in avg_second.items():
    #     print(key, value)
    pause()

def gen_translist_new(span):
    print('-'*72+"\n>> Gen_Tanslist_New")
    translist = zd.listTransactions(200)
    df = pd.DataFrame.from_dict(translist)#, columns=labels)
    # print(df)

    df = df.drop(['account', 'blockhash', 'blockindex', 'blocktime', 'confirmations', 'fee', 'size', 'txid', 'vjoinsplit', 'vout', 'walletconflicts','timereceived'], axis = 'columns')
    # print(df)

    #convert dates to col
    translist = df.values.tolist()
    # print(translist)
    # print("lenght of list:", len(translist))

    table = []

    for translist_index in range(0,len(translist)):
        # print("start Trans Record - "+ str(translist_index) + " " +"-"*72)
        # print(translist[translist_index])
        # translist[translist_index]

        table.append([ \
            "{:d}".format(translist_index+1),\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(translist[translist_index][3])).split(" ")[0].split("-")[0],\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(translist[translist_index][3])).split(" ")[0].split("-")[1],\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(translist[translist_index][3])).split(" ")[0].split("-")[2],\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(translist[translist_index][3])).split(" ")[1].split(":")[0],\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(translist[translist_index][3])).split(" ")[1].split(":")[1],\
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(translist[translist_index][3])).split(" ")[1].split(":")[2],\
            '{:s}'.format("Received" if translist[translist_index][2] == "receive" else "Sent"),\
            '{:f}'.format(translist[translist_index][1]),\
            "{:s}".format("Outgoing" if translist[translist_index][2] == "send" else translist[translist_index][0]),\
            ])
        # print(table[translist_index])

    print("Trans Count: ", len(table))


    labels = ['transaction', 'year','month','day','hour','minute','second','recieved','ammount','address']
    df = pd.DataFrame.from_records(table, columns=labels)

    if span == "year":
        df = df.drop(['month','day','hour','minute','second',], axis = 'columns')
    elif span == "month":
        df = df.drop(['day','hour','minute','second',], axis = 'columns')
    elif span == "day":
        df = df.drop(['hour','minute','second',], axis = 'columns')
    elif span == "hour":
        df = df.drop(['minute','second',], axis = 'columns')
    elif span == "minute":
        df = df.drop(['second',], axis = 'columns')
    elif span == "second":
        df = df
    else:
        print("Wrong Span:")
        sys.exit(0)

    print('-'*72)
    return df

def combine(span,price_hist, df_translist):
    print('-'*72+"\n>> Combine")
    df_avghist = avg_finder(span, price_hist)
    # print(df_avghist.head())
    # print(df_translist.head())

    list_avghist = df_avghist.values.tolist()
    list_translist = df_translist.values.tolist()
    # json_dump(list_avghist)
    # json_dump(list_translist)

    if span == "year":
        for tran_index in range(len(list_translist)): # check Each Tran to align to mkt val
            # print(list_translist[tran_index])
            for mkt_index in range(len(list_avghist)):
                # print(list_translist[tran_index][1])
                # print(int(list_avghist[mkt_index][0]))
                # print(type(list_translist[tran_index][1]))
                # print(type(int(list_avghist[mkt_index][0])))
                # print("--")
                if int(list_translist[tran_index][1]) == int(list_avghist[mkt_index][0]):
                    # print("match found")
                    list_translist[tran_index] = sum([list_translist[tran_index], list_avghist[mkt_index][1:]],[])
        df_outlabels = ['transaction', 'year', 'recieved','ammount','address','high','low','open','close', 'volume','average','rev']

    elif span == "month":
        for tran_index in range(len(list_translist)): # check Each Tran to align to mkt val
            # print(list_translist[tran_index])
            for mkt_index in range(len(list_avghist)):
                # print(list_translist[tran_index][1])
                # print(int(list_avghist[mkt_index][0]))
                # print(list_avghist[mkt_index])
                # print(type(list_translist[tran_index][1]))
                # print(type(int(list_avghist[mkt_index][0])))
                # print("--")
                if (   int(list_translist[tran_index][1]) == int(list_avghist[mkt_index][0])   ) and (   int(list_translist[tran_index][2]) == int(list_avghist[mkt_index][1])   ):
                    # print("match found")
                    list_translist[tran_index] = sum([list_translist[tran_index], list_avghist[mkt_index][2:]],[])
        df_outlabels = ['transaction', 'year','month', 'recieved','ammount','address','high','low','open','close', 'volume','average','rev']

    elif span == "day":
        for tran_index in range(len(list_translist)): # check Each Tran to align to mkt val
            # print(list_translist[tran_index])
            for mkt_index in range(len(list_avghist)):
                # print(list_translist[tran_index][1])
                # print(int(list_avghist[mkt_index][0]))
                # print(list_avghist[mkt_index])
                # print(type(list_translist[tran_index][1]))
                # print(type(int(list_avghist[mkt_index][0])))
                # print("--")
                if (   int(list_translist[tran_index][1]) == int(list_avghist[mkt_index][0])   ) and (   int(list_translist[tran_index][2]) == int(list_avghist[mkt_index][1])   )and (   int(list_translist[tran_index][3]) == int(list_avghist[mkt_index][2])   ):
                    # print("match found")
                    list_translist[tran_index] = sum([list_translist[tran_index], list_avghist[mkt_index][3:]],[])
        df_outlabels = ['transaction', 'year','month','day', 'recieved','ammount','address','high','low','open','close', 'volume','average','rev']

    elif span == "hour":
        for tran_index in range(len(list_translist)): # check Each Tran to align to mkt val
            # print(list_translist[tran_index])
            for mkt_index in range(len(list_avghist)):
                # print(list_translist[tran_index][1])
                # print(int(list_avghist[mkt_index][0]))
                # print(list_avghist[mkt_index])
                # print(type(list_translist[tran_index][1]))
                # print(type(int(list_avghist[mkt_index][0])))
                # print("--")
                if (   int(list_translist[tran_index][1]) == int(list_avghist[mkt_index][0])   ) and (   int(list_translist[tran_index][2]) == int(list_avghist[mkt_index][1])   )and (   int(list_translist[tran_index][3]) == int(list_avghist[mkt_index][2])   )and (   int(list_translist[tran_index][4]) == int(list_avghist[mkt_index][3])   ):
                    # print("match found")
                    list_translist[tran_index] = sum([list_translist[tran_index], list_avghist[mkt_index][4:]],[])

        df_outlabels = ['transaction', 'year','month','day','hour', 'recieved','ammount','address','high','low','open','close', 'volume','average','rev']

    elif span == "minute":
        print('fail')
        # for tran_index in range(len(list_translist)): # check Each Tran to align to mkt val
        #     # print(list_translist[tran_index])
        #     for mkt_index in range(len(list_avghist)):
        #         # print(list_translist[tran_index][1])
        #         # print(int(list_avghist[mkt_index][0]))
        #         # print(list_avghist[mkt_index])
        #         # print(type(list_translist[tran_index][1]))
        #         # print(type(int(list_avghist[mkt_index][0])))
        #         if (   int(list_translist[tran_index][1]) == int(list_avghist[mkt_index][0])   ) and (   int(list_translist[tran_index][2]) == int(list_avghist[mkt_index][1])   )and (   int(list_translist[tran_index][3]) == int(list_avghist[mkt_index][2])   )and (   int(list_translist[tran_index][4]) == int(list_avghist[mkt_index][3])   )and (   int(list_translist[tran_index][5]) == int(list_avghist[mkt_index][4])   ):
        #         # print("--")
        #             # print("match found")
        #             list_translist[tran_index] = sum([list_translist[tran_index], list_avghist[mkt_index][4:]],[])
    elif span == "second":
        print('fail')
        # df = df

    # for tran_index in range(len(list_translist)): # check Each Tran to align to mkt val
    #     # print(list_translist[tran_index])
    #     for mkt_index in range(len(list_avghist)):
    #         # print(list_translist[tran_index][1])
    #         # print(int(list_avghist[mkt_index][0]))
    #         # print(type(list_translist[tran_index][1]))
    #         # print(type(int(list_avghist[mkt_index][0])))
    #         # print("--")
    #         if int(list_translist[tran_index][1]) == int(list_avghist[mkt_index][0]):
    #             # print("match found")
    #             list_translist[tran_index] = sum([list_translist[tran_index], list_avghist[mkt_index][1:]],[])


    # outlist = pd.merge(list_translist, list_avghist)
    outlist = list_translist

    #Calcs Revenue
    for x in range(len(outlist)):
        outlist[x].append((float(outlist[x][-8])*float(outlist[x][-1])))

    # print(outlist[0])

    print("Found entires after combine:", len(outlist))

    print('-'*72)
    return outlist, pd.DataFrame.from_records(outlist, columns=df_outlabels)

def add_date_col(span, df_final):
    if span == "year":
        print("year")
        df_final['day'] = '01'
        df_final['month'] = '01'
        df_final[['transaction','year','month']] = df_final[['transaction','year','month']].astype(int)
        df_final[['ammount']] = df_final[['ammount']].astype(float)
        df_final['date'] = pd.to_datetime(df_final[['year', 'month', 'day']])
    elif span == "month":
        df_final['day'] = '01'
        # df_final['month'] = '01'
        df_final[['transaction','year','month']] = df_final[['transaction','year','month']].astype(int)
        df_final[['ammount']] = df_final[['ammount']].astype(float)
        df_final['date'] = pd.to_datetime(df_final[['year', 'month', 'day']])
    elif span == "day":
        df_final[['transaction','year','month','day']] = df_final[['transaction','year','month','day']].astype(int)
        df_final[['ammount']] = df_final[['ammount']].astype(float)
        df_final['date'] = pd.to_datetime(df_final[['year', 'month', 'day']])
    elif span == "hour":
        print("test")
        df_final[['transaction','year','month','day','hour']] = df_final[['transaction','year','month','day','hour']].astype(int)
        df_final[['ammount']] = df_final[['ammount']].astype(float)
        df_final['date'] = pd.to_datetime(df_final[['year', 'month', 'day', 'hour']])
    elif span == "minute":
        df_final[['transaction','year','month','day','hour','minute']] = df_final[['transaction','year','month','day','hour','minute']].astype(int)
        df_final[['ammount']] = df_final[['ammount']].astype(float)
        df_final['date'] = pd.to_datetime(df_final[['year', 'month', 'day', 'hour', 'minute']])
    elif span == "second":
        df_final[['transaction','year','month','day','hour','minute','second']] = df_final[['transaction','year','month','day','hour','minute','second']].astype(int)
        df_final[['ammount']] = df_final[['ammount']].astype(float)
        df_final['date'] = pd.to_datetime(df_final[['year', 'month', 'day', 'hour', 'minute', 'second']])
    else:
        print("Wrong Span:")
        sys.exit(0)

    return df_final

def getopts(argv):
    opts = {
    }  # Empty dictionary to store key-value pairs.
    count = 0
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:] # Reduce the argument list by copying it starting from index 1.
    return opts

if __name__ == '__main__':
    from sys import argv
    myargs = getopts(argv)
    # print(myargs)
    if '-a' in myargs:  # Change Accuracy
        print("Input: [" + myargs['-a']+"] - Switch worked!!")
        accuracy = myargs['-a']
    if '-c' in myargs:  # Custom Pair
        print("Input: [" + myargs['-c']+"] - Switch worked!!")
        pair = myargs['-c']
    if '-p' in myargs:  # Custom Period ( Controlls how accurate the data is that is pulled from polo)
        print("Input: [" + myargs['-p']+"] - Switch worked!!")
        if ((myargs['-p'] == 300)or(myargs['-p'] == 900)or(myargs['-p'] == 1800)or(myargs['-p'] == 14400)or(myargs['-p'] == 86400)or(myargs['-p'] == 7200)):
            period = myargs['-p']
        else:
            period = period
    else:
        print("No option selected accuracy = 'hour'")
        # main()

    historicalData = conn.api_query("returnChartData",{"currencyPair":pair,"start":startTime,"end":endTime,"period":period})
    price_hist = gethist(historicalData, pair, startTime, endTime)
    # print(price_hist)
    df_translist = gen_translist_new(accuracy)
    final, df_final = combine(accuracy ,price_hist, df_translist)

    # test_avg(price_hist)
    # pause()

    print('-'*72+"\n>> Final list")
    # for tran_index in range(len(final)):
    for tran_index in range(0,5):
        print(final[tran_index])
    print('-'*72)


    bills = pd.Series([600,600,600,600,600,600,600,600,600,600,], index = pd.date_range('7/1/2017',periods=10))
    # ts.plot()


    # print('-'*72+"\n>> Final dataframe")
    # import matplotlib.pyplot as plt
    # df_final = add_date_col(accuracy, df_final)
    # # .concat(bills, axis=0)
    # # df_final.set_index('date')#$/
    #
    # # These are a few differetn view styles to print
    # # print(df_final.head())
    # # df_final[(df_final['address'] == z_address)].plot.line(x='date', y=['open','average','close','rev'])
    # # df_final[(df_final['address'] == z_address)].plot.area(x='date', y=['open','average','close','rev'], stacked=False)
    # df_final[(df_final['address'] == z_address)].plot.area(x='date', y=['rev'], stacked=False)
    # plt.show()
    # # print(df_final.head())
    # print('-'*72)

    print('-'*72+"\n>> Total Rev")
    print("Sample table: (Most Recent 5)\n", df_final[(df_final['address'] == z_address)].filter(items=['address','rev'])[-5:] )# .filter(items=['address','rev']).
    # print( df_final.filter(items=['address','rev']).info() )
    print("\nTotal Rev Earned: $ {:>12.2f}".format(sum(df_final[(df_final['address'] == z_address)]['rev'])))
    print('-'*72)

    # Print out to .txt file ( Has a slightly different layout)
    # print('-'*72+"\n>> export txt")
    # thefile = open('Tax_info.txt', 'w')
    #
    # for item in final:
    #     thefile.write("%s\n" % item)
    # print('-'*72)

    print('-'*72+"\n>> Export CVS")
    thefile = open('Tax_cvs.txt', 'w')
    for trans in final:
        line = ""
        # print(trans)
        for cell in range(len(trans)):
            line += str(trans[cell]).strip()+","
        thefile.write("%s\n" % line)
    print('-'*72)
    print(">> Finished Sucessfully ! ")
