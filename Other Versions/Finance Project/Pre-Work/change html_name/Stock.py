import Get_Data as gd

path = "C:\\Senior Project\\資料庫\\台股\\html\\"

season = ['2019Q1', '2019Q2', '2019Q3', '2019Q4'
        , '2020Q1', '2020Q2', '2020Q3', '2020Q4'
        , '2021Q1', '2021Q2', '2021Q3', '2021Q4']

lenum = len(season)

for s in season:
    for num in range(lenum):
        if s == season[num]:

            print(s)
            print("-----------------")

            slist = gd.get_stocknumber()

            cnt = len(slist)

            for i in range(cnt):

                number,name,group = slist[i]

                gd.change_filename_cr(path, s, number)
                gd.change_filename_ir(path, s, number)
