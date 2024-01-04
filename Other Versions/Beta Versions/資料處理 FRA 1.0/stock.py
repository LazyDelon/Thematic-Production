import get_data as gd
import time
path = 'C:\\Senior Project\\資料庫\\台股\\'
group_name = '半導體業'

#for x in range(1,5):
slist = gd.get_stocknumber()
cnt = len(slist)
for i in range(cnt):
    number,name,group = slist[i]
    if group == group_name:
        gd.get_data(path,number,group)
        gd.combine_all_data(path,number,name,group)
        print(number + "\t Success")

gd.csv_db(group_name,path)


# 3686,達能,半導體業        2020.Q1有問題       應收帳款淨額 
# 5471,松翰,半導體業        2020.Q1有問題       沒利息費用
# 6515,穎崴,半導體業        2020.Q1有問題
# 5222,全訊,半導體業        2020.Q3有問題