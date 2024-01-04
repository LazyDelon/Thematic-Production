import winsound
import Get_Data as gd

seasons = ['2016Q1', '2016Q2', '2016Q3', '2016Q4',
           '2017Q1', '2017Q2', '2017Q3', '2017Q4',
           '2018Q1', '2018Q2', '2018Q3', '2018Q4',
           '2019Q1', '2019Q2', '2019Q3', '2019Q4',
           '2020Q1', '2020Q2', '2020Q3', '2020Q4',
           '2021Q1', '2021Q2', '2021Q3', '2021Q4' ]

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
                    gd.Get_Data(path, season, number)
                    print("Succesful_" + number)
                except:
                    frequency = 2000
                    duration = 1000
                    winsound.Beep(frequency, duration)

                    print("Fail_" + number)

print("==================")
        
#   ▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍▍


Stock_List = gd.Get_StockNumber()

Stock_Len = len(Stock_List)

for i in range(Stock_Len):

    Number, Name, Group = Stock_List[i]
    
    try:
        gd.Combine_Data(Number, Name, Group)
        gd.Get_CSV(Number)
        gd.Get_Result(Number, Name)                
    except:
        frequency = 2000
        duration = 1000
        winsound.Beep(frequency, duration)
        print(Number + "Fail")
 
        pass

seasons = [ '      ',
            '2015Q1', '2015Q2', '2015Q3', '2015Q4',
            '2016Q1', '2016Q2', '2016Q3', '2016Q4',
            '2017Q1', '2017Q2', '2017Q3', '2017Q4',
            '2018Q1', '2018Q2', '2018Q3', '2018Q4',
            '2019Q1', '2019Q2', '2019Q3', '2019Q4',
            '2020Q1', '2020Q2', '2020Q3', '2020Q4',
            '2021Q1', '2021Q2', '2021Q3', '2021Q4']

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

gd.Result_Nan()
    
# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌

for i in range(cnt):

    number,name,group = slist[i]
    try:
        gd.GetDB()
    except:
        pass
print("======================")

# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌
