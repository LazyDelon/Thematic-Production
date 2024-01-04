import time
import get_data as gd

path = 'C:\\Senior Project\\資料庫\\台股\\'
group_name = '半導體業'
season = ['2019Q4', '2020Q1']

lenum = len(season)

for s in season:
    for num in range(lenum):
        if s == season[num]:
            print(s)
            slist = gd.get_stocknumber()
            cnt = len(slist)

            for i in range(cnt):
                number,name,group = slist[i]
                if group == group_name:
                    try:
                        gd.get_data(path,number,group,s)
                        gd.combine_all_data(path,number,name,group,s)
                        print(number + "\t Success")
                    except:
                        pass
            print("======================")
            gd.csv_db(group_name,path,s)

            