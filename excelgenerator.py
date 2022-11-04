 
from datetime import datetime
import os
from random import randint, random
# import xlsxwriter
import random
from datetime import datetime
from faker import Faker
import pandas as pd
from os.path import exists
import json
 
fake = Faker()

# rand = random.randrange(20, 50, 3)
def random_cpr_and_mobile(c= "cpr",*args):
    if c == "c" or c == "cpr":
        n =9 
        end_range = 10**n-1
        r = (10**(n-1))-1
        start_range = end_range - r
        # print( randint(start_range, end_range))
        return randint(start_range, end_range)
    elif c == "mob" or c == "m":
        return randint(31000001,39999999)
    else:
        print("randomly generating a 9 digit number with 9 in strat")
        n =9 
        end_range = 10**n-1
        r = (10**(n-1))-1
        start_range = end_range - r
        # print( randint(start_range, end_range))
        return randint(start_range, end_range)  
        
        
def generator(n=1):
    # print("this is it")
    random_cpr_and_mobile("cpr")    
    data = {}
    jsondata = {}
    logindata = {}
    current_time = str(datetime.now().strftime("%H-%M-%S"))
    gender = ['MALE','FEMALE']
    addresstype = ['home','office','work','other']
    language = ['english','hindi','malayalam']
    except_nation = ["British Indian Ocean Territory (Chagos Archipelago)","Montenegro"]
    for x in range(n):
        cpr = str(random_cpr_and_mobile("cpr"))
        data[x] = {}
        jsondata[cpr] = {}
        logindata[x] = {}
        selectedgender = random.choice(gender)
        selectedlang = random.choice(language)
        print("selected gender",selectedgender)
        # write operation perform
        fake_country = fake.country(x)
        while fake_country in except_nation:
            fake_country = fake.country()
            # print ("fake_country = ",fake_country)
        if selectedgender == 'male':
            data[x]['FirstName'] =  fake.first_name_male()
            data[x]['MiddleName'] = fake.last_name_male()
            data[x]['LastName'] = fake.last_name_male()
        else:
            data[x]['FirstName'] =  fake.first_name_female()
            data[x]['MiddleName'] = fake.last_name_female()
            data[x]['LastName'] = fake.last_name_female()
            
        data[x]['Gender'] = selectedgender
        # data[x]['EmployeeCPRId'] = str(random_cpr_and_mobile("cpr"))
        data[x]['EmployeeCPRId'] = str(cpr)
        data[x]['CPRExpiryDate'] = (fake.date_between(start_date='+2y', end_date='+30y')).strftime("%m/%d/%Y")
        data[x]['MobileNumber'] = str(random_cpr_and_mobile("m"))
        data[x]['EmailId'] = fake.email()
        data[x]['PlaceOfBirth'] = fake.city()
        data[x]['DateOfBirth'] =fake.date()
        data[x]['Nationality'] = fake_country
        data[x]['PassportNumber'] = fake.bothify(text='????#####')
        # data[x]['PassportExpiry'] = (fake.future_date()).strftime("%m/%d/%Y")
        data[x]['PassportExpiry'] = (fake.date_between(start_date='+2y', end_date='+30y')).strftime("%m/%d/%Y")
        data[x]['AddressType'] = random.choice(addresstype)
        data[x]['FlatNumber'] =fake.bothify(text='????##')
        data[x]['BuildingNumber'] =fake.bothify(text='?##')
        data[x]['RoadNumber'] = fake.bothify(text='??###')
        data[x]['BlockNumber'] = fake.building_number()
        data[x]['PreferedCommunicationLanguage'] = selectedlang
        data[x]['ValidProofOfIdentification'] = 'CPR'
        data[x]['Occupation'] = fake.job()
        print("x is ",data[x])
        print("x is ",data[x]['MobileNumber'])
        # # expect,testcase,reason
        # logindata[x] = data[x]
        # logindata[x]['expect'] = None
        # logindata[x]['testcase']=None
        # logindata[x]['reason']=None
# to format this in feeder
        jsondata[data[x]['EmployeeCPRId']]['EmployeeCPRId'] = data[x]['EmployeeCPRId']
        jsondata[data[x]['EmployeeCPRId']]['FirstName'] = data[x]['FirstName']
        jsondata[data[x]['EmployeeCPRId']]['MobileNumber'] = data[x]['MobileNumber']
        jsondata[data[x]['EmployeeCPRId']]['DateOfBirth'] = data[x]['DateOfBirth']
        jsondata[data[x]['EmployeeCPRId']]['PassportNumber'] = data[x]['PassportNumber']
        jsondata[data[x]['EmployeeCPRId']]['userpin'] = '123321'
        jsondata[data[x]['EmployeeCPRId']]['Otp'] = '111111'
        jsondata[data[x]['EmployeeCPRId']]['EmailId'] = data[x]['EmailId']
        jsondata[data[x]['EmployeeCPRId']]['status'] = None
        jsondata[data[x]['EmployeeCPRId']]['expect'] = None
        jsondata[data[x]['EmployeeCPRId']]['testcase'] = None
        jsondata[data[x]['EmployeeCPRId']]['reason'] = None
    
    df = pd.DataFrame(data).transpose()
    # jsdf=  pd.DataFrame(jsondata).transpose()
    # jsonobj = jsdf.to_json() datapath
    # print("jsonobj",jsonobj)
    parent_dir = os.getcwd()
    date = str((datetime.date(datetime.now())))
    path4 = os.path.join(parent_dir,date,"data")
    path3 = os.path.join(parent_dir,date)
    print("if os.path.isdir(path4)",os.path.isdir(path4))
    print("already created date folder exists") if os.path.isdir(path3) else os.mkdir(path3) #pwd/{date}
    print("already created data folder exists") if os.path.isdir(path4) else os.mkdir(path4) #pwd/{date}/data
    #adding cpr to json
    # print(parent_dir)
    # print(path4)
    excelpath = os.path.join(path4,"excel"+current_time+".xlsx")
    print(excelpath)
# create csv
    csvpath =os.path.join(path4,"logindata"+current_time+".csv") #pwd/{date}/data/logindata{time}.csv
    df.to_csv(csvpath,index = False)
    print("CSV file created as :",csvpath)
    df.to_excel(excelpath, index=False) ##pwd/{date}/data/excel{time}.xlsx
    print("EXCEL file created as :",excelpath)
#duplicating csv,excel to ensure data stability output folder will be ignored in github
    excelpath2 = os.path.join(parent_dir,"Output",date,"data","excel"+current_time+".xlsx")
    df.to_excel(excelpath2, index=False)
    print( "duplicated excel file created in output as :",excelpath2)#pwd/Output/{date}/data/excel{time}.xlsx   
    csvpath2 = os.path.join(parent_dir,"Output",date,"data","csv"+current_time+".csv")
    df.to_csv(csvpath2,index = False)
    print("duplicated CSV file created in output as :",csvpath2)#pwd/Output/{date}/data/csv{time}.csv

    jsonpath =  os.path.join(path4,'cprjsondata'+current_time+'.json') #pwd/{date}/data
    if exists(jsonpath):
    # added time to jsom file name,now this check may be not necessary unless it is created on same time but dif day
        
        with open(jsonpath,'r+', encoding='utf-8') as jsonfile:
        # First we load existing data into a dict.
            my_data = json.load(jsonfile)
            point = len(my_data)
            formatteddata = {} 
            # start = len(my_data) # 2
            # end = len(jsondata)+start # 2
            # i = 0
            # for x in range( start , end):
            #     formatteddata[x] = jsondata[i]
            #     i+=1
            
            my_data.update(formatteddata)
            keys = my_data.keys()
            json_object = json.dumps(my_data, indent=4)
            jsonfile.seek(0)
            jsonfile.write(json_object)
            #JSON is re writing the whole file. we need find a better way.
            print("JSON file updated")
    else :
        print("file doesnot exist,creating new")
        with open(jsonpath, 'w') as f:
            print("The json file is created,adding data")
            json_object = json.dumps(jsondata, indent=4)
            print("The json object data is created")
            f.write(json_object)
            print("json is written into newly created json file")
       
#calling function here
def generatecsv():
    print("csv generator invoked")

generator(10)