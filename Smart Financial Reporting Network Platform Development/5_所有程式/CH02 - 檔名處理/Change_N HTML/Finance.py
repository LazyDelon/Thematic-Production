import Get_Data as gd

seasons = [ '2019Q2', '2019Q3', '2019Q4',
            '2020Q1' ,'2020Q2' ,'2020Q3' ,'2020Q4', 
            '2021Q1' ,'2021Q2' ,'2021Q3' ,'2021Q4'   ]

lenum = len(seasons)

for season in seasons:

    path = 'C:\\Senior Project\\HTML\\' + season + "\\"

    for num in range(lenum):
        
        if season == seasons[num]:

            print(season)
            print("-----------------")

            try:
                gd.Change_Name(path)
            except:
                print("Fail")