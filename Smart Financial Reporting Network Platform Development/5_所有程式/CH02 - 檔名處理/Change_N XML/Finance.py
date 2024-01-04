import Get_Data as gd

Seasons = [ '2015Q2' ] 

LeNum = len(Seasons)

for Season in Seasons:
    
    Path = "C:\\Senior Project\\HTML\\" + Season + "\\"
    
    for Num in range(LeNum):
        
        if Season == Seasons[Num]:
         
            print(Season)
            print("-----------------")

            gd.Rename_XML(Path)
            gd.Download_CR_XML(Path, Season)
            gd.Download_IR_XML(Path, Season)
            
# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌

# https://mops.twse.com.tw/server-java/t164sb01?t203sb01Form=t203sb01Form&step=1&CO_ID=1101&SYEAR=2015&SSEASON=1&REPORT_ID=C
# ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌       