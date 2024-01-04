import time
import wget
import random
import requests

import os
from os import walk
from os.path import join


def Get_StockNumber(): 

    Results = [] 

    try:
        with open('Stock Symbol.csv', encoding="utf-8-sig") as File: 
            
            F_Read = File.readlines()

            for Stock_List in F_Read: 
            
                S = Stock_List.replace("\u3000", ",")
                S = S.split(',')

                Results.append([S[0].strip(), str(S[1].strip()), str(S[2].strip())]) 

    except: 
        print('讀不到')

    return Results

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌


def Rename_XML(Path):

    Stock_List = Get_StockNumber()
    
    StockLen = len(Stock_List)

    for root, dirs, files in walk(Path):

        for file in files:

            FullPath = join(root, file) 
            
            FileName = join(file) 

            CR = '-cr-'
            IR = '-ir-'

            for i in range(StockLen):

                Number, Name, Group = Stock_List[i]

                Number_List = '-' + Number + '-'
    
                if Number_List in FileName:

                    if CR in FileName:

                        folder = Path + "CR\\"
                        if not os.path.isdir(folder):
                            os.makedirs(folder)

                        os.rename(FullPath, Path + "CR\\" + Number + ".xml")

                    elif IR in FileName:

                        folder = Path + "IR\\"
                        if not os.path.isdir(folder):
                            os.makedirs(folder)

                        os.rename(FullPath, Path + "IR\\" + Number + ".xml")

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌


def Download_CR_XML(Path, Season):

    try:

        Stock_List = Get_StockNumber()

        StockLen = len(Stock_List)

        for i in range(StockLen):

            Number, Name, Group = Stock_List[i]

            StockName = Number + ".xml"

            if StockName in os.listdir("C:\\Senior Project\\HTML\\" + Season + "\\CR\\"):

                URL = "https://mops.twse.com.tw/server-java/t164sb01?t203sb01Form=t203sb01Form&step=1&CO_ID=" + Number + "&SYEAR=" + Season[0:4] + "&SSEASON=" + Season[5:6] + "&REPORT_ID=C"
                
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

                folder = "C:\\Senior Project\\HTML\\" + Season + "\\"
                if not os.path.isdir(folder):
                    os.makedirs(folder)

                delay_choices = [3, 5, 10, 6, 7, 11]  
                delay = random.choice(delay_choices)  
                time.sleep(delay)  

                Web_URL = requests.get(URL, headers=headers)

                Web_Content = wget.download(Web_URL.url, folder + str(Number) + '.html')
    except:
        print(Number + "Fail")

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌


def Download_IR_XML(Path, Season):

    try:

        Stock_List = Get_StockNumber()

        StockLen = len(Stock_List)

        for i in range(StockLen):

            Number, Name, Group = Stock_List[i]

            StockName = Number + ".xml"

            if StockName in os.listdir("C:\\Senior Project\\HTML\\" + Season + "\\IR\\"):

                URL = "https://mops.twse.com.tw/server-java/t164sb01?t203sb01Form=t203sb01Form&step=1&CO_ID=" + Number + "&SYEAR=" + Season[0:4] + "&SSEASON=" + Season[5:6] + "&REPORT_ID=A"

                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

                folder = "C:\\Senior Project\\HTML\\" + Season + "\\"
                if not os.path.isdir(folder):
                    os.makedirs(folder)

                delay_choices = [3, 5, 10, 6, 7, 11]  
                delay = random.choice(delay_choices)  
                time.sleep(delay)  

                Web_URL = requests.get(URL, headers=headers)

                Web_Content = wget.download(Web_URL.url, folder + str(Number) + '.html')
    except:
        print(Number + "Fail")

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌