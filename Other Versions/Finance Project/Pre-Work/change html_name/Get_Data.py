import os
from os import walk
from os.path import join

def get_stocknumber(): # 股票代碼 / 股票名稱 / 股票類別

    res = [] # 存放切割文字結果

    try:
        with open('Stock_Number.csv', encoding="utf-8-sig") as F: # 開啟csv檔案
            
            slist = F.readlines()

            for lst in slist: # 走訪每一個股票組合
            
                s = lst.replace("\u3000", ",")
                s = s.split(',')
                
                # s = lst.splitlines(',') # 以逗點切割為陣列
                res.append([s[0].strip(),str(s[1].strip()),str(s[2].strip())]) # .strip去除空白，存到res陣列
    except:
        print('讀不到')

    return res

###################################################

def change_filename_cr(path, s, number):# -cr-為個別財務報告
    
    Path = path + "tifrs-" + s + "\\"

    for root, dirs, files in walk(Path):
       
        for i in files:

            FullPath = join(root, i) # 獲取檔案完整路徑
            FileName = join(i) # 獲取檔案名稱
            filenumber = '-cr-'+number+'-'#設定尋找的檔案名稱 -cr-合併財務報告
           
            #此檔案名稱如果在資料夾內
            if filenumber in FullPath:
                #更改檔案名稱
                os.rename(FullPath, Path+number+".html")
               

def change_filename_ir(path, s, number):# -ir-為個別財務報告
    
    Path = path + "tifrs-" + s + "\\"

    for root, dirs, files in walk(Path):

        for i in files:
            FullPath = join(root) # 獲取檔案完整路徑
            FileName = join(i) # 獲取檔案名稱
            filenumber = '-ir-'+number+'-'#設定尋找的檔案名稱 -ir-為個別財務報告
            
            #此檔案名稱如果在資料夾內
            if filenumber in FullPath:
                #確認沒有重複的檔名
                if not os.path.isfile(number+".html"):
                    #更改檔案名稱
                    os.rename(FullPath, Path+number+".html")
