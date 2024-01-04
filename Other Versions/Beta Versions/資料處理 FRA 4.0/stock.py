import get_data as gd
dirPath = "C:\\Users\\Chai_Chai\\Desktop\\html"  # html資料夾路徑
Path = "D:\\資料庫\\台股" # 存放csv檔案路徑
group_name = '半導體業' #選擇類別

slist = gd.get_stocknumber()
cnt = len(slist)
for i in range(cnt):
    number,name,group = slist[i]
    if group == group_name:
        gd.read_folder_saveCSV(dirPath,number,group,Path)
        gd.combine_all_data(Path,number,name,group)
        gd.csv_data(Path,number,group)
        gd.csv_all(Path,group)
        print(number + "\t Success")
gd.csv_db(Path,number,group)

