from email import header
import os
import csv
import sqlite3
from traceback import print_tb
import pandas as pd
from glob import glob
from collections import OrderedDict


def get_stocknumber():
    res = [] # 存放切割文字結果
    try:
        with open('stock_number.csv', encoding="utf-8") as f: # 開啟csv檔案
            slist = f.readlines() # 以行為單位讀取所有資料
            # print('讀入：',slist) # 列印讀取資料
            for lst in slist: # 走訪每一個股票組合
                s = lst.split(',') # 以逗點切割為陣列
                # s = lst.splitlines(',') # 以逗點切割為陣列
                res.append([s[0].strip(),str(s[1].strip()),str(s[2].strip())]) # .strip去除空白，存到res陣列
    except:
        print('讀不到')
    return res