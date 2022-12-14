import os
from datetime import datetime
import random
from random import randint
import yaml
from pathlib import Path
from getyaml import getyaml, serialise_data
parent_dir = os.getcwd()


# Use xlwings to automate data from excel 
#TO_DO Add this to a dict as TEST_DATA { USER :
#                                               1 : [{
    #                                               }]
    #                                           2 : [{
    #                                               }]      
                                    #    CARD: [{
    #                                            }]
    #                                    paths:{
    #                                               }
    # 
    #                                                   }

#Laura
# loggedcpr = '970061300'
# loggedmobile = '37463040'
# loggeddob = '1979-03-24'
# loggedname = 'laura'

# #Thomas
# loggedcpr = '910425100'
# loggedmobile = '31336369'
# loggeddob = '2009-03-20'
# loggedname = 'Thomas'

#Unknown
# loggedcpr = '910000100'
# loggedmobile = '33333349'
# loggeddob = '2009-03-20'
# loggedname = 'Unknown'

#unknownThomas
loggedcpr = '910425100'
loggedmobile = '31111300'
loggeddob = ['2009-03-10','2010-09-19','2009-03-20']
loggedname = 'Thomas'
loggedpassport = 'hiqk41922'

#davis #avenues enabled
# loggedcpr = '871275287'
# loggedmobile = '33505220'
# loggeddob = '1994-08-25'
# loggedname = 'Davis'

#
# loggedcpr = '770809195'
# # 09-08-1977
# loggedcpr = '871275287'
# loggedmobile = '33505220'
# loggeddob = '1977-08-09'
# loggedname = 'Davis'


loggeduserpin = '123321'
if isinstance(loggeddob, str):
    dob = loggeddob.rsplit("-") #['2009', '03', '20']
    bday =  dob[2]    #format dd
    bmonth =  dob[1]  #format mm
    byear =  dob[0] #format yyyy

    lastbday =  ""    #format dd
    lastbmonth =  ""  #format mm
    lastbyear =  "" #format yyyy

# optparser variable
# global force
force = True
expected = True
# variables

minimal = False

addmoneyamount = 1
addmoneyupperlimit = 3999
loggedotp = '111111'
cardnumber = "460041123"+str( randint(1000000,9999999)) # 460041<10digits>
cardholdername = "redlohdrac eman"
nofailtestcase = ["register_with_cpr",'feed_signin'] # if this fails close this test ,without running anything else
walletbal = 0 #update whenever possible
#cpr number generated to transfer money by
sendtocpr = [790241401,871275287,840160550]
selectedsendtocpr = random.choice(sendtocpr)
outputpath = os.path.join(parent_dir, "Output")
fcsv = {} #from CSV

# feedercheck ={'tc':list()} #  dict{'tc':list[{k1:v1,k2:v2},{k1:v1,k2:v2},{k1:v1,k2:v2}]}

feedercheck ={'paybywallet':list(),'addmoney':list(),'login':list()}
feedercheck['pass'] = 0
feedercheck['fail'] = 0#  dict{'tc':list[{k1:v1,k2:v2},{k1:v1,k2:v2},{k1:v1,k2:v2}]}
feederexceloutput = ''
feederhtmloutput = ''
check = {"pass" : 0 , "fail" : 0 ,"warn": 0,"w_test":[], "p_test" : [] , "f_test" : [] ,"flow" :{}}

#paths
#parent dir /app/*.apk
apkpath = os.path.join(parent_dir, 'app','app-uat.apk')
#log file path C:\Users\Administrator\Desktop\pyppium\Output\2022-09-01\log\screenshots
# logpath = "" #changed name to to session log file
# yaml path 
yamlpath = os.path.join(parent_dir,"sitemap.yaml")
serialiser,serialiserpages,serialiseractivity = serialise_data(yamlpath)
csvpath = os.path.join(parent_dir,'csvfile.csv')

# Parent Directory path
# parent_dir = os.getcwd()
yml = yaml.safe_load(Path(yamlpath).read_text())
ymlf = getyaml(yamlpath)

date = str((datetime.date(datetime.now())))
# Output folder path #pyppium/Output
path1 = outputpath #os.path.join(parent_dir, "Output")
#dated folder for current session - pyppium/Output/{date}
path2 = os.path.join(path1, date)
#screenshot folder for current session - pyppium/Output/{date}/log/screenshots
path3 = os.path.join(path2,"log","screenshots")
path4 = datapath = os.path.join(path2,"data")
excelpath = ""
userdata = ''
# global outputtime,outputdate # for logger date and time
outputdate = date
outputtime = str(datetime.now().strftime("%H-%M-%S"))
# path to create excel output
outputexcelpath = path2
expectedloginflow = ['changemobile','shufti','passport']
sessionlogfile =os.path.join(path2,"log", outputtime+'_log.txt')    


########## activities #############

dashboardactivity = "com.bfc.bfcpayments.modules.home.view.DashboardActivity"
signupactivity = "com.bfc.bfcpayments.modules.onboarding_journey.view.ui.SignUpSliderActivity"
SplashScreenActivity= "com.bfc.bfcpayments.modules.splash.view.SplashScreenActivity"
cardsactivity = 'com.bfc.bfcpayments.modules.card.CardActivity'


