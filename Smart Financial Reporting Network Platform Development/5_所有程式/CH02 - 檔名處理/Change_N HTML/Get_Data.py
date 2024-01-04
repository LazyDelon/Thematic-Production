import os

from os import walk
from glob import glob
from os.path import join


def Get_StockNumber(): 

    Results = [] 

    try:
        with open('Stock Symbol.csv', encoding="utf-8-sig") as File: 
            
            F_Read = File.readlines()

            for Stock_List in F_Read: 
            
                S = Stock_List.replace("\u3000", ",")
                S = S.split(',')

                Results.append([S[0].strip(), str(S[1].strip()), str(S[2].strip())]) 

    except:
        print('讀不到')

    return Results

########################################################################################


def Change_Name(path):

    slist = Get_StockNumber()

    cnt = len(slist)

    for root, dirs, files in walk(path):

        for file in files:
           
            FullPath = join(root, file) 

            FileName = join(file) 

            CI = '-ci-'
            BD = '-bd-'
            FH = '-fh-'
            INS = '-ins-'
            MIM = '-mim-'
            BASI = '-basi-'

            CR = '-cr-'
            IR = '-ir-'
            ER = '-er-'

            for i in range(cnt):

                number, name, group = slist[i]

                Number_List = '-' + number + '-'
    
                if CI in FileName:
                    if Number_List in FileName:

                        if ER in FileName:

                            folder = path + "CI\\ER\\"
                            if not os.path.isdir(folder):
                                os.makedirs(folder)

                            os.rename(FullPath, path + "CI\\ER\\" + number + ".html")

                        else:

                            os.rename(FullPath, path + number + ".html")

                ################################################################


                if BD in FileName:  
                    if Number_List in FileName:

                        if ER in FileName:
                            
                            folder = path + "BD\\ER\\"
                            if not os.path.isdir(folder):
                                os.makedirs(folder)

                            os.rename(FullPath, path + "BD\\ER\\" + number + ".html")

                        else:
                  
                            os.rename(FullPath, path + number + ".html")

                ################################################################


                if FH in FileName:
                    if Number_List in FileName:

                        if ER in FileName:

                            folder = path + "FH\\ER\\"
                            if not os.path.isdir(folder):
                                os.makedirs(folder)

                            os.rename(FullPath, path + "FH\\ER\\" + number + ".html")

                        else:

                            os.rename(FullPath, path + number + ".html")

                ################################################################


                if INS in FileName:
                    if Number_List in FileName:

                        if ER in FileName:

                            folder = path + "INS\\ER\\"
                            if not os.path.isdir(folder):
                                os.makedirs(folder)

                            os.rename(FullPath, path + "INS\\ER\\" + number + ".html")

                        else:

                            os.rename(FullPath, path + number + ".html")

                ################################################################


                if MIM in FileName:
                    if Number_List in FileName:
                        
                        if ER in FileName:

                            folder = path + "MIM\\ER\\"
                            if not os.path.isdir(folder):
                                os.makedirs(folder)

                            os.rename(FullPath, path + "MIM\\ER\\" + number + ".html")

                        else:

                            os.rename(FullPath, path + number + ".html")
                
                ################################################################


                if BASI in FileName:
                    if Number_List in FileName:

                        if ER in FileName:

                            folder = path + "BASI\\ER\\"
                            if not os.path.isdir(folder):
                                os.makedirs(folder)

                            os.rename(FullPath, path + "BASI\\ER\\" + number + ".html")
                
                        else:

                            os.rename(FullPath, path + number + ".html")

                ################################################################