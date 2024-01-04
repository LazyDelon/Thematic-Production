import winsound
import Get_Data as gd


seasons = ['2016Q4', '2017Q4', '2018Q4', '2019Q4', '2020Q4', '2021Q4']

lenum = len(seasons)

for season in seasons:

    path = 'C:\\Senior Project\\HTML\\' + season + "\\"


#   ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍


seasons = [ ' ', '2015Q4', '2016Q4', '2017Q4', '2018Q4', '2019Q4', '2020Q4', '2021Q4']

lenum = len(seasons)

for season in seasons:

    path = 'C:\\Senior Project\\HTML\\' + season + "\\"

    for num in range(lenum):
        
        if season == seasons[num]:

            print(season)
            print("-----------------")

            slist = gd.Get_StockNumber()

            cnt = len(slist)
            
            for i in range(cnt):

                number, name, group = slist[i]
                
                try:
                    gd.Get_Finance(num, name, number, season, seasons)
                except:
                    pass
    print("==================")
    
# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌

# for i in range(cnt):

    # number,name,group = slist[i]
    # try:
    # gd.GetDB()
    # except:
    #     pass
# print("======================")

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌
