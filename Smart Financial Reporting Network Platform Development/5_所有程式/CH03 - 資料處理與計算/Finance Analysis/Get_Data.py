import os
import csv
import sqlite3
import numpy as np
import pandas as pd
from glob import glob
from collections import OrderedDict


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


def Get_Data(path, season, number): 

    File_Path = path + number + ".html"

    Files = os.path.isfile(File_Path)

    if Files == True:           

        if int(season[0:4]) >= 2019:

            df = pd.read_html(path + number + ".html", flavor='bs4')
        
            for index in range(0, 3): 

                File_Num = str(index + 1)

                Folder = "C:\\Senior Project\\Finance\\" + season + "\\" + number + "\\"
            
                if not os.path.isdir(Folder):
                    os.makedirs(Folder)

                df[index].to_csv(Folder + "Finance_" + number + "-" + File_Num + ".csv", index = False, encoding='utf-8-sig')
            
            #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

            for index in range(0, 3): 

                File_Num = str(index + 1)

                df = pd.read_csv(Folder + "Finance_" + number + "-" + File_Num + ".csv", header=0, index_col=0, encoding='utf-8-sig')

                df = df.iloc[:, [0, 1]]

                df.to_csv(Folder + "Finance_" + number + "-" + File_Num + ".csv", index = False, encoding='utf-8-sig')
                
        else:

            df = pd.read_html(path + number + ".html", encoding='ANSI', flavor='bs4')

            for index in range(0, 3): 

                File_Num = str(index + 1)

                Folder = "C:\\Senior Project\\Finance\\" + season + "\\" + number + "\\"
            
                if not os.path.isdir(Folder):
                    os.makedirs(Folder)

                df[index].to_csv(Folder + "Finance_" + number + "-" + File_Num + ".csv", index = False, encoding='utf_8_sig')
                    
            #   ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

            for index in range(0, 3): 

                File_Num = str(index + 1)

                df = pd.read_csv(Folder + "Finance_" + number + "-" + File_Num + ".csv", header=0, encoding='utf_8_sig')
            
                df = df.iloc[:, [0, 1]]

                df.to_csv(Folder + "Finance_" + number + "-" + File_Num + ".csv", index = False, encoding='utf_8_sig')   
    # else:     
    #     pass

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌


def Combine_Data(Number, Name, Group):
   
    Folder = "C:\\Senior Project\\Finance\\"

    Files = os.listdir(Folder)

    for Num in range(0, len(Files)):
        
        File = ( os.listdir(Folder)[Num] )

        Path = Folder + File + "\\" + Number
      
        for index in range(1, 4):

            File_Num = str(index)

            df = pd.read_csv(Path + "\\Finance_" + Number + "-" + File_Num + ".csv", encoding= "utf_8_sig") 
            
            table = ["會計項目", File]
                    
            df = pd.DataFrame(df.values, columns = table)

            df = df.drop(df.index[0:2])
            
            df = df.T

            df = df.dropna(axis=1)

            df.to_csv(Path + "\\Finance_" + Number + "-" + File_Num + ".csv", header=0, encoding='utf-8-sig')
            
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        File_CSV = glob(Path + "\\Finance_" + Number + "-*.csv")

        File_List = [pd.read_csv(FCSV) for FCSV in File_CSV]

        Result = pd.merge(File_List[0], File_List[1], on="會計項目") 
        Result = pd.merge(Result, File_List[2], on="會計項目") 

        Result.to_csv(Path + "\\Finance_" + Number + ".csv", index=0, encoding='utf-8-sig')

        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        Files = glob(Path + "\\Finance_" + Number + ".csv")

        TableList = ["會計項目", 
                     "權益", "權益 Equity", "權益總計", "權益總計 Equity",  "權益總計 Total equity", "權益總計 Total stockholders' equity", "權益總額", "權益總額 Total equity", 
                     "基本每股盈餘合計", "基本每股盈餘合計　Total basic earnings per share", "基本每股盈餘合計　Total primary earnings per share",
                     "營業活動之淨現金流入（流出）", "營業活動之淨現金流入（流出）Net cash flows from (used in) operating activities",
                     "資產總計", "資產總計　Total assets",
                     "不動產、廠房及設備", "不動產、廠房及設備合計", "不動產、廠房及設備 Property, plant and equipment",
                     "流動資產合計", "流動資產合計 Total current assets", 
                     "流動負債合計", "流動負債合計 Total current liabilities", 
                     "營業利益（損失）", "營業利益（損失）Net operating income (loss)",
                     "存貨", "存貨合計", "存貨 Current inventories", 
                     "利息費用", "利息費用 Interest expense", "利息費用_y", "利息費用 Interest expense_y", 
                     "應收帳款淨額", "應收帳款淨額 Accounts receivable, net",
                     "本期淨利", "本期淨利（淨損）", "本期淨利（淨損）Profit (loss)", "本期稅後淨利（淨損）", "本期稅後淨利（淨損）Profit (loss)",
                     "繼續營業單位稅前淨利（淨損）", "繼續營業單位稅前淨利（淨損）_x", "繼續營業單位稅前淨利（淨損）Profit (loss) from continuing operations before tax", "繼續營業單位稅前淨利（淨損）Profit (loss) from continuing operations before tax_x",
                     "營業收入合計", "營業收入合計　Total operating revenue",
                     "營業成本合計", "營業成本合計　Total operating costs",
                     "負債總計", "負債總計 Total liabilities",
                     "所得稅費用（利益）合計", "所得稅費用（利益）合計　Total tax expense (income)"]
                     
        for i in range(len(TableList)):
        
            Table = list(pd.read_csv(Path + "\\Finance_" + Number + ".csv", nrows=0)) + TableList
            Final_List = list(OrderedDict.fromkeys(Table))
      
            File_New = pd.read_csv(Path + "\\Finance_" + Number + ".csv", names=Final_List, na_values=['?'])

            File_New = File_New.drop(labels=0)   
            File_New.to_csv(Path + "\\Finance_" + Number + ".csv", index = False, encoding= "utf_8_sig")

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, names=Final_List, usecols=TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df = df.fillna(value=0)
        
        df.to_csv(Path + "\\Finance_" + Number + ".csv", encoding='utf-8-sig', index = False)
 
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        df = pd.read_csv(Path + "\\Finance_" + Number + ".csv")

        Table_Col = list(df.columns)

        TableList1 = []
        TableList2 = []
        TableList3 = []
        TableList4 = []

        for Table_List in Table_Col:

            if "權益" in Table_List:
                    
                TableList1.append(Table_List)
            
            if "營業活動之淨現金流入" in Table_List:
                    
                TableList2.append(Table_List)
            
            if "資產總計" in Table_List:
                    
                TableList3.append(Table_List)

            if "負債總計" in Table_List:
                    
                TableList4.append(Table_List)
                

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList1 + TableList2 + TableList3 + TableList4
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)

        df = df.loc[:, (df != 0).all(axis=0)]

        df.columns = ["會計項目", "資產總計", "負債總計", "權益總計", "營業活動之淨現金流入"]

        df.drop_duplicates(inplace=True)
                
        df.to_csv(Path + "\\Finance_" + Number + "-1.csv", encoding='utf-8-sig', index = False)
        # df.to_csv(Path + "\\Finance_" + Number + "-F.csv", encoding='utf-8-sig', index = False)
 
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "不動產" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "不動產、廠房及設備合計", "不動產、廠房及設備合計", "不動產、廠房及設備合計"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["不動產、廠房及設備合計"] = '0'
        
        df.to_csv(Path + "\\Finance_" + Number + "-2.csv", encoding='utf-8-sig', index = False)

        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "流動資產合計" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "流動資產合計", "流動資產合計"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["流動資產合計"] = '0'

        df.to_csv(Path + "\\Finance_" + Number + "-3.csv", encoding='utf-8-sig', index = False)

        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "流動負債合計" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "流動負債合計", "流動負債合計"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["流動負債合計"] = '0'
        
        df.to_csv(Path + "\\Finance_" + Number + "-4.csv", encoding='utf-8-sig', index = False)
        
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "營業利益" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "營業利益", "營業利益"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["營業利益"] = '0'

        df.to_csv(Path + "\\Finance_" + Number + "-5.csv", encoding='utf-8-sig', index = False)
        
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "存貨" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "存貨合計", "存貨合計", "存貨合計"]
        
        df.drop_duplicates(inplace=True)
      
        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["存貨合計"] = '0'
            
        df.to_csv(Path + "\\Finance_" + Number + "-6.csv", encoding='utf-8-sig', index = False)
        
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "利息費用" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "利息費用", "利息費用", "利息費用", "利息費用"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["利息費用"] = '0'
       
        df.to_csv(Path + "\\Finance_" + Number + "-7.csv", encoding='utf-8-sig', index = False)
   
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "應收帳款淨額" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "應收帳款淨額", "應收帳款淨額"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)
        
        if len(df.columns) < 2:

            df["應收帳款淨額"] = '0'
            
        df.to_csv(Path + "\\Finance_" + Number + "-8.csv", encoding='utf-8-sig', index = False)
        
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "本期" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "本期淨利", "本期淨利", "本期淨利", "本期淨利", "本期淨利"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["本期淨利"] = '0'
        
        df.to_csv(Path + "\\Finance_" + Number + "-9.csv", encoding='utf-8-sig', index = False)
       
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "營業收入合計" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "營業收入合計", "營業收入合計"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["營業收入合計"] = '0'

        df.to_csv(Path + "\\Finance_" + Number + "-10.csv", encoding='utf-8-sig', index = False)
        
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "營業成本合計" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "營業成本合計", "營業成本合計"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["營業成本合計"] = '0'

        df.to_csv(Path + "\\Finance_" + Number + "-11.csv", encoding='utf-8-sig', index = False)
        
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "基本每股盈餘合計" in Table_List:
                    
                TableList.append(Table_List)
            
        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "每股盈餘", "每股盈餘", "每股盈餘"]
       
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["每股盈餘"] = '0'

        df.to_csv(Path + "\\Finance_" + Number + "-12.csv", encoding='utf-8-sig', index = False)
        
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "繼續營業單位稅前淨利" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "繼續營業單位稅前淨利", "繼續營業單位稅前淨利", "繼續營業單位稅前淨利", "繼續營業單位稅前淨利"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)

        if len(df.columns) < 2:

            df["繼續營業單位稅前淨利"] = '0'

        df.to_csv(Path + "\\Finance_" + Number + "-13.csv", encoding='utf-8-sig', index = False)
     
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        TableList = []

        for Table_List in Table_Col:

            if "所得稅費用" in Table_List:
                    
                TableList.append(Table_List)

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=["會計項目"] + TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "所得稅費用", "所得稅費用"]
        
        df.drop_duplicates(inplace=True)

        if len(df.columns) > 2:
            
            df = df.loc[:, (df != 0).all(axis=0)]
            
            df = df.dropna(axis=0).fillna(value=df)
        
        if len(df.columns) < 2:

            df["所得稅費用"] = '0'

        df.to_csv(Path + "\\Finance_" + Number + "-14.csv", encoding='utf-8-sig', index = False)
        
        #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

        File_CSV = glob(Path + "\\Finance_" + Number + "-*.csv")

        File_List = [pd.read_csv(FCSV) for FCSV in File_CSV]
        
        Result = pd.merge(File_List[0], File_List[1], on="會計項目") 
        Result = pd.merge(Result, File_List[2], on="會計項目") 
        Result = pd.merge(Result, File_List[3], on="會計項目") 
        Result = pd.merge(Result, File_List[4], on="會計項目") 
        Result = pd.merge(Result, File_List[5], on="會計項目") 
        Result = pd.merge(Result, File_List[6], on="會計項目") 
        Result = pd.merge(Result, File_List[7], on="會計項目") 
        Result = pd.merge(Result, File_List[8], on="會計項目") 
        Result = pd.merge(Result, File_List[9], on="會計項目") 
        Result = pd.merge(Result, File_List[10], on="會計項目") 
        Result = pd.merge(Result, File_List[11], on="會計項目") 
        Result = pd.merge(Result, File_List[12], on="會計項目") 
        Result = pd.merge(Result, File_List[13], on="會計項目") 

        Result["代碼"] = Result["會計項目"] + "_" + Number 
        Result["股票代碼"] = Number 
        Result["股票名稱"] = Name
        Result["股票類別"] = Group

        Result.to_csv(Path + "\\Finance_" + Number + ".csv", index=0, encoding='utf-8-sig')

        for Num in range(1, 15):
        
            os.remove(Path + "\\Finance_" + Number + "-" + str(Num) + ".csv")

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌


def Get_CSV(Number):
    
    Folder = "C:\\Senior Project\\Finance\\"

    Files = os.listdir(Folder)

    for Num in range(0, len(Files)):
        
        File = ( os.listdir(Folder)[Num] )
       
        Path = Folder + File + "\\" + Number

        Files = glob(Path + "\\Finance_" + Number + ".csv")

        TableList = ["會計項目", "資產總計", "負債總計", "權益總計", "營業活動之淨現金流入", "營業收入合計", "營業成本合計", "每股盈餘", "繼續營業單位稅前淨利", "所得稅費用",  "不動產、廠房及設備合計", "流動資產合計", "流動負債合計", "營業利益", "存貨合計", "利息費用", "應收帳款淨額", "本期淨利", "代碼", "股票代碼", "股票名稱", "股票類別"]

        df = pd.concat(
            (pd.read_csv(Path + "\\Finance_" + Number + ".csv", header=0, usecols=TableList
                        ,dtype={'name': str, 'tweet':str}) for File in Files), sort=False, ignore_index=True)

        df.columns = ["會計項目", "資產總計", "負債總計", "權益總計", "營業活動之淨現金流入", "營業收入合計", "營業成本合計", "每股盈餘", "繼續營業單位稅前淨利", "所得稅費用",  "不動產、廠房及設備合計", "流動資產合計", "流動負債合計", "營業利益", "存貨合計", "利息費用", "應收帳款淨額", "本期淨利", "代碼", "股票代碼", "股票名稱", "股票類別"]

        df.to_csv(Path + "\\Finance_" + Number + ".csv", index=0, encoding='utf-8-sig')

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌


def Get_Result(Number, Name):

    Path = "C:\\Senior Project\\Finance\\"

    for i in range(0, len(os.listdir(Path))):

        Folder = (os.listdir(Path)[i]) 
        Files = Path + Folder + "\\" + Number

        Data_File = pd.read_csv(Files + "\\" + "Finance_" + Number + ".csv")
        
        with open("C:\\Senior Project\\" + 'Finance.csv', 'a+', newline="", encoding='utf-8-sig') as File:
            
            writer = csv.writer(File)

            with open("C:\\Senior Project\\" + 'Finance.csv', 'r', newline="", encoding='utf-8-sig') as File:
                
                render = csv.reader(File)

                if not [row for row in render]:

                    writer.writerow(("會計項目", "資產總計", "負債總計", "權益總計", "營業活動之淨現金流入", "營業收入合計", "營業成本合計", "每股盈餘", "繼續營業單位稅前淨利", "所得稅費用",  "不動產、廠房及設備合計", "流動資產合計", "流動負債合計", "營業利益", "存貨合計", "利息費用", "應收帳款淨額", "本期淨利", "代碼", "股票代碼", "股票名稱", "股票類別"))
                    writer.writerow((Data_File["會計項目"].values[0], Data_File["資產總計"].values[0], Data_File["負債總計"].values[0], Data_File["權益總計"].values[0], Data_File["營業活動之淨現金流入"].values[0], Data_File["營業收入合計"].values[0], Data_File["營業成本合計"].values[0], Data_File["每股盈餘"].values[0], Data_File["繼續營業單位稅前淨利"].values[0], Data_File["所得稅費用"].values[0], Data_File["不動產、廠房及設備合計"].values[0], Data_File["流動資產合計"].values[0], Data_File["流動負債合計"].values[0], Data_File["營業利益"].values[0], Data_File["存貨合計"].values[0], Data_File["利息費用"].values[0], Data_File["應收帳款淨額"].values[0], Data_File["本期淨利"].values[0], Data_File["代碼"].values[0], Data_File["股票代碼"].values[0], Data_File["股票名稱"].values[0], Data_File["股票類別"].values[0]))
                else:
                    
                    writer.writerow((Data_File["會計項目"].values[0], Data_File["資產總計"].values[0], Data_File["負債總計"].values[0], Data_File["權益總計"].values[0], Data_File["營業活動之淨現金流入"].values[0], Data_File["營業收入合計"].values[0], Data_File["營業成本合計"].values[0], Data_File["每股盈餘"].values[0], Data_File["繼續營業單位稅前淨利"].values[0], Data_File["所得稅費用"].values[0], Data_File["不動產、廠房及設備合計"].values[0], Data_File["流動資產合計"].values[0], Data_File["流動負債合計"].values[0], Data_File["營業利益"].values[0], Data_File["存貨合計"].values[0], Data_File["利息費用"].values[0], Data_File["應收帳款淨額"].values[0], Data_File["本期淨利"].values[0], Data_File["代碼"].values[0], Data_File["股票代碼"].values[0], Data_File["股票名稱"].values[0], Data_File["股票類別"].values[0]))
                
# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌


def Get_Finance(num, name, number, season, seasons):

    Path = "C:\\Senior Project\\"

    Data_File = pd.read_csv(Path + "Finance.csv", index_col="代碼", encoding="utf_8_sig").replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)
    
    # ▌▌▌▌▌▌ ◎ 流動比率  

    try:
        Current_Assets = Data_File.loc[season + "_" + number, "流動資產合計"]

        Current_Liabilities = Data_File.loc[season + "_" + number, "流動負債合計"]

        Current_Ratio = float(Current_Assets) / float(Current_Liabilities)

        Data_File.loc[season + "_" + number, "流動比率"] = Current_Ratio
        Data_File.loc[season + "_" + number, "流動比率"] = round(Data_File.loc[season + "_" + number, "流動比率"]*100, 2)
    except:
        Data_File.loc[season + "_" + number, "流動比率"] = '0'
   
    # ▌▌▌▌▌▌ ◎ 速動比率  

    try:
        Current_Inventories = Data_File.loc[season + "_" + number, "存貨合計"]

        Quick_Ratio = ( float(Current_Assets) - float(Current_Inventories) ) / float(Current_Liabilities)

        Data_File.loc[season + "_" + number, "速動比率"] = Quick_Ratio
        Data_File.loc[season + "_" + number, "速動比率"] = round(Data_File.loc[season + "_" + number, "速動比率"]*100, 2)
    except:
        Data_File.loc[season + "_" + number, "速動比率"] = '0'

    # ▌▌▌▌▌▌ ◎ 利息保障倍數 

    try:
        if season[4:6] == "Q1":

            Interest_Expense = Data_File.loc[season + "_" + number, "利息費用"]
            Profit_Btax  = Data_File.loc[season + "_" + number, "繼續營業單位稅前淨利"]

        else:
            Interest_Expense = Data_File.loc[season + "_" + number, "利息費用"]
            Interest_LExpense = Data_File.loc[seasons[num-1] + "_" + number, "利息費用"]

            Profit_Btax  = Data_File.loc[season + "_" + number, "繼續營業單位稅前淨利"]

            Interest_Expense = Interest_Expense - Interest_LExpense

        if season[4:6] == "Q4":

            Interest_Expense = Data_File.loc[season + "_" + number, "利息費用"]
            Interest_LExpense = Data_File.loc[seasons[num-1] + "_" + number, "利息費用"]

            Profit_Btax  = Data_File.loc[season + "_" + number, "繼續營業單位稅前淨利"]
            Profit_Btax1  = Data_File.loc[seasons[num-1] + "_" + number, "繼續營業單位稅前淨利"]
            Profit_Btax2  = Data_File.loc[seasons[num-2] + "_" + number, "繼續營業單位稅前淨利"]
            Profit_Btax3  = Data_File.loc[seasons[num-3] + "_" + number, "繼續營業單位稅前淨利"]
        
            Profit_Btax = Profit_Btax - Profit_Btax1 - Profit_Btax2 - Profit_Btax3
            Interest_Expense = Interest_Expense - Interest_LExpense

            
        TIER = ( float(Profit_Btax) + float(Interest_Expense) ) / float(Interest_Expense)
        
        Data_File.loc[season + "_" + number, "利息保障倍數"] = TIER
        Data_File.loc[season + "_" + number, "利息保障倍數"] = round(Data_File.loc[season + "_" + number, "利息保障倍數"], 2)
    except:
        Data_File.loc[season + "_" + number, "利息保障倍數"] = '0'

    # ▌▌▌▌▌▌ ◎ 負債佔資產比率 

    try:
        Total_Assets = Data_File.loc[season + "_" + number, "資產總計"]

        Total_Liabilities = Data_File.loc[season + "_" + number, "負債總計"]
    
        Debt_Ratio = float(Total_Liabilities) / float(Total_Assets)

        Data_File.loc[season + "_" + number, "負債比"] = Debt_Ratio
        Data_File.loc[season + "_" + number, "負債比"] = round(Data_File.loc[season + "_" + number, "負債比"]*100, 2)
    except:
        Data_File.loc[season + "_" + number, "負債比"] = '0'

    # ▌▌▌▌▌▌ ◎ 稅後淨利率 = 純益率

    try:
        if season[4:6] == "Q4":

            Income_Net = Data_File.loc[season + "_" + number, "本期淨利"]
            Income_Net1  = Data_File.loc[seasons[num-1] + "_" + number, "本期淨利"]
            Income_Net2  = Data_File.loc[seasons[num-2] + "_" + number, "本期淨利"]
            Income_Net3  = Data_File.loc[seasons[num-3] + "_" + number, "本期淨利"]
        
            Operating_Revenue = Data_File.loc[season + "_" + number, "營業收入合計"]
            Operating_Revenue1  = Data_File.loc[seasons[num-1] + "_" + number, "營業收入合計"]
            Operating_Revenue2  = Data_File.loc[seasons[num-2] + "_" + number, "營業收入合計"]
            Operating_Revenue3  = Data_File.loc[seasons[num-3] + "_" + number, "營業收入合計"]

            Income_Net = Income_Net - Income_Net1 - Income_Net2 - Income_Net3
            Operating_Revenue = Operating_Revenue - Operating_Revenue1 - Operating_Revenue2 - Operating_Revenue3

        else:

            Income_Net = Data_File.loc[season + "_" + number, "本期淨利"]

            Operating_Revenue = Data_File.loc[season + "_" + number, "營業收入合計"]

        Profit_Margin = float(Income_Net) / float(Operating_Revenue)

        Data_File.loc[season + "_" + number, "稅後淨利率"] = Profit_Margin
        Data_File.loc[season + "_" + number, "稅後淨利率"] = round(Data_File.loc[season + "_" + number, "稅後淨利率"]*100, 2)
    except:
        Data_File.loc[season + "_" + number, "稅後淨利率"] = '0'

    # ▌▌▌▌▌▌ ◎ 存貨週轉率  

    try:
        if season[4:6] == "Q4":

            Current_Inventories = Data_File.loc[season + "_" + number, "存貨合計"]
            Current_LInventories = Data_File.loc[seasons[num-1] + "_" + number, "存貨合計"]

            Operating_Costs = Data_File.loc[season + "_" + number, "營業成本合計"]
            Operating_Costs1 = Data_File.loc[seasons[num-1] + "_" + number, "營業成本合計"]
            Operating_Costs2 = Data_File.loc[seasons[num-2] + "_" + number, "營業成本合計"]
            Operating_Costs3 = Data_File.loc[seasons[num-3] + "_" + number, "營業成本合計"]

            Operating_Costs = Operating_Costs - Operating_Costs1 - Operating_Costs2 - Operating_Costs3
            
        else:
            
            Current_Inventories = Data_File.loc[season + "_" + number, "存貨合計"]
            Current_LInventories = Data_File.loc[seasons[num-1] + "_" + number, "存貨合計"]

            Operating_Costs = Data_File.loc[season + "_" + number, "營業成本合計"]

        Average_Inventories = (float(Current_Inventories) + float(Current_LInventories)) / 2
            
        Inventory_Turnover = float(Operating_Costs) / float(Average_Inventories)
        
        Data_File.loc[season + "_" + number, "存貨週轉率"] = Inventory_Turnover
        Data_File.loc[season + "_" + number, "存貨週轉率"] = round(Data_File.loc[season + "_" + number, "存貨週轉率"], 2)

    except:
        Data_File.loc[season + "_" + number, "存貨週轉率"] = '0'

    # ▌▌▌▌▌▌ ◎ 資產報酬率(ROA)  (未確認)

    # try:

    if season[4:6] == "Q1":

        Income_Net = Data_File.loc[season + "_" + number, "本期淨利"]
        Interest_Expense = Data_File.loc[seasons[num]  + "_" + number, "利息費用"]

        Income_Tte = Data_File.loc[season + "_" + number, "所得稅費用"]
        Profit_Btax  = Data_File.loc[season + "_" + number, "繼續營業單位稅前淨利"]
        
        Total_Assets = Data_File.loc[seasons[num] + "_" + number, "資產總計"]
        Total_LAssets = Data_File.loc[seasons[num-1] + "_" + number, "資產總計"]

    elif season[4:6] == "Q4":

        Income_Net = Data_File.loc[seasons[num] + "_" + number, "本期淨利"]
        Income_Net1 = Data_File.loc[seasons[num-1] + "_" + number, "本期淨利"]
        Income_Net2 = Data_File.loc[seasons[num-2] + "_" + number, "本期淨利"]
        Income_Net3 = Data_File.loc[seasons[num-3] + "_" + number, "本期淨利"]
        
        Income_Tte = Data_File.loc[seasons[num] + "_" + number, "所得稅費用"]
        Income_Tte1 = Data_File.loc[seasons[num-1] + "_" + number, "所得稅費用"]
        Income_Tte2 = Data_File.loc[seasons[num-2] + "_" + number, "所得稅費用"]
        Income_Tte3 = Data_File.loc[seasons[num-3] + "_" + number, "所得稅費用"]
        
        Profit_Btax  = Data_File.loc[seasons[num] + "_" + number, "繼續營業單位稅前淨利"]
        Profit_Btax1  = Data_File.loc[seasons[num-1] + "_" + number, "繼續營業單位稅前淨利"]
        Profit_Btax2  = Data_File.loc[seasons[num-2] + "_" + number, "繼續營業單位稅前淨利"]
        Profit_Btax3  = Data_File.loc[seasons[num-3] + "_" + number, "繼續營業單位稅前淨利"]

        Interest_Expense = Data_File.loc[seasons[num]  + "_" + number, "利息費用"]
        Interest_Expense1 = Data_File.loc[seasons[num-1] + "_" + number, "利息費用"]
        
        Total_Assets = Data_File.loc[seasons[num] + "_" + number, "資產總計"]
        Total_LAssets = Data_File.loc[seasons[num-1] + "_" + number, "資產總計"]

        Income_Net = Income_Net - Income_Net1 - Income_Net2 - Income_Net3
        Income_Tte = Income_Tte - Income_Tte1 - Income_Tte2 - Income_Tte3
        Profit_Btax = Profit_Btax - Profit_Btax1 - Profit_Btax2 - Profit_Btax3
        
        Interest_Expense = Interest_Expense - Interest_Expense1

    else:

        Income_Net = Data_File.loc[season + "_" + number, "本期淨利"]
        
        Income_Tte = Data_File.loc[season + "_" + number, "所得稅費用"]
        Profit_Btax  = Data_File.loc[season + "_" + number, "繼續營業單位稅前淨利"]

        Interest_Expense = Data_File.loc[seasons[num]  + "_" + number, "利息費用"]
        Interest_LExpense = Data_File.loc[seasons[num-1] + "_" + number, "利息費用"]
        
        Total_Assets = Data_File.loc[seasons[num] + "_" + number, "資產總計"]
        Total_LAssets = Data_File.loc[seasons[num-1] + "_" + number, "資產總計"]

        Interest_Expense = Interest_Expense - Interest_LExpense

    Tax_Rate = round((float(Income_Tte) / float(Profit_Btax)), 4)
    Average_Assets = (float(Total_Assets) + float(Total_LAssets)) / 2

    Total_ROA = (float(Income_Net) + float(Interest_Expense) * (1 - Tax_Rate))

    ROA = float(Total_ROA) / float(Average_Assets)

    Data_File.loc[season + "_" + number, "ROA"] = ROA
    Data_File.loc[season + "_" + number, "ROA"] = round(Data_File.loc[season + "_" + number, "ROA"]*100, 2)

    # except:
    #     Data_File.loc[season + "_" + number, "ROA"] = '0'

    # ▌▌▌▌▌▌ ◎ 股東權益報酬率(ROE)

    try:
        if season[4:6] != "Q4":

            Income_Net = Data_File.loc[season + "_" + number, "本期淨利"]
        else:
            Income_Net = Data_File.loc[season + "_" + number, "本期淨利"]
            Income_Net1 = Data_File.loc[seasons[num-1] + "_" + number, "本期淨利"]
            Income_Net2 = Data_File.loc[seasons[num-2] + "_" + number, "本期淨利"]
            Income_Net3 = Data_File.loc[seasons[num-3] + "_" + number, "本期淨利"]
            Income_Net = Income_Net - (Income_Net1 + Income_Net2 + Income_Net3)

        Total_Equity = Data_File.loc[season + "_" + number, "權益總計"]
        Total_LEquity = Data_File.loc[seasons[num-1] + "_" + number, "權益總計"]

        Average_Equity = (Total_Equity + Total_LEquity) / 2

        ROE = float(Income_Net) / float(Average_Equity)

        Data_File.loc[season + "_" + number, "ROE"] = ROE
        Data_File.loc[season + "_" + number, "ROE"] = round(Data_File.loc[season + "_" + number, "ROE"]*100, 2)
    except:
        Data_File.loc[season + "_" + number, "ROE"] = '0'

    # ▌▌▌▌▌▌ ◎  毛利率

    try:
        if season[4:6] != "Q4":

            Operating_Costs = Data_File.loc[season + "_" + number, "營業成本合計"]
            Operating_Revenue = Data_File.loc[season + "_" + number, "營業收入合計"]
        else:
            Operating_Costs = Data_File.loc[seasons[num] + "_" + number, "營業成本合計"]
            Operating_Costs1 = Data_File.loc[seasons[num-1] + "_" + number, "營業成本合計"]
            Operating_Costs2 = Data_File.loc[seasons[num-2] + "_" + number, "營業成本合計"]
            Operating_Costs3 = Data_File.loc[seasons[num-3] + "_" + number, "營業成本合計"]

            Operating_Revenue = Data_File.loc[seasons[num] + "_" + number, "營業收入合計"]
            Operating_Revenue1 = Data_File.loc[seasons[num-1] + "_" + number, "營業收入合計"]
            Operating_Revenue2 = Data_File.loc[seasons[num-2] + "_" + number, "營業收入合計"]
            Operating_Revenue3 = Data_File.loc[seasons[num-3] + "_" + number, "營業收入合計"]

            Operating_Costs = Operating_Costs - Operating_Costs1 - Operating_Costs2 - Operating_Costs3
            Operating_Revenue = Operating_Revenue - Operating_Revenue1 - Operating_Revenue2 - Operating_Revenue3

        Gross_Margin =  ((float(Operating_Revenue) - float(Operating_Costs)) / float(Operating_Revenue))

        Data_File.loc[season + "_" + number, "毛利率"] = Gross_Margin
        Data_File.loc[season + "_" + number, "毛利率"] = round(Data_File.loc[season + "_" + number, "毛利率"]*100, 2)
    except:
        Data_File.loc[season + "_" + number, "毛利率"] = '0'

    #  ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍

    with open("C:\\Senior Project\\" + 'Result.csv', 'a+', newline="", encoding='utf-8-sig') as File:
              
        writer = csv.writer(File)

        with open("C:\\Senior Project\\" + 'Result.csv', 'r', newline="", encoding='utf-8-sig') as File:
            
            render = csv.reader(File)

            if not [row for row in render]:

                writer.writerow(("會計項目", "資產總計", "負債總計", "權益總計", "營業活動之淨現金流入", "營業收入合計", "營業成本合計", "每股盈餘", "繼續營業單位稅前淨利", "所得稅費用", "不動產、廠房及設備合計", "流動資產合計", "流動負債合計", "營業利益", "存貨合計", "利息費用", "應收帳款淨額", "本期淨利", "流動比率", "速動比率", "利息保障倍數", "負債比", "稅後淨利率", "存貨週轉率", "ROA", "ROE", "毛利率", "股票代碼", "股票名稱", "股票類別"))
                writer.writerow((Data_File.loc[season + "_" + number, "會計項目"], Data_File.loc[season + "_" + number, "資產總計"], Data_File.loc[season + "_" + number, "負債總計"], Data_File.loc[season + "_" + number, "權益總計"], Data_File.loc[season + "_" + number, "營業活動之淨現金流入"], Data_File.loc[season + "_" + number, "營業收入合計"], Data_File.loc[season + "_" + number, "營業成本合計"], Data_File.loc[season + "_" + number, "每股盈餘"], Data_File.loc[season + "_" + number, "繼續營業單位稅前淨利"], Data_File.loc[season + "_" + number, "所得稅費用"], Data_File.loc[season + "_" + number, "不動產、廠房及設備合計"], Data_File.loc[season + "_" + number, "流動資產合計"], Data_File.loc[season + "_" + number, "流動負債合計"], Data_File.loc[season + "_" + number, "營業利益"], Data_File.loc[season + "_" + number, "存貨合計"], Data_File.loc[season + "_" + number, "利息費用"], Data_File.loc[season + "_" + number, "應收帳款淨額"], Data_File.loc[season + "_" + number, "本期淨利"], Data_File.loc[season + "_" + number, "流動比率"], Data_File.loc[season + "_" + number, "速動比率"], Data_File.loc[season + "_" + number, "利息保障倍數"], Data_File.loc[season + "_" + number, "負債比"], Data_File.loc[season + "_" + number, "稅後淨利率"], Data_File.loc[season + "_" + number, "存貨週轉率"], Data_File.loc[season + "_" + number, "ROA"], Data_File.loc[season + "_" + number, "ROE"], Data_File.loc[season + "_" + number, "毛利率"], Data_File.loc[season + "_" + number, "股票代碼"], Data_File.loc[season + "_" + number, "股票名稱"], Data_File.loc[season + "_" + number, "股票類別"]))
            else:
                writer.writerow((Data_File.loc[season + "_" + number, "會計項目"], Data_File.loc[season + "_" + number, "資產總計"], Data_File.loc[season + "_" + number, "負債總計"], Data_File.loc[season + "_" + number, "權益總計"], Data_File.loc[season + "_" + number, "營業活動之淨現金流入"], Data_File.loc[season + "_" + number, "營業收入合計"], Data_File.loc[season + "_" + number, "營業成本合計"], Data_File.loc[season + "_" + number, "每股盈餘"], Data_File.loc[season + "_" + number, "繼續營業單位稅前淨利"], Data_File.loc[season + "_" + number, "所得稅費用"], Data_File.loc[season + "_" + number, "不動產、廠房及設備合計"], Data_File.loc[season + "_" + number, "流動資產合計"], Data_File.loc[season + "_" + number, "流動負債合計"], Data_File.loc[season + "_" + number, "營業利益"], Data_File.loc[season + "_" + number, "存貨合計"], Data_File.loc[season + "_" + number, "利息費用"], Data_File.loc[season + "_" + number, "應收帳款淨額"], Data_File.loc[season + "_" + number, "本期淨利"], Data_File.loc[season + "_" + number, "流動比率"], Data_File.loc[season + "_" + number, "速動比率"], Data_File.loc[season + "_" + number, "利息保障倍數"], Data_File.loc[season + "_" + number, "負債比"], Data_File.loc[season + "_" + number, "稅後淨利率"], Data_File.loc[season + "_" + number, "存貨週轉率"], Data_File.loc[season + "_" + number, "ROA"], Data_File.loc[season + "_" + number, "ROE"], Data_File.loc[season + "_" + number, "毛利率"], Data_File.loc[season + "_" + number, "股票代碼"], Data_File.loc[season + "_" + number, "股票名稱"], Data_File.loc[season + "_" + number, "股票類別"]))
            
# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌

def Result_Nan():

    df = pd.read_csv("C:\\Senior Project\\" + 'Result.csv', index_col=False, encoding="utf-8-sig") 
       
    df = df.dropna(axis=0, how='any')

    df.to_csv("C:\\Senior Project\\" + 'Result.csv', index =False, encoding="utf-8-sig")


def GetDB():

    conn = sqlite3.connect("C:\\Senior Project\\Finance.db")

    df = pd.read_csv("C:\\Senior Project\\" + 'Result.csv', encoding="utf-8-sig") 
            
    df.to_sql("Result", conn, if_exists="append", index=False)

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌
