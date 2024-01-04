import get_data as gd

path = 'C:\\Senior Project\\資料庫\\台股\\'
html_path = 'C:\\Senior Project\\資料庫\\台股\\html'
group_name = '金融保險業'
slist = gd.get_stocknumber()
cnt = len(slist)
for i in range(cnt):
    number,name,group = slist[i]
    if group == group_name:
        gd.read_folder_saveCSV(path,html_path,number,group)
        gd.combine_all_data(path,html_path,number,name,group)
        gd.csv_data(path,number,html_path,group)
        # gd.csv_db(path,html_path,number,group)
        print(number + "\t Success")

