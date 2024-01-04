import csv
import winsound
import pandas as pd
import Get_Data as gd

Stock_List = gd.Get_StockNumber()

StockLen = len(Stock_List)

for i in range(StockLen):

    Number, Name, Group = Stock_List[i]
    
    try:
        gd.Get_Finance(Number)
    except:
        print(Number + "Fail")
        pass
    
    
# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌

for i in range(StockLen):

    Number, Name, Group = Stock_List[i]

    try:
        gd.GetResult(Number)
    except:
        pass
    
print("======================")

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌
# gd.GetDB()