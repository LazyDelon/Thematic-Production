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


def get_data(path,number,group,s):
    try:
        df = pd.read_html(path+"\\html\\tifrs-"+s+"\\"+number+".html")#取得放置html的資料夾
        # 查詢是否已有資料夾，無資料夾則新增一個
        folder = ""+path+group+"\\"+s+"\\"+number+"//"
        if not os.path.isdir(folder):
            os.makedirs(folder)
        #分割網頁表格分開存檔
        df[0].to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_1.csv",header=0, encoding= "utf_8_sig")
        df[1].to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_2.csv",header=0, encoding= "utf_8_sig")
        df[2].to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_3.csv",header=0, encoding= "utf_8_sig")
    except:
        pass


def combine_all_data(path,number,name,group,s):

    for i in range(1,4):
        
        #取得csv檔案位置
        a = str(i)
        df = pd.read_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_"+a+".csv", encoding= "utf_8_sig")
        #取得csv表格列數
        num = (len(df.columns))+1
        #整個轉為list
        df = df.values.tolist()
        #設定一個空陣列，放置列數
        num_list = []
        for i in range(1, num):
            num_list += [i]
        #將陣列從int轉str
        num_list = [str(i) for i in num_list]
        df = pd.DataFrame(columns = num_list, data = df)
        #刪除num_list陣列的3、4
        del num_list[2]
        del num_list[2]
        #刪除不需要的資料
        df = df.drop(num_list,axis=1)
        #把 Dataframe 轉成 2D numpy array
        data = df.values
        #找到數據的 key
        index1 = list(df.keys())
        #行列互換，再利用map函數將zip內的元組轉列表
        data = list(map(list, zip(*data)))
        data = pd.DataFrame(data, index=index1)

        #存檔
        data.to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_new_"+a+".csv",header=0, encoding= "utf_8_sig")
    
    

    files = glob(path+group+"\\"+s+"\\"+number+"//"+number+"_new_1.csv")

    datalist = ['3','應收帳款淨額 Accounts receivable, net','流動資產合計 Total current assets','流動負債合計 Total current liabilities',
                '存貨 Current inventories','不動產、廠房及設備 Property, plant and equipment',
                '資產總計　Total assets','負債總計 Total liabilities']
    
    # for i in range(len(datalist)):
    
    names = list(pd.read_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_new_1.csv", nrows=0)) + datalist
    final_list = list(OrderedDict.fromkeys(names))

    file_new = pd.read_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_new_1.csv", names=final_list, skiprows=1, na_values=['?'])
    file_new.to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_change_1.csv", encoding= "utf_8_sig", index = False)
    
    file2 = glob(path+group+"\\"+s+"\\"+number+"//"+number+"_change_1.csv")

    # res = []
    # # res.append('-')

    # for i in names:
    #     if i not in res:
    
    #         res.append(i)
    # # print(res)

    df = pd.concat(
        (pd.read_csv(file,header=0, names=final_list, usecols=datalist
                    ,dtype={'name': str, 'tweet':str}) for file in file2), sort=False, ignore_index=True)
        
    df.to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_getnum_1.csv", encoding= "utf_8_sig", index = False)


    
    files = glob(path+group+"\\"+s+"\\"+number+"//"+number+"_new_2.csv")
    
    datalist = ['3','本期淨利（淨損）Profit (loss)','營業收入合計　Total operating revenue','營業成本合計　Total operating costs']
    
    names = list(pd.read_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_new_2.csv", nrows=0)) + datalist
    final_list = list(OrderedDict.fromkeys(names))

    file_new = pd.read_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_new_2.csv", names=final_list, skiprows=1, na_values=['?'])
    file_new.to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_change_2.csv", encoding= "utf_8_sig", index = False)
    
    file2 = glob(path+group+"\\"+s+"\\"+number+"//"+number+"_change_2.csv")

    df = pd.concat(
        (pd.read_csv(file,header=0, names=final_list, usecols=datalist
                    ,dtype={'name': str, 'tweet':str}) for file in file2), sort=False, ignore_index=True)
        
    df.to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_getnum_2.csv", encoding= "utf_8_sig", index = False)



    files = glob(path+group+"\\"+s+"\\"+number+"//"+number+"_new_3.csv")

    datalist = ['3','本期稅前淨利（淨損）　Profit (loss) before tax','利息費用 Interest expense','營業活動之淨現金流入（流出）Net cash flows from (used in) operating activities']

    names = list(pd.read_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_new_3.csv", nrows=0)) + datalist
    final_list = list(OrderedDict.fromkeys(names))

    file_new = pd.read_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_new_3.csv", names=final_list, skiprows=1, na_values=['?'])
    file_new.to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_change_3.csv", encoding= "utf_8_sig", index = False)
    
    file2 = glob(path+group+"\\"+s+"\\"+number+"//"+number+"_change_3.csv")

    df = pd.concat(
        (pd.read_csv(file,header=0, names=final_list, usecols=datalist
                    ,dtype={'name': str, 'tweet':str}) for file in file2), sort=False, ignore_index=True)
        
    df.to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_getnum_3.csv", encoding= "utf_8_sig", index = False)


    
    #取得資料夾內所有資料
    files = glob(path+group+"\\"+s+"\\"+number+"//"+number+"_getnum_*.csv")

    # #串列中包含兩個Pandas DataFrame
    df_list = [pd.read_csv(file) for file in files]
    result = pd.merge(df_list[0],df_list[1], on='3')
    result = pd.merge(result,df_list[2],on='3')
    #新增股票代碼
    result["股票代碼"] = number 
    #新增股票名稱
    result["股票名稱"] = name   
    # 查詢是否已有資料夾，無資料夾則新增一個
    folder = ""+path+group+"\\"+s+"\\計算"
    if not os.path.isdir(folder):
        os.makedirs(folder)
    # #存檔
    
    result.to_csv(path+group+"\\"+s+"\\計算\\stock_"+number+".csv", encoding='utf-8-sig', index = False)
    
def csv_db(group_name,path,s):

    files = glob(path+group_name+"\\"+s+"\\計算\\stock_*.csv")
    
    df = pd.concat(
            (pd.read_csv(file,header=0, usecols=['應收帳款淨額 Accounts receivable, net','流動資產合計 Total current assets','流動負債合計 Total current liabilities',
                                                 '存貨 Current inventories','本期稅前淨利（淨損）　Profit (loss) before tax',
                                                 '營業活動之淨現金流入（流出）Net cash flows from (used in) operating activities',
                                                 '不動產、廠房及設備 Property, plant and equipment',
                                                 '資產總計　Total assets','負債總計 Total liabilities','本期淨利（淨損）Profit (loss)',
                                                 '營業收入合計　Total operating revenue','營業成本合計　Total operating costs','利息費用 Interest expense','股票代碼', '股票名稱']
                            ,dtype={'name': str, 'tweet': str}) for file in files), sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)

    df.columns = ['應收帳款淨額','存貨','流動資產合計','不動產、廠房及設備','資產總計','流動負債合計','負債總計','營業收入合計','營業成本合計',
                  '本期淨利（淨損）','本期稅前淨利（淨損）','利息費用','營業活動之淨現金流入（流出）','股票代碼','股票名稱']

    df.to_csv(path+"Sort_All\\"+group_name+"\\"+group_name+s+".csv", encoding='utf-8-sig', index = False)
    
    conn = sqlite3.connect(path + "\\DataBase\\"+group_name+"\\"+group_name+".db")
    # conn = sqlite3.connect(path + "\\DataBase\\"+group_name+"\\"+group_name+s+".db")
    
    df = pd.read_csv(path+"Sort_All\\"+group_name+"\\"+group_name+s+".csv", encoding="utf-8-sig") #, dtype='float64'

    df.to_sql("sort_"+s, conn, if_exists="replace", index=False,
    dtype={
        "本期淨利（淨損）": "float64",
        "本期稅前淨利（淨損）": "float64",
        "營業活動之淨現金流入（流出）": "float64"
    })