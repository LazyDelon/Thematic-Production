import os
import sqlite3
import pandas as pd
from numpy import int64

from glob import glob

from sys import exec_prefix
from traceback import print_tb
from collections import OrderedDict


def get_stocknumber():
    res = [] # 存放切割文字結果
    try:
        with open('stock_number.csv', encoding="utf-8-sig") as f: # 開啟csv檔案
            # slist = f.readlines() # 以行為單位讀取所有資料
            slist = f.readlines()

            # print('讀入：',slist) # 列印讀取資料
            for lst in slist: # 走訪每一個股票組合
                s = lst.split(',') # 以逗點切割為陣列
                # s = lst.splitlines(',') # 以逗點切割為陣列
                res.append([s[0].strip(),str(s[1].strip()),str(s[2].strip())]) # .strip去除空白，存到res陣列
    except:
        print('讀不到')
    return res


def get_data(s, path, number, group):
    # try:
    df = pd.read_html(path+"\\html\\tifrs-"+s+"\\"+number+".html")#取得放置html的資料夾
    
    for index_num in range(0,3): #取得陣列中的資料

        file_num = str(index_num + 1)
        
        # 查詢是否已有資料夾，無資料夾則新增一個
        folder = path + group + "\\" + s + "\\" + number
        if not os.path.isdir(folder):
            os.makedirs(folder)
        
        df[index_num].to_csv(folder+"\\"+number+"_"+file_num+".csv", index = False, encoding='utf_8-sig')
    #     print("First_" + number + "\t Success")
    # print("-------------------")
        # #分割網頁表格分開存檔
        # df[0].to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_1.csv",header=0, encoding= "utf_8_sig")
        # df[1].to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_2.csv",header=0, encoding= "utf_8_sig")
        # df[2].to_csv(path+group+"\\"+s+"\\"+number+"//"+number+"_3.csv",header=0, encoding= "utf_8_sig")
    # except:
    #     pass


def combine_all_data(s, path, number, name, group):

    for i in range(1,4):
        
        #取得csv檔案位置
        file_num  = str(i)

        folder = path + group + "\\" + s + "\\" + number
        if not os.path.isdir(folder):
            os.makedirs(folder)

        df = pd.read_csv(folder+"\\"+number+"_"+file_num+".csv", encoding= "utf_8_sig")
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
        del num_list[1]
        del num_list[1]
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
        data.to_csv(folder+"\\"+number+"_getfile_"+file_num+".csv",header=0, encoding= "utf_8_sig")
    #     print("Second_" + number + "\t Success")
    # print("-------------------")
    

    files = glob(folder+"\\"+number+"_getfile_1.csv")

    datalist = ['2','應收帳款淨額 Accounts receivable, net','流動資產合計 Total current assets','流動負債合計 Total current liabilities',
                '存貨 Current inventories','不動產、廠房及設備 Property, plant and equipment',
                '資產總計　Total assets','負債總計 Total liabilities','權益總計 Total equity']
    
    for i in range(len(datalist)):
    
        names = list(pd.read_csv(folder+"\\"+number+"_getfile_1.csv", nrows=0)) + datalist
        final_list = list(OrderedDict.fromkeys(names))

        file_new = pd.read_csv(folder+"\\"+number+"_getfile_1.csv", names=final_list, skiprows=1, na_values=['?'])
        file_new.to_csv(folder+"\\"+number+"_getfile_1.csv", encoding= "utf_8_sig", index = False)
    
    file2 = glob(folder+"\\"+number+"_getfile_1.csv")

    # res = []
    # # res.append('-')

    # for i in names:
    #     if i not in res:
    
    #         res.append(i)
    # # print(res)

    df = pd.concat(
        (pd.read_csv(file,header=0, names=final_list, usecols=datalist
                    ,dtype={'name': str, 'tweet':str}) for file in file2), sort=False, ignore_index=True)
    
    df.to_csv(folder+"\\"+number+"_getfile_1.csv", encoding= "utf_8_sig", index = False)
    


    files = glob(folder+"\\"+number+"_getfile_2.csv")
    
    datalist = ['2','本期淨利（淨損）Profit (loss)','營業收入合計　Total operating revenue','營業成本合計　Total operating costs']
    
    names = list(pd.read_csv(folder+"\\"+number+"_getfile_2.csv", nrows=0)) + datalist
    final_list = list(OrderedDict.fromkeys(names))

    file_new = pd.read_csv(folder+"\\"+number+"_getfile_2.csv", names=final_list, skiprows=1, na_values=['?'])
    file_new.to_csv(folder+"\\"+number+"_getfile_2.csv", encoding= "utf_8_sig", index = False)
    
    file2 = glob(folder+"\\"+number+"_getfile_2.csv")

    df = pd.concat(
        (pd.read_csv(file,header=0, names=final_list, usecols=datalist
                    ,dtype={'name': str, 'tweet':str}) for file in file2), sort=False, ignore_index=True)

    df.to_csv(folder+"\\"+number+"_getfile_2.csv", encoding= "utf_8_sig", index = False)



    files = glob(folder+"\\"+number+"_getfile_3.csv")

    datalist = ['2','本期稅前淨利（淨損）　Profit (loss) before tax','利息費用 Interest expense','營業活動之淨現金流入（流出）Net cash flows from (used in) operating activities']

    names = list(pd.read_csv(folder+"\\"+number+"_getfile_3.csv", nrows=0)) + datalist
    final_list = list(OrderedDict.fromkeys(names))

    file_new = pd.read_csv(folder+"\\"+number+"_getfile_3.csv", names=final_list, skiprows=1, na_values=['?'])
    file_new.to_csv(folder+"\\"+number+"_getfile_3.csv", encoding= "utf_8_sig", index = False)
    
    file2 = glob(folder+"\\"+number+"_getfile_3.csv")

    df = pd.concat(
        (pd.read_csv(file,header=0, names=final_list, usecols=datalist
                    ,dtype={'name': str, 'tweet':str}) for file in file2), sort=False, ignore_index=True)
    
    df.to_csv(folder+"\\"+number+"_getfile_3.csv", encoding= "utf_8_sig", index = False)


    
    #取得資料夾內所有資料
    files = glob(folder+"\\"+number+"_getfile_*.csv")

    #串列中包含兩個Pandas DataFrame
    df_list = [pd.read_csv(file) for file in files]
    result = pd.merge(df_list[0],df_list[1], on='2')
    result = pd.merge(result,df_list[2],on='2')

    #新增股票代碼
    result["股票代碼"] = number 
    #新增股票名稱
    result["股票名稱"] = name   
    #新增股票分類
    result["類股"] = group
    #新增股票季別
    result["季別"] = s 
    result["判斷季別"] = s 

    # 查詢是否已有資料夾，無資料夾則新增一個
    folder = path + group + "\\" + s + "\\" + number + "\\整合\\"
    if not os.path.isdir(folder):
        os.makedirs(folder)

    result = result.fillna(0)
    result.to_csv(folder+"stock_"+number+".csv", encoding='utf-8-sig', index = False)
    # print("======================")
    # print("Three" + number + "\t Success")

 

def csv_data(s, num, season, path, number, group):
    # 查詢是否已有資料夾，無資料夾則新增一個
    folder = path + group + "\\" + s + "\\" + number + "\\整合\\"
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    files = glob(folder+"stock_"+number+".csv")

    df = pd.concat(
            (pd.read_csv(file,header=0, usecols=['應收帳款淨額 Accounts receivable, net',
                                                 '流動資產合計 Total current assets',
                                                 '流動負債合計 Total current liabilities',
                                                 '存貨 Current inventories',
                                                 '本期稅前淨利（淨損）　Profit (loss) before tax',
                                                 '營業活動之淨現金流入（流出）Net cash flows from (used in) operating activities',
                                                 '不動產、廠房及設備 Property, plant and equipment',
                                                 '資產總計　Total assets',
                                                 '負債總計 Total liabilities',
                                                 '權益總計 Total equity',
                                                 '本期淨利（淨損）Profit (loss)',
                                                 '營業收入合計　Total operating revenue',
                                                 '營業成本合計　Total operating costs',
                                                 '利息費用 Interest expense',
                                                 '股票代碼', 
                                                 '股票名稱',
                                                 '類股',
                                                 '季別',
                                                 '判斷季別'
                                                ]
                            ,dtype={'name': str, 'tweet': str}) for file in files), sort=False, ignore_index=True).replace( '[(]','-',  regex=True).replace( '[,]','',  regex=True).replace( '[)]','',  regex=True)

    df.columns = ['應收帳款淨額','存貨','流動資產合計','不動產、廠房及設備','資產總計','流動負債合計','負債總計','權益總計','營業收入合計'
                , '營業成本合計','本期淨利','本期稅前淨利','利息費用','營業活動之淨現金流入','股票代碼','股票名稱','類股','季別','判斷季別']

    # 新增計算
    df["流動比率"] = df.流動資產合計.astype(int64) / df.流動負債合計.astype(int64)
    df["流動比率"] = round(df["流動比率"]*100,2) 


    df["速動比率"] = (df.流動資產合計.astype(int64) - df.存貨.astype(int64)) / df.流動負債合計.astype(int64)
    df["速動比率"] = round(df["速動比率"]*100,2) 
    
    
    df.to_csv(folder+"stock_"+number+".csv", encoding="utf_8-sig", index = False)
    


def calculate(s, num, season, path, number, group):

    # 查詢是否已有資料夾，無資料夾則新增一個
    Path = path + group + "\\" 

    for i in range(0,len(os.listdir(Path))):

        Folder = (os.listdir(Path)[i]) 
        Path_New = Path + Folder + "\\" + number
        Data_File = pd.read_csv(Path_New + "\\整合\\stock_"+number+".csv")

        if Folder == '2019Q1' or Folder == '2020Q1' or Folder == '2021Q1':

            Income_Net1 = Data_File.本期稅前淨利.astype(int64)
            Interest_Expense1 = Data_File.利息費用.astype(int64)
        
            Income_Result = (Income_Net1 + Interest_Expense1) / Interest_Expense1

            Data_File['利息保障倍數'] = Income_Result 
            Data_File["利息保障倍數"] = round(Data_File["利息保障倍數"],2)  
            Data_File.to_csv(Path_New + "\\整合\\stock_"+number+".csv", encoding="utf_8-sig", index = False)
            

        if Folder == '2019Q2' or Folder == '2020Q2' or Folder == '2021Q2':

            Income_Net2 = Data_File.本期稅前淨利.astype(int64)
            Interest_Expense2 = Data_File.利息費用.astype(int64)

            Income_Result2 = (Income_Net2 - Income_Net1)
            Interest_Result2 = (Interest_Expense2 - Interest_Expense1)

            Income_Result = (Income_Result2 + Interest_Result2) / Interest_Result2
            
            Data_File['利息保障倍數'] = Income_Result
            Data_File["利息保障倍數"] = round(Data_File["利息保障倍數"],2)
            Data_File.to_csv(Path_New + "\\整合\\stock_"+number+".csv", encoding="utf_8-sig", index = False)


        if Folder == '2019Q3' or Folder == '2020Q3' or Folder == '2021Q3':

            Income_Net3 = Data_File.本期稅前淨利.astype(int64)
            Interest_Expense3 = Data_File.利息費用.astype(int64)

            Income_Result3 = (Income_Net3 - Income_Net2)
            Interest_Result3 = (Interest_Expense3 - Interest_Expense2)

            Income_Result = (Income_Result3 + Interest_Result3) / Interest_Result3
            
            Data_File['利息保障倍數'] = Income_Result
            Data_File["利息保障倍數"] = round(Data_File["利息保障倍數"],2)
            Data_File.to_csv(Path_New + "\\整合\\stock_"+number+".csv", encoding="utf_8-sig", index = False)


        if Folder == '2019Q4' or Folder == '2020Q4' or Folder == '2021Q4':

            Income_Net4 = Data_File.本期稅前淨利.astype(int64)
            Interest_Expense4 = Data_File.利息費用.astype(int64)

            Income_Result4 = (Income_Net4 - Income_Net3)
            Interest_Result4 = (Interest_Expense4 - Interest_Expense3)

            Income_Result = (Income_Result4 + Interest_Result4) / Interest_Result4
            
            Data_File['利息保障倍數'] = Income_Result
            Data_File["利息保障倍數"] = round(Data_File["利息保障倍數"],2)
            Data_File.to_csv(Path_New + "\\整合\\stock_"+number+".csv", encoding="utf_8-sig", index = False)

            
def get_calculate(path, number, group):

    # 查詢是否已有資料夾，無資料夾則新增一個
    Path = path + group + "\\" 

    for i in range(0,len(os.listdir(Path))):

        Folder = (os.listdir(Path)[i]) 
        Path_New = Path + Folder + "\\" + number
        Data_File = pd.read_csv(Path_New + "\\整合\\stock_"+number+".csv")


        if Folder == '2019Q1' or Folder == '2020Q1' or Folder == '2021Q1':

            Folder_1 = (os.listdir(Path)[i-1]) 
            Path_New_1 = Path + Folder_1 + "\\" + number
            Data_File_1 = pd.read_csv(Path_New_1 + "\\整合\\stock_"+number+".csv")


            # 第一季
            Folder1 = (os.listdir(Path)[i]) 
            Path_New1 = Path + Folder1 + "\\" + number
            Data_File1 = pd.read_csv(Path_New1 + "\\整合\\stock_"+number+".csv")
  

            # 資料區
            Income_Net1 = Data_File1.本期淨利.astype(int64)
            Total_Equity1 = Data_File1.權益總計.astype(int64) 
            Total_Assets1 = Data_File1.資產總計.astype(int64)
            Total_Equity_1 = Data_File_1.權益總計.astype(int64) 
            Operating_Revenue1 = Data_File1.營業收入合計.astype(int64)


            # 計算區
            Total_Equity = ((Total_Equity1 + Total_Equity_1) / 2)
            Operating_Result = (Operating_Revenue1 / Total_Assets1)
            
            Result_ROE = Income_Net1 / Total_Equity

            # 儲存區
            Data_File['ROE'] = Result_ROE
            Data_File["ROE"] = round(Data_File["ROE"]*100,2)

            Data_File['總資產週轉率'] = Operating_Result
            Data_File["總資產週轉率"] = round(Data_File["總資產週轉率"],2)

            Data_File.to_csv(Path_New + "\\整合\\stock_"+number+".csv", encoding="utf_8-sig", index = False)

        # ============================================================================

        if Folder == '2019Q2' or Folder == '2020Q2' or Folder == '2021Q2':

            # 第一季
            Folder1 = (os.listdir(Path)[i-1]) 
            Path_New1 = Path + Folder1 + "\\" + number
            Data_File1 = pd.read_csv(Path_New1 + "\\整合\\stock_"+number+".csv")
 

            # 第二季
            Folder2 = (os.listdir(Path)[i]) 
            Path_New2 = Path + Folder2 + "\\" + number
            Data_File2 = pd.read_csv(Path_New2 + "\\整合\\stock_"+number+".csv")

            
            # 資料區
            Income_Net2 = Data_File2.本期淨利.astype(int64)
            Total_Equity1 = Data_File1.權益總計.astype(int64) 
            Total_Equity2 = Data_File2.權益總計.astype(int64) 
            Total_Assets2 = Data_File2.資產總計.astype(int64)
            Operating_Revenue2 = Data_File2.營業收入合計.astype(int64)

            Total_Equity = ((Total_Equity1 + Total_Equity2) / 2)

            # 計算區
            Result_ROE = Income_Net2 / Total_Equity
            Operating_Result = (Operating_Revenue2 / Total_Assets2)

            # 儲存區
            Data_File['ROE'] = Result_ROE
            Data_File["ROE"] = round(Data_File["ROE"]*100,2)

            Data_File['總資產週轉率'] = Operating_Result
            Data_File["總資產週轉率"] = round(Data_File["總資產週轉率"],2)

            Data_File.to_csv(Path_New + "\\整合\\stock_"+number+".csv", encoding="utf_8-sig", index = False)

        # ============================================================================

        if Folder == '2019Q3' or Folder == '2020Q3' or Folder == '2021Q3':

            # 第二季
            Folder2 = (os.listdir(Path)[i-1]) 
            Path_New2 = Path + Folder2 + "\\" + number
            Data_File2 = pd.read_csv(Path_New2 + "\\整合\\stock_"+number+".csv")

            # 第三季
            Folder3 = (os.listdir(Path)[i]) 
            Path_New3 = Path + Folder3 + "\\" + number
            Data_File3 = pd.read_csv(Path_New3 + "\\整合\\stock_"+number+".csv")

   
            # 資料區
            Income_Net3 = Data_File3.本期淨利.astype(int64)
            Total_Equity2 = Data_File2.權益總計.astype(int64) 
            Total_Equity3 = Data_File3.權益總計.astype(int64) 
            Total_Assets3 = Data_File3.資產總計.astype(int64)
            Operating_Revenue3 = Data_File3.營業收入合計.astype(int64)

            Total_Equity = ((Total_Equity2 + Total_Equity3) / 2)

            # 計算區
            Result_ROE = Income_Net3 / Total_Equity
            Operating_Result = (Operating_Revenue3 / Total_Assets3)


            # 儲存區
            Data_File['ROE'] = Result_ROE
            Data_File["ROE"] = round(Data_File["ROE"]*100,2)

            Data_File['總資產週轉率'] = Operating_Result
            Data_File["總資產週轉率"] = round(Data_File["總資產週轉率"],2)

            Data_File.to_csv(Path_New + "\\整合\\stock_"+number+".csv", encoding="utf_8-sig", index = False)

        # ============================================================================

        if Folder == '2019Q4' or Folder == '2020Q4' or Folder == '2021Q4':
            
            # 第一季
            Folder1 = (os.listdir(Path)[i-3]) 
            Path_New1 = Path + Folder1 + "\\" + number
            Data_File1 = pd.read_csv(Path_New1 + "\\整合\\stock_"+number+".csv")

            Income_Net1 = Data_File1.本期淨利.astype(int64)
            Operating_Revenue1 = Data_File1.營業收入合計.astype(int64)


            # 第二季
            Folder2 = (os.listdir(Path)[i-2]) 
            Path_New2 = Path + Folder2 + "\\" + number
            Data_File2 = pd.read_csv(Path_New2 + "\\整合\\stock_"+number+".csv")

            Income_Net2 = Data_File2.本期淨利.astype(int64)
            Operating_Revenue2 = Data_File2.營業收入合計.astype(int64)


            # 第三季
            Folder3 = (os.listdir(Path)[i-1]) 
            Path_New3 = Path + Folder3 + "\\" + number
            Data_File3 = pd.read_csv(Path_New3 + "\\整合\\stock_"+number+".csv")

            Income_Net3 = Data_File3.本期淨利.astype(int64)
            Operating_Revenue3 = Data_File3.營業收入合計.astype(int64)

            
            # 資料區
            Income_Net4 = Data_File.本期淨利.astype(int64)
            Total_Equity3 = Data_File3.權益總計.astype(int64) 
            Total_Equity4 = Data_File.權益總計.astype(int64) 
            Total_Assets = Data_File.資產總計.astype(int64)
            Operating_Result = Data_File.營業收入合計.astype(int64)


            Total_Equity = ((Total_Equity3 + Total_Equity4) / 2)

            # 總計算
            Operating_Result = (Operating_Result - Operating_Revenue1 - Operating_Revenue2 - Operating_Revenue3)
            Income_Result = (Income_Net4 - Income_Net1 - Income_Net2 - Income_Net3)

            # 計算區
            OR_Result = Operating_Result / Total_Assets
            Result_ROE = Income_Result / Total_Equity

             
            # 儲存區
            Data_File['ROE'] = Result_ROE
            Data_File["ROE"] = round(Data_File["ROE"]*100,2)

            Data_File['總資產週轉率'] = OR_Result
            Data_File["總資產週轉率"] = round(Data_File["總資產週轉率"],2)

            Data_File.to_csv(Path_New + "\\整合\\stock_"+number+".csv", encoding="utf_8-sig", index = False)
            
        

def calculate_4(path, number, group):
    # 查詢是否已有資料夾，無資料夾則新增一個
    Path = path + group + "\\" 

    for i in range(0,len(os.listdir(Path))):

        Folder = (os.listdir(Path)[i]) 
        Path_New = Path + Folder + "\\" + number
        Data_File = pd.read_csv(Path_New + "\\整合\\stock_"+number+".csv")

        if Folder == '2019Q4' or Folder == '2020Q1' or Folder == '2020Q2' or Folder == '2020Q3' or Folder == '2020Q4' or Folder == '2021Q1' or Folder == '2021Q2' or Folder == '2021Q3':
            
            Folder1 = (os.listdir(Path)[i-1]) 
            Path_New1 = Path + Folder1 + "\\" + number
            Data_File1 = pd.read_csv(Path_New1 + "\\整合\\stock_"+number+".csv")
        
            ROE1 = Data_File1.ROE.astype(int64)


            Folder2 = (os.listdir(Path)[i-2]) 
            Path_New2 = Path + Folder2 + "\\" + number
            Data_File2 = pd.read_csv(Path_New2 + "\\整合\\stock_"+number+".csv")
        
            ROE2 = Data_File2.ROE.astype(int64)


            Folder3 = (os.listdir(Path)[i-3]) 
            Path_New3 = Path + Folder3 + "\\" + number
            Data_File3 = pd.read_csv(Path_New3 + "\\整合\\stock_"+number+".csv")
        
            ROE3 = Data_File3.ROE.astype(int64)

            ROE4 = Data_File.ROE.astype(int64)
            ROE_4 = (ROE1 + ROE2 + ROE3 + ROE4)

            Data_File['近四季ROE'] = ROE_4
            
        Data_File.to_csv(Path_New + "\\整合\\stock_"+number+".csv", encoding="utf_8-sig", index = False)
            

def csv_db(s, path, number, group):  # 有問題
    
    # 查詢是否已有資料夾，無資料夾則新增一個
    Path = path + group  

    for i in range(0,len(os.listdir(Path))):

        Folder = (os.listdir(Path)[i]) 
        Path_New = Path  + "\\" + Folder + "\\" + number

        Path_DB = Path + "\\DataBase\\"
        if not os.path.isdir(Path_DB):
            os.makedirs(Path_DB)
    
        conn = sqlite3.connect(path + group + "\\DataBase\\stock.db")
        # print(conn)
            
        df = pd.read_csv(Path_New + "\\整合\\stock_"+number+".csv", encoding="utf-8-sig") 
        df.to_sql("stock", conn, if_exists="append", index=False)
        # replace
        # print(df)


 