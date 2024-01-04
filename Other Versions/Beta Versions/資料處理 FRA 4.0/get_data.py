import pandas as pd
import os
from glob import glob
import sqlite3
import csv

def get_stocknumber():
    res = [] # 存放切割文字結果
    try:
        with open('stock_number.csv', encoding="utf-8") as f: # 開啟csv檔案
            slist = f.readlines() # 以行為單位讀取所有資料
            print('讀入：',slist) # 列印讀取資料
            for lst in slist: # 走訪每一個股票組合
                s = lst.split(',') # 以逗點切割為陣列
                # s = lst.splitlines(',') # 以逗點切割為陣列
                res.append([s[0].strip(),str(s[1].strip()),str(s[2].strip())]) # .strip去除空白，存到res陣列
    except:
        print('讀不到')
    return res
def read_folder_saveCSV(dirPath,number,group,Path):
    for i in range(0,len(os.listdir(dirPath))):
        folder = (os.listdir(dirPath)[i]) #取得陣列中的資料夾名稱
        df = pd.read_html(dirPath+"\\"+folder+"\\"+number+".html") #讀取資料夾內的檔案
        for index_num in range(0,3): #取得陣列中的資料
            file_num = str(index_num+1) #資料儲存檔名
            number_folder = Path+"\\"+folder+"\\"+group+"\\"+number+"\\" #設定資料存放路徑
            if not os.path.isdir(number_folder): #判斷資料夾是否存在
                os.makedirs(number_folder) #新增資料夾
            df[index_num].to_csv(number_folder+"\\"+number+"_"+file_num+".csv", index = False, encoding='utf_8-sig') #儲存資料
def combine_all_data(Path,number,name,group):
    for i in range(0,len(os.listdir(Path))):
        folder = (os.listdir(Path)[i]) #取得陣列中的資料夾名稱
        Path_CSV = Path+"\\"+folder+"\\" #建立資料路徑
        for x in range(1,4):
            file_num = str(x) #轉換資料型別
            df = pd.read_csv(Path_CSV+group+"\\"+number+"\\"+number+"_"+file_num+".csv", encoding= "utf_8_sig") #取得csv檔案位置
            num = (len(df.columns))+1 #取得csv表格列數
            df = df.values.tolist() #整個轉為list
            num_list = [] #設定一個空陣列，放置列數
            for i in range(1, num):
                num_list += [i]
            num_list = [str(i) for i in num_list] #將陣列從int轉str
            df = pd.DataFrame(columns = num_list, data = df)
            del num_list[1] #刪除num_list陣列的3
            del num_list[1] #刪除num_list陣列的4
            df = df.drop(num_list,axis=1)#刪除不需要的資料
            data = df.values #把 Dataframe 轉成 2D numpy array
            index1 = list(df.keys()) #找到數據的 key
            data = list(map(list, zip(*data))) #行列互換，再利用map函數將zip內的元組轉列表
            data = pd.DataFrame(data, index=index1)
            data.to_csv(Path_CSV+group+"\\"+number+"\\getfile_"+file_num+".csv",header=0, encoding= "utf_8_sig") #存檔
        files = glob(Path_CSV+group+"\\"+number+"//getfile_1.csv") #取得檔案
        df = pd.concat(
                    (pd.read_csv(file,header=0, usecols=['2','流動資產合計 Total current assets','流動負債合計 Total current liabilities',
                                                        '存貨 Current inventories',
                                                        '應收帳款淨額 Accounts receivable, net',
                                                        '不動產、廠房及設備 Property, plant and equipment',
                                                        '資產總計　Total assets','負債總計 Total liabilities']
                                    ,dtype={'name': str, 'tweet':str}) for file in files), sort=False, ignore_index=True) #抓取需要的資料
        df.to_csv(Path_CSV+group+"\\"+number+"//getfile_1.csv", encoding= "utf_8_sig", index = False) #存檔
        files = glob(Path_CSV+group+"\\"+number+"//getfile_2.csv") #取得檔案
        df = pd.concat(
                    (pd.read_csv(file,header=0, usecols=['2','營業收入合計　Total operating revenue',
                                                        '營業成本合計　Total operating costs',
                                                        '本期淨利（淨損）Profit (loss)']
                                    ,dtype={'name': str, 'tweet':str}) for file in files), sort=False, ignore_index=True) #抓取需要的資料
        df.to_csv(Path_CSV+group+"\\"+number+"//getfile_2.csv", encoding= "utf_8_sig", index = False) #存檔
        files = glob(Path_CSV+group+"\\"+number+"//getfile_3.csv") #取得檔案
        df = pd.concat(
                    (pd.read_csv(file,header=0, usecols=['2','本期稅前淨利（淨損）　Profit (loss) before tax',
                                                        '營業活動之淨現金流入（流出）Net cash flows from (used in) operating activities',
                                                        '利息費用 Interest expense']
                                    ,dtype={'name': str, 'tweet':str}) for file in files), sort=False, ignore_index=True) #抓取需要的資料
        df.to_csv(Path_CSV+group+"\\"+number+"//getfile_3.csv", encoding= "utf_8_sig", index = False) #存檔
        files = glob(Path_CSV+group+"\\"+number+"//getfile_*.csv") #取得資料夾內所有資料
        df_list = [pd.read_csv(file) for file in files] #串列中包含兩個Pandas DataFrame
        result = pd.merge(df_list[0],df_list[1], on='2') #進行資料合併
        result = pd.merge(result,df_list[2],on='2') #進行資料合併
        result["股票代碼"] = number #新增股票代碼
        result["股票名稱"] = name #新增股票名稱
        folder = ""+Path_CSV+group+"\\計算"
        if not os.path.isdir(folder): #判斷資料夾是否存在
            os.makedirs(folder) #新增資料夾
        result.to_csv(Path_CSV+group+"\\計算\\stock_"+number+".csv", encoding='utf_8-sig', index = False) #存檔
def csv_data(Path,number,group):
    for i in range(0,len(os.listdir(Path))):
        folder = (os.listdir(Path)[i]) #取得陣列中的資料夾名稱
        Path_CSV = Path+"\\"+folder+"\\" #建立資料路徑
        files = glob(Path_CSV+"\\"+group+"\\計算\\"+"stock_"+number+".csv") #取得合併的資料
        df = pd.concat(
                (pd.read_csv(file,header=0, usecols=['流動資產合計 Total current assets','流動負債合計 Total current liabilities',
                                                        '存貨 Current inventories',
                                                        '應收帳款淨額 Accounts receivable, net',
                                                        '不動產、廠房及設備 Property, plant and equipment',
                                                        '資產總計　Total assets','負債總計 Total liabilities',
                                                        '營業收入合計　Total operating revenue',
                                                        '營業成本合計　Total operating costs',
                                                        '本期稅前淨利（淨損）　Profit (loss) before tax',
                                                        '利息費用 Interest expense',
                                                        '營業活動之淨現金流入（流出）Net cash flows from (used in) operating activities',
                                                        '本期淨利（淨損）Profit (loss)',
                                                        '股票代碼', '股票名稱'] #取得資料內容
                                ,dtype={'name': str, 'tweet':str}) for file in files), sort=False, ignore_index=True)
        df.columns = ['流動資產合計','流動負債合計','存貨',
                      '應收帳款淨額','不動產、廠房及設備',
                      '資產總計','負債總計','營業收入合計',
                      '營業成本合計','本期稅前淨利','利息費用',
                      '營業活動之淨現金流入','本期淨利',
                      '股票代碼','股票名稱'] #修改資料欄位名稱
        df.to_csv(Path_CSV+"\\"+group+"\\計算\\"+"stock_"+number+".csv", encoding="utf_8-sig", index = False) #存檔
def csv_all(Path,number,group):
    for i in range(0,len(os.listdir(Path))):
        folder = (os.listdir(Path)[i]) #取得陣列中的資料夾名稱
        Path_CSV = Path+"\\"+folder+"\\" #建立資料路徑
        files = glob(Path_CSV+"\\"+group+"\\計算\\"+"stock_*.csv") #取得資料夾內名稱符合的資料
        # 合併所有資料
        df = pd.concat(
                (pd.read_csv(file, usecols=['流動資產合計','流動負債合計','存貨','應收帳款淨額','不動產、廠房及設備',
                      '資產總計','負債總計','營業收入合計','營業成本合計','本期稅前淨利','利息費用','營業活動之淨現金流入','本期淨利',
                      '股票代碼','股票名稱'], dtype={ 'name': str, 'tweet':str}) for file in files),
                ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)
        df.to_csv(Path_CSV+"\\"+group+"\\計算\\"+"stock_ALL.csv", encoding="utf_8-sig", index = False) #存檔
        df = pd.read_csv(Path_CSV+"\\"+group+"\\計算\\"+"stock_ALL.csv", encoding="utf_8-sig") #開啟已合併的資料
        df = df.drop_duplicates(subset=['存貨'], keep='first', inplace=False) #刪除重複的資料
        df.to_csv(Path_CSV+"\\"+group+"\\計算\\"+"stock_ALL_save.csv", encoding="utf_8-sig", index = False) #存檔
def csv_db(Path,group):
    for i in range(0,len(os.listdir(Path))):
        folder = (os.listdir(Path)[i]) #取得陣列中的資料夾名稱
        Path_CSV = Path+"\\"+folder+"\\" #設定資料讀取路徑
        sql_data = "D:\\Flask\\"+group+"\\"+folder+"\\" #設定資料存檔路徑
        if not os.path.isdir(sql_data): #判斷資料夾是否存在
            os.makedirs(sql_data) #新增資料夾
        conn = sqlite3.connect(sql_data+group+".db")
        df = pd.read_csv(Path_CSV+"\\"+group+"\\計算\\"+"stock_ALL_save.csv", encoding="utf_8-sig") #取得csv檔案
        df.to_sql(group, conn, if_exists="append", index=False) #存檔
            