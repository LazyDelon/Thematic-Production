import os
import csv
import sqlite3
from sys import exec_prefix
from numpy import int64
import pandas as pd
from glob import glob
from traceback import print_tb
from collections import OrderedDict
from cmath import nan

def get_stocknumber():
    res = []
    try:
        with open('stock_number.csv', encoding="utf-8") as f:
            slist = f.readlines()
            # print('讀入：',slist)
            for lst in slist:
                s = lst.split(',')
                res.append([s[0].strip(),str(s[1].strip()),str(s[2].strip())])
    except:
        print('讀不到')
    return res

def read_folder_saveCSV(path,html_path,number,group):
    for i in range(0,len(os.listdir(html_path))):
        folder = (os.listdir(html_path)[i]) #取得陣列中的資料夾名稱
        file_path = (html_path+"\\"+folder+"\\"+number+".html")
        result = os.path.isfile(file_path)
        if result == True:
            df = pd.read_html(html_path+"\\"+folder+"\\"+number+".html") #讀取資料夾內的檔案
            for index_num in range(0,3): #取得陣列中的資料
                file_num = str(index_num+1) #資料儲存檔名
                Path_CSV = path+"\\"+group+"\\"+folder+"\\"+number #設定資料存放路徑
                if not os.path.isdir(Path_CSV): #判斷資料夾是否存在
                    os.makedirs(Path_CSV) #新增資料夾
                df[index_num].to_csv(Path_CSV+"\\"+number+"_"+file_num+".csv", index = False, encoding='utf_8-sig')
        else:
            pass

def combine_all_data(path,html_path,number,name,group):
    Path = path+"\\"+group #設定資料存放路徑
    for i in range(0,len(os.listdir(html_path))):
        folder = (os.listdir(html_path)[i]) #取得陣列中的資料夾名稱
        Path_CSV = Path+"\\"+folder+"\\"+number #設定個股資料存放路徑
        file_path = (Path_CSV+"\\"+number+"_1.csv")
        
        result = os.path.isfile(file_path)
       
        if result == True:

            for x in range(1,4):
                file_num = str(x) #轉換資料型別
                df = pd.read_csv(Path_CSV+"\\"+number+"_"+file_num+".csv", encoding= "utf_8_sig") #取得csv檔案位置
                num = (len(df.columns))+1 #取得csv表格列數
                df = df.values.tolist() #整個轉為list
                num_list = [] #設定一個空陣列，放置列數
                for i in range(1, num):
                    num_list += [i]
                num_list = [str(i) for i in num_list] #將陣列從int轉str
                df = pd.DataFrame(columns = num_list, data = df)
                #刪除num_list陣列的3、4
                del num_list[1] #刪除num_list陣列的3
                del num_list[1] #刪除num_list陣列的4
                df = df.drop(num_list,axis=1) #刪除不需要的資料
                data = df.values #把 Dataframe 轉成 2D numpy array
                index1 = list(df.keys()) #找到數據的 key
                data = list(map(list, zip(*data))) #行列互換，再利用map函數將zip內的元組轉列表
                data = pd.DataFrame(data, index=index1)
                data.to_csv(Path_CSV+"\\"+number+"_getfile_"+file_num+".csv",header=0, encoding= "utf_8_sig") #存檔
            files = glob(Path_CSV+"\\"+number+"_getfile_1.csv") #取得檔案
            df = pd.read_csv(Path_CSV+"\\"+number+"_getfile_1.csv")
            dfs = df.head(0)

            if '權益總額 Total equity' in dfs:
                df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['2','權益總額 Total equity'] #抓取需要的資料
                                            ,dtype={'name': str, 'tweet':str}) for file in files), sort=False, ignore_index=True)
                df.to_csv(Path_CSV+"\\"+number+"_getfile_1.csv", encoding= "utf_8_sig", index = False) #存檔
            
            elif '權益總計 Total equity' in dfs:
                df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['2','權益總計 Total equity'] #抓取需要的資料
                                            ,dtype={'name': str, 'tweet':str}) for file in files), sort=False, ignore_index=True)
                df.to_csv(Path_CSV+"\\"+number+"_getfile_1.csv", encoding= "utf_8_sig", index = False) #存檔
            
            elif '權益總計 Equity' in dfs:
                df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['2','權益總計 Equity'] #抓取需要的資料
                                            ,dtype={'name': str, 'tweet':str}) for file in files), sort=False, ignore_index=True)
                df.to_csv(Path_CSV+"\\"+number+"_getfile_1.csv", encoding= "utf_8_sig", index = False) #存檔
            
            files = glob(Path_CSV+"\\"+number+"_getfile_2.csv") #取得檔案
            df = pd.concat(
                        (pd.read_csv(file,header=0, usecols=['2'] #抓取需要的資料
                                        ,dtype={'name': str, 'tweet':str}) for file in files), sort=False, ignore_index=True)
            df.to_csv(Path_CSV+"\\"+number+"_getfile_2.csv", encoding= "utf_8_sig", index = False) #存檔
            
            files = glob(Path_CSV+"\\"+number+"_getfile_3.csv") #取得檔案
            df = pd.concat(
                        (pd.read_csv(file,header=0, usecols=['2','繼續營業單位稅前淨利（淨損）　Profit (loss) from continuing operations before tax',
                        '本期稅前淨利（淨損）　Profit (loss) before tax'] #抓取需要的資料
                                        ,dtype={'name': str, 'tweet':str}) for file in files), sort=False, ignore_index=True)
            df.to_csv(Path_CSV+"\\"+number+"_getfile_3.csv", encoding= "utf_8_sig", index = False) #存檔
            
            files = glob(Path_CSV+"\\"+number+"_getfile_*"+".csv") #取得資料夾內需要的資料
            df_list = [pd.read_csv(file) for file in files] #串列中包含兩個Pandas DataFrame
            result = pd.merge(df_list[0],df_list[1], on='2') #進行資料合併
            result = pd.merge(result,df_list[2],on='2') #進行資料合併
            result["股票代碼"] = number #新增股票代碼
            result["股票名稱"] = name #新增股票名稱
            result["股票類別"] = group #新增股票名稱
            result["季"] = folder #新增季別
            
            
            folder_save = Path_CSV+"\\計算"
            if not os.path.isdir(folder_save): #判斷資料夾是否存在
                os.makedirs(folder_save) #新增資料夾
            result.to_csv(folder_save+"\\stock_"+number+".csv", encoding='utf_8-sig', index = False) #存檔
        else:
            pass

def csv_data(path,number,html_path,group):
    Path = path+"\\"+group
    for i in range(0,len(os.listdir(html_path))):
        folder = (os.listdir(html_path)[i]) #取得陣列中的資料夾名稱
        Path_CSV = Path+"\\"+folder+"\\"+number #設定個股資料存放路徑
        file_path = (Path_CSV)
        result = os.path.isdir(file_path)
        if result == True:
            files = glob(Path_CSV+"\\計算\\stock_"+number+".csv")
            df = pd.read_csv(Path_CSV+"\\計算\\stock_"+number+".csv")
            dfs = df.head(0)
            
            if '權益總額 Total equity' in dfs:
                
                if '本期稅前淨利（淨損）　Profit (loss) before tax' in dfs:
                    df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['權益總額 Total equity',
                                                                '本期稅前淨利（淨損）　Profit (loss) before tax',
                                                                '股票代碼','股票名稱','股票類別','季']
                                            ,dtype={'name': str, 'tweet':str}) for file in files),
                            sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)
                    df.columns = ['權益總計','本期稅前淨利',
                                '股票代碼','股票名稱','股票類別','季']
                
                elif '繼續營業單位稅前淨利（淨損）　Profit (loss) from continuing operations before tax' in dfs:
                    df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['權益總額 Total equity','繼續營業單位稅前淨利（淨損）　Profit (loss) from continuing operations before tax',
                                                                '股票代碼','股票名稱','股票類別','季']
                                            ,dtype={'name': str, 'tweet':str}) for file in files),
                            sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)
                    df.columns = ['權益總計','本期稅前淨利',
                                '股票代碼','股票名稱','股票類別','季']
            
            elif '權益總計 Total equity' in dfs:
                
                if '本期稅前淨利（淨損）　Profit (loss) before tax' in dfs:
                    df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['權益總計 Total equity',
                                                                '本期稅前淨利（淨損）　Profit (loss) before tax',
                                                                '股票代碼','股票名稱','股票類別','季']
                                            ,dtype={'name': str, 'tweet':str}) for file in files),
                            sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)
                    df.columns = ['權益總計','本期稅前淨利',
                                '股票代碼','股票名稱','股票類別','季']
                
                elif '繼續營業單位稅前淨利（淨損）　Profit (loss) from continuing operations before tax' in dfs:
                    df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['權益總計 Total equity','繼續營業單位稅前淨利（淨損）　Profit (loss) from continuing operations before tax',
                                                                '股票代碼','股票名稱','股票類別','季']
                                            ,dtype={'name': str, 'tweet':str}) for file in files),
                            sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)
                    df.columns = ['權益總計','本期稅前淨利',
                                '股票代碼','股票名稱','股票類別','季']
            
            elif '權益總計 Equity' in dfs:
                
                if '本期稅前淨利（淨損）　Profit (loss) before tax' in dfs:
                    
                    df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['權益總計 Equity',
                                                                '本期稅前淨利（淨損）　Profit (loss) before tax',
                                                                '股票代碼','股票名稱','股票類別','季']
                                            ,dtype={'name': str, 'tweet':str}) for file in files),
                            sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)
                    df.columns = ['權益總計','本期稅前淨利',
                                '股票代碼','股票名稱','股票類別','季']
                
                elif '繼續營業單位稅前淨利（淨損）　Profit (loss) from continuing operations before tax' in dfs:
                    
                    df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['權益總計 Equity','繼續營業單位稅前淨利（淨損）　Profit (loss) from continuing operations before tax',
                                                                '股票代碼','股票名稱','股票類別','季']
                                            ,dtype={'name': str, 'tweet':str}) for file in files),
                            sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)
                    df.columns = ['權益總計','本期稅前淨利',
                                '股票代碼','股票名稱','股票類別','季']
            
            elif '負債及權益總計　Total liabilities and equity' in dfs:
                
                if '本期稅前淨利（淨損）　Profit (loss) before tax' in dfs:
                    
                    df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['負債及權益總計　Total liabilities and equity',
                                                                '本期稅前淨利（淨損）　Profit (loss) before tax',
                                                                '股票代碼','股票名稱','股票類別','季']
                                            ,dtype={'name': str, 'tweet':str}) for file in files),
                            sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)
                    df.columns = ['權益總計','本期稅前淨利',
                                '股票代碼','股票名稱','股票類別','季']
                
                elif '繼續營業單位稅前淨利（淨損）　Profit (loss) from continuing operations before tax' in dfs:
                    
                    df = pd.concat(
                            (pd.read_csv(file,header=0, usecols=['負債及權益總計　Total liabilities and equity','繼續營業單位稅前淨利（淨損）　Profit (loss) from continuing operations before tax',
                                                                '股票代碼','股票名稱','股票類別','季']
                                            ,dtype={'name': str, 'tweet':str}) for file in files),
                            sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)
                    df.columns = ['權益總計','本期稅前淨利',
                                '股票代碼','股票名稱','股票類別','季']
            # 新增計算 ROE
            folder_true = Path+"\\"+folder+"\\"+number
            print(folder_true)
            result = os.path.isdir(folder_true)
            print(result)
            if result == True: #判斷資料夾是否存在
                
                if folder == '2019Q4' or folder == '2020Q4':
                    folder1 = (os.listdir(html_path)[i-3])
                    Path_CSV1 = Path+"\\"+folder1+"\\"+number
                    df1 = pd.read_csv(Path_CSV1+"\\計算\\stock_"+number+".csv")
                    a1 = (df1.本期稅前淨利.astype(int64))
                    folder2 = (os.listdir(html_path)[i-2])
                    Path_CSV2 = Path+"\\"+folder2+"\\"+number
                    df2 = pd.read_csv(Path_CSV2+"\\計算\\stock_"+number+".csv")
                    a2 = (df2.本期稅前淨利.astype(int64))
                    folder3 = (os.listdir(html_path)[i-1])
                    Path_CSV3 = Path+"\\"+folder3+"\\"+number
                    df3 = pd.read_csv(Path_CSV3+"\\計算\\stock_"+number+".csv")
                    a3 = (df3.本期稅前淨利.astype(int64))
                    a = (df.本期稅前淨利.astype(int64))
                    a = (a-a1-a2-a3)
                    df["ROE"] = a / (df.權益總計.astype(int64))
                    df["ROE"] = round(df["ROE"]*100,2) 
                else:
                    df["ROE"] = ((df.本期稅前淨利.astype(int64)) / (df.權益總計.astype(int64)))
                    df["ROE"] = round(df["ROE"]*100,2) 
                df.to_csv(Path_CSV+"\\計算\\stock_"+number+".csv", encoding="utf_8-sig", index = False)
            else:
                df["ROE"] = 'None'
                df.to_csv(Path_CSV+"\\計算\\stock_"+number+".csv", encoding="utf_8-sig", index = False)
        else:
            pass

def csv_db(path,html_path,number,group):
    Path = path+"\\"+group
    for i in range(0,len(os.listdir(html_path))):
        folder = (os.listdir(html_path)[i])
        Path_CSV = Path+"\\"+folder+"\\"+number
        file_path = (Path_CSV+"\\計算\\stock_"+number+".csv")
        result = os.path.isfile(file_path)
        if result == True:
            sql_data = path+"\\DB\\"
            if not os.path.isdir(sql_data):
                os.makedirs(sql_data)
            conn = sqlite3.connect("Stock.db")
            df = pd.read_csv(Path_CSV+"\\計算\\stock_"+number+".csv", encoding="utf_8-sig")
            df.to_sql("Stock", conn, if_exists="append", index=False)
        else:
            pass
