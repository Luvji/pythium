#coding: utf-8 
from distutils.command.config import config
import inspect
from itertools import count
# from this import d
import os
from time import sleep
from datetime import datetime
import traceback
import customclasses
import sys, getopt
from config import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException
from inspect import currentframe



#global variables
RED="\033[0;31m"  # <-- [0 means not bold
GREEN="\033[1;32m" 
YELLOW="\033[1;33m" # <-- [1 means bold
BLUE="\033[1;34m"
CYAN="\033[1;36m"
CRESET = '\033[0m'
PURPLE='\033[1;35m'
LIGHTGREY = '\033[1;37m'
BLUEINWHITE = '\033[;34;47m'
BLACKONWHITE ='\x1b[0;30;47m'
BLACKONRED = '\x1b[0;30;41m'
BLACKONGREEN = '\x1b[6;30;42m'
GREYONRED = '\x1b[0;30;41m'
WHITEONRED = '\x1b[1;37;41m'
assert_count = { "PASS":0,"FAIL":0 }
middlespace = " "*int(os.get_terminal_size().columns/3)
visible = 'visible'
notvisible = 'notvisible'

# these are utility functions defined for test pages. write utility or recursive function in this  

def centerofcmd(text="",pos=True):
    '''
    pos = TRue returns position only with spaces 
        false prints it with text 
    
    '''    
    if os.get_terminal_size().columns > len(text)+6:
            center = " "*int( (os.get_terminal_size().columns - len(text)/2)/2)
    else:
            center = "   "
    if pos:
            return center
    else:
            print(center+text)
    
    
def get_linenumber():
    cf = currentframe()
    print(cf.f_back.f_lineno)
    return cf.f_back.f_lineno

def color(txt = '', bg = '' ,style =''):
    '''
    txt = 'colour' | number
    bg = 'colour' | number
    type = 
    '''
    li = ['black','red','green','yellow','blue','purple','cyan','white']
    #convert to number first
    def colourvalue(val):
        try:
            float(val)
        except ValueError:
            try:
                return li.index(val.casefold())
            except ValueError: # value is '' or any other string
                return ''
        else:
            # return float(val).is_integer() deprecating float check
            return int(float(val)) #returning s
        
    if (txt == bg == style == ''):
        return 
    txt = colourvalue(txt)
    bg = colourvalue(bg)
    style = colourvalue(style)
    txt = str(txt if txt == '' else txt+30)+';'
    bg = str(bg if bg == '' else bg+40)
    style = str(style if style == '' or int(style) not in range (0,8) else style)+';'
    # code ='\x1b['+style+';'+txt+';'+bg+ 'm'
    # code ='\x1b['+style+txt+bg+ 'm'    
    code ='x1b['+style+txt+bg+ 'm'    
    print(code)
    return code

def xpath(d,xpath):
    try:
        return d.find_element_by_xpath('//android.widget.TextView[@text = "'+xpath+'"]')
    except NoSuchElementException as e:
        print(e)
        # return False
        
def p(*args, **kwargs):
    print(*args, **kwargs)
    with open( sessionlogfile ,'a+',encoding="utf-8") as file:
    
        print(*args, **kwargs, file=file) 

def check_and_hide_keyboard(d):
    try:
        if d.is_keyboard_shown():
            # to check and hide keyboard if visible.
            p("keyboard was displayed ,now hiding it.")
            d.hide_keyboard()
        else:
            print("keyboard not found")
    except Exception as e:
        print (e)
        pass
        
def save_screenshot(d, test_name):
    now = datetime.now()
    current_time = str(now.strftime("%H-%M-%S"))
    # pathoutput = "Output" 
    # # Parent Directory path
    # parent_dir = os.getcwd()
    # date = str((datetime.date(datetime.now())))
    # path1 = os.path.join(parent_dir, pathoutput)
    # path2 = os.path.join(path1, date)
    # path3 = os.path.join(path2,"screenshots")
    if ('.NexusLauncherActivity' == d.current_activity):
        print( BLACKONRED+"\n\n"+middlespace+"seems like app crashed\n\n"+CRESET)
    
    scname = os.path.join(path3,current_time+test_name)
    print(BLACKONWHITE)
    p(scname)
    path =scname+".png"
    path_II = scname+"_II.png"
    d.save_screenshot(path)
    print(BLACKONRED)
    p("screenshot taken")
    d.get_screenshot_as_file(path_II)
    # screenshotBase64.save(r"C:\Users\Administrator\Desktop\python class\Output\2022-08-04\screenshots\testfunction222.png")
    p("second screen shot taken",'\r')
    print(CRESET)

def testcasereport(testname,status,msg = "No message provided"):
    msg = "Message : "+str(msg)
    testStatus = ''
    if status in ['fail','Fail','FAIL','failed','Failed','FAILED',False]:
        testStatus = "\033[1mTEST STATUS |" + testname +"|"+RED+str(status)+CRESET
        p("="*os.get_terminal_size().columns)
        p(testStatus+" | "+msg)
        p("="*os.get_terminal_size().columns)
    elif status in ['true',True,'True','TRUE','pass','Pass','PASS','passed','Passed','PASSED']:
        testStatus = "\033[1mTEST STATUS |" + testname +"|"+GREEN+str(status)+CRESET
        p("="*os.get_terminal_size().columns)
        p(testStatus+" | "+msg)
        p("="*os.get_terminal_size().columns)
        
    else:
        testStatus = "\033[1mTEST STATUS |" + testname +"|"+YELLOW+str(status)+CRESET
        p("="*os.get_terminal_size().columns)
        p(testStatus+" | "+msg)
        p("="*os.get_terminal_size().columns)
    with open( testlogfile ,'a+',encoding="utf-8") as file:
        print('XXX XXX XXX XXX', file=file)
        
        print(testStatus+" | "+msg, file=file)

def printred(msg):
    p(" \033[;33m ")
    p(msg)
    p(" \033[0m ")

def printblue(msg):
    p("\033[0;34m")
    p(msg+"\033[0m")
def p_to_tslog(*args, **kwargs):
    
    with open( testlogfile ,'a+',encoding="utf-8") as file:
        print(*args, **kwargs, file=file)
    
    
def reportcard(check):
    now = datetime.now()
    current_time = str(now.strftime("%H-%M-%S"))
    length = os.get_terminal_size().columns-10
    p("\033[1;34;47m♠"*os.get_terminal_size().columns)
    p("-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=")
    p(":"+"_"*(length+7)+":")
    p(":           ######   ***   TEST REPORT   ***   ######")
    p("_"*length+current_time)
    p(":"+"_"*(length+7)+":")
    p("\033[0;34;47m","="*(os.get_terminal_size().columns-1))
    #passed testcases
    p("♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠")
    p("-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=PASSED")
    
    p("\033[0;32;47m")
    p( "Tests Passed :",check["pass"])
    if(check["pass"]>0):
        p("passed testcases are : \n")
        p(check["p_test"])
    else:
        p("\t"+RED+"NO TESTCASES PASSED!" +CRESET)
    p("\033[m\033[0;34;47m\n-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=")
    
    # p("==========================================================================")
    #if soft failed / warning in testcases
    if(check["warn"]>0):
        # p("==========================================================================")
        p("-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=Warn")

        
        p("\033[1;33;47m ")
        p("Tests not run /softfail/warning",check["warn"])
        if(check["warn"]>0):
            p("incompleted testcases are : \n")
            p(check["w_test"])

        p("\033[0m\033[;33;47m")
        p("="*os.get_terminal_size().columns,"\033[0m")
        # p("==========================================================================\033[0m")
    #failed test cases
    
    if(check["fail"]>0):
        p("\n \033[1;31;47m")
        p("-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=Fail")
        p("Tests Failed",check["fail"])
        if(check["fail"]>0):
            p("failed testcases are : \n")
            p(check["f_test"])
        p("")
        p("\033[0m\033[;34;47m")
        p("="*os.get_terminal_size().columns,"\033[0m")
        
        # p("==========================================================================\033[0m")
        p("")
    totassert = assert_count["PASS"]+assert_count["FAIL"]
    
    p("Total Asserts == ",totassert)
    print(CRESET)
    # centerofcmd(PURPLE+str(assert_count["FAIL"])+" /"+str(totassert)+" ASSERT(s) FAILED",False)
    # centerofcmd(CYAN+str(assert_count["PASS"])+" /"+str(totassert)+" ASSERT(s) PASSED"+CRESET,False)
    print(middlespace+PURPLE+str(assert_count["FAIL"])+" /"+str(totassert)+" ASSERT(s) FAILED")
    print(middlespace+CYAN+str(assert_count["PASS"])+" /"+str(totassert)+" ASSERT(s) PASSED"+CRESET)
    p("\033[0m")
    #########################
    #printing to testcase log
    #########################
    p_to_tslog("-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=")
    p_to_tslog(":           ######   ***   TEST REPORT   ***   ######")
    p_to_tslog("-==-=-=-==-=-=-=-==-=-=-==-=-="+current_time+"-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=")
    p_to_tslog(":Tests Passed ",check["pass"])
    if(check["pass"]>0):
        p_to_tslog("passed testcases are : \n")
        p_to_tslog(check["p_test"])
    else:
        p_to_tslog("\t"+RED+"NO TESTCASES PASSED" +CRESET)
    if(check["warn"]>0):
        # p("==========================================================================")
        p_to_tslog("-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=Warn")
        p_to_tslog("Tests not run /softfail/warning",check["warn"])
        if(check["warn"]>0):
            p_to_tslog("incompleted testcases are : \n")
            p_to_tslog(check["w_test"])
        else:
            p_to_tslog("no warnings")
        p_to_tslog("-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=Warn")
    if(check["fail"]>0):
        p_to_tslog("-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=Fail")
        p_to_tslog("Tests Failed",check["fail"])
        if(check["fail"]>0):
            p_to_tslog("failed testcases are : \n")
            p_to_tslog(check["f_test"])
        p_to_tslog("-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=-==-=-=-==-=-=-=Fail")
    p_to_tslog("Total Asserts == ",totassert)
    p_to_tslog(str(assert_count["FAIL"])+" /"+str(totassert)+" ASSERT(s) FAILED")
    p_to_tslog(str(assert_count["PASS"])+" /"+str(totassert)+" ASSERT(s) PASSED"+CRESET)

def setup_output_folder_structure():
    log = "Checking for folders and subfolders"
    print("Checking for folders and subfolders")
    try:
        if(os.path.isdir(path1) == False):
            #Output folder not found
            #creating path into 3-4 phase to not miss out any path
            log = log + "\n" + "Output folder not found - Creating..)"
            print("Output folder not found - Creating..)")
            os.mkdir(path1)
            os.mkdir(path2)
            os.makedirs(path3,exist_ok = True)
            os.mkdir(path4)
            print("Output/"+date," folder created")
        elif(os.path.isdir(path2) == False):
            os.mkdir(path2)
            os.makedirs(path3,exist_ok = True)
            os.mkdir(path4)
            
            print("Output/",date," folder created")
        elif((os.path.isdir(path3) == False) or (os.path.isdir(path4) == False)):
            if(os.path.isdir(path3) == False):
                # creating screenshot folder if not exists
                os.makedirs(path3,exist_ok = True)

                print("Output/"+date+"/screenshots"," folder created")
            else:
                print("output folder already exists")
            if(os.path.isdir(path4) == False):
                if(os.path.isdir(path4) == False):
                # creating screenshot folder if not exists
                    os.mkdir(path4)
                    print("Output/"+date+"/data"," folder created")
            else:
                print("data folder already exists")
                
        else:
            print("seems all depending output and data folders already exists")      
        print("Folder setup completed ")
    except OSError as error:
        print(error) 
        print(path1+" and its subfolder might exists")
    finally:
        # if(error is None):
        pass
 
def wait_until_activity(d,activityname,condition,sec = 15, iterate = .5):
    '''
    returns boolean
    check if current page is in activity by controlled sleep.
    d = driver(self.driver)
    activity = activity view identifier eg. com.bfc.bfcpayments.modules.splash.view.SplashScreenActivity
    condition = "visible" [wait until visible] 
                , "notvisible" [wait until not visible] 
    sec = maximum wait time 
    iterate = frequency
    '''
    curractivity = d.current_activity
    print("waiting for activity : ",activityname)
    p("\tcurrent ACTIVITY when wait_until-activity called ",curractivity)
    counter = 0
    if (condition == "visible" and activityname != ""):
        while (curractivity != activityname and counter<sec ):
            counter = counter + iterate
            sleep(iterate)
            curractivity = d.current_activity

        else:
            if (curractivity == activityname):
                p("\tactivity: "+activityname+" found waited for :"+str(counter)+" seconds")
                return True
            else:
                p(YELLOW+"\tactivity: "+activityname+" not found waited for :"+str(counter)+" seconds. curractivity is "+RED+curractivity+CRESET)
                return False
    elif (condition == "notvisible" and activityname != ""):
        while (curractivity == activityname and counter<sec ):
            counter = counter + iterate
            sleep(iterate)
            curractivity = d.current_activity

        else:
            if (curractivity != activityname):
                p(activityname+"\tnot visible."+curractivity+" is current activity.took"+str(counter)+" seconds")
                return True
            else:
                p("\t"+activityname+"still visible.that means"+curractivity+" is current activity.took"+str(counter)+" seconds")
                return False                         
# end wait_until_activity    
    
def wait_until(d,locatorstring,condition ="==",checker ="",sec = 7, iterate = .5,minimal = False,wait =  0):
    '''
    only returns bool if condition is not string check .
    used to check and wait for if a text value of a id/xpath has changed.
    
    
    d = self.driver , string = id/xpath locator ,checker = strng to compare.
    
    condition -> == waits until the value becomes equal.
                != waits until the value becomes different. 
                visible waits until it is visible.
                not visible waits until it is not visible
                ~  <default> waits until text contains checker string.  
                sec = maximum wait time , iterate = frequency.
    '''
    try:
        if wait == 0:
            d.implicitly_wait(3)
            print("wait set to 3 seconds as default")
        else:
            print("wait time passed and set to ",wait)
        
        print("waiting for ",locatorstring,condition,checker)
        if minimal:
            counter = 0
            if (condition == "==" and checker != ""):
                p("checking if the text contains text :"+checker)
                if(locatorstring.startswith("//")):
                    txtxapth = d.find_element_by_xpath(locatorstring)
                    p("xpaths = "+str(txtxapth))
                    txt = d.find_element_by_xpath(locatorstring).text
                else:            
                    txt = d.find_element_by_id(locatorstring).text
                while (txt != checker and counter<sec ):
                    counter = counter + iterate
                    sleep(iterate)
                    txt = d.find_element_by_id(locatorstring).text
                else:
                    if txt == checker and counter<=sec  :
                        p("\telement TEXT with ID/expath/ "+locatorstring+GREEN+ " found"+CRESET+". waited for :"+str(counter)+" seconds")
                        return True
                    else:
                        p("\telement TEXT with ID/expath/ "+locatorstring+ RED+" NOT found "+CRESET+". waited for :"+str(counter)+" seconds")
                        return False
                        
            elif(condition == "visible" and locatorstring.startswith("//")):
                # p("checking for element visibility")
                while (len(d.find_elements_by_xpath(locatorstring)) == 0 and counter<sec):
                    counter = counter + iterate
                    sleep(iterate)
                else:
                    if counter>=sec :
                        p("\telement with ID/xpath/ "+locatorstring+ " NOT found. waited for :"+str(counter)+" seconds")
                        return False
                    else:
                        p("\telement with ID/xpath/ "+locatorstring+ " found. waited for :"+str(counter)+" seconds")
                        return True
            
            elif(condition == "visible"):
                # p("checking for element visibility by id")
                while (len(d.find_elements_by_id(locatorstring)) == 0 and counter<sec):
                    counter = counter + iterate
                    sleep(iterate)
                else:
                    if counter>=sec :
                        p("\telement with ID/xpath/ '"+locatorstring+ "' NOT found. waited for :"+str(counter)+" seconds")
                        return False
                    else:
                        p("\telement with ID/xpath/ '"+locatorstring+ "' found. waited for :"+str(counter)+" seconds")            
                        return True
                    
                # p("#TO_DO : logic yet to be written.just sleep for 3 seconds now to ensure running")
                # p("if you are a developer please create one now")
            # condition -not visible- logic
            elif(condition == "not visible" and locatorstring.startswith("//")):
                # p("checking for element visibility")
                while (len(d.find_elements_by_xpath(locatorstring)) > 0 and counter<sec):
                    
                    counter = counter + iterate
                    sleep(iterate)
                    
                else:
                    if counter>=sec :
                        p("\telement with Xpath "+locatorstring+ " is taking longer than expected. waited for more than:"+str(counter)+" seconds")
                        return False
                    else:
                        p("\telement with Xpath "+locatorstring+ " currently not found. waited for :"+str(counter)+" seconds")
                        return True
            
            elif(condition == "not visible"):
                # p("checking for element visibility by id")
                while (len(d.find_elements_by_id(locatorstring)) > 0 and counter<sec):
                    counter = counter + iterate
                    sleep(iterate)
                else:
                    if counter>=sec :
                        p("\telement with ID  '"+locatorstring+ "' is taking longer than expected. waited for more than:"+str(counter)+" seconds")
                        return False
                    else:
                        p("\telement with ID  '"+locatorstring+ "'currently not found. waited for :"+str(counter)+" seconds")            
                        return True
            
            
            else:
                if (condition == "==" and checker == "" or condition == 'not visible'):
                    p("checker string missing, sleeping 3 for the sake of test")
                    sleep(3)
                    return False
                else:
                    p("TO_DO: wait_until != logic to be written ,please do not use it now")
                    p("if you are a developer please create one now")
                    return False
        else:
            p("checking changes -wait_until")
            
            counter = 0
            if (condition == "==" and checker != ""):
                p("checking if the text contains text :"+checker)
                if(locatorstring.startswith("//")):
                    txtxapth = d.find_element_by_xpath(locatorstring)
                    p("xpaths = "+str(txtxapth))
                    txt = d.find_element_by_xpath(locatorstring).text
                else:            
                    txt = d.find_element_by_id(locatorstring).text
                while (txt != checker and counter<sec ):
                    p("this is txt" + txt)
                    p("this is checker"+ checker)
                    counter = counter + iterate
                    sleep(iterate)
                    txt = d.find_element_by_id(locatorstring).text
                else:
                    if txt == checker and counter<=sec  :
                        p("\telement TEXT with ID/expath/ "+locatorstring+GREEN+ " found"+CRESET+". waited for :"+str(counter)+" seconds")
                        return True
                    else:
                        p("\telement TEXT with ID/expath/ "+locatorstring+ RED+" NOT found "+CRESET+". waited for :"+str(counter)+" seconds")
                        return False
                        
            elif(condition == "visible" and locatorstring.startswith("//")):
                p("checking for element visibility of locator :",locatorstring )
                while (len(d.find_elements_by_xpath(locatorstring)) == 0 and counter<sec):
                    counter = counter + iterate
                    sleep(iterate)
                else:
                    if counter>=sec :
                        p("\telement with ID/xpath/ "+locatorstring+ " NOT found. waited for :"+str(counter)+" seconds")
                        return False
                    else:
                        p("\telement with ID/xpath/ "+locatorstring+ " found. waited for :"+str(counter)+" seconds")
                        return True
            
            elif(condition == "visible"):
                p("\tchecking for element visibility by id of",locatorstring)
                while (len(d.find_elements_by_id(locatorstring)) == 0 and counter<sec):
                    counter = counter + iterate
                    sleep(iterate)
                else:
                    if counter>=sec :
                        
                        p("\telement with ID/xpath/ '"+locatorstring+ "' NOT found. waited for :"+str(counter)+" seconds")
                        return False
                    else:
                        p("\telement with ID/xpath/ '"+locatorstring+ "' found. waited for :"+str(counter)+" seconds")            
                        return True
                    
                # p("#TO_DO : logic yet to be written.just sleep for 3 seconds now to ensure running")
                # p("if you are a developer please create one now")
            elif(condition == "not visible" and locatorstring.startswith("//")):
                # p("checking for element visibility")
                print('checking for:',locatorstring)
                while (len(d.find_elements_by_xpath(locatorstring)) > 0 and counter<sec):
                    print("element drawn but is it displayed? ",d.find_elements_by_xpath(locatorstring)[0].is_displayed())
                    print("\twait until bug check:::len(d.find_elements_by_xpath(locatorstring)):",len(d.find_elements_by_xpath(locatorstring)) > 0,' length : ',len(d.find_elements_by_xpath(locatorstring)))
                    counter = counter + iterate
                    sleep(iterate)
                else:
                    if counter>=sec :
                        p("\telement with ID/xpath/ "+locatorstring+ " is taking longer than expected. waited for more than:"+str(counter)+" seconds")
                        return False
                    else:
                        p("\telement with ID/xpath/ "+locatorstring+ " currently not found. waited for :"+str(counter)+" seconds")
                        return True
            
            elif(condition == "not visible"):
                # p("checking for element visibility by id")
                while (len(d.find_elements_by_id(locatorstring)) > 0 and counter<sec):
                    counter = counter + iterate
                    sleep(iterate)
                else:
                    if counter>=sec :
                        p("\telement with ID/xpath/ '"+locatorstring+ "' is taking longer than expected. waited for more than:"+str(counter)+" seconds")
                        return False
                    else:
                        p("\telement with ID/xpath/ '"+locatorstring+ "'currently not found. waited for :"+str(counter)+" seconds")            
                        return True
            else:
                if (condition == "==" and checker == ""):
                    p("\tchecker string missing, sleeping 3 for the sake of test")
                    sleep(3)
                    return False
                else:
                    p("\tconditions not met: logic to be written ,please do not use it now")
                    p("\tif you are a developer please create one now")
                    return False
    finally:
        d.implicitly_wait(10)
            
def waitfor(d,locatorstring,s_type = "id",condition = "",sec = 15, iterate = .5):
    '''
    d = self.driver , locatorstring = id/xpath locator ,
    s_type = ["id","xpath,"text","class"]
    condition = <deprecated for now>
    sec = maximum wait time , iterate = frequency
    NB: if only check visibilty id/ or xpath : give d,locatorstring and ,s_type
    '''
    
    p("waiting for "+s_type+ " "+locatorstring)
    counter = 0 
    if s_type == "id":
        # fullstring = d.find_element_by_id(locatorstring)
        while(len(d.find_elements_by_id(locatorstring)) == 0  and counter<sec):
            
            counter = counter + iterate
            sleep(iterate)
        else:
            # p( ":: checked element with id "+locatorstring)
            # fullstring = d.find_element_by_id(locatorstring)
            
            if (counter<sec and len(d.find_elements_by_id(locatorstring))):
                p("\telement with type "+s_type+ " found. waited for :"+str(counter)+" seconds")
                return True
            else:
                p("\twaited for "+str(counter)+" seconds for "+s_type+ "to be displayed,not found")
                return False
   # below may be re writable to above liked code             
    elif s_type == "xpath":
        while(len(d.find_elements_by_xpath(locatorstring)) == 0  and counter<sec):
            counter = counter + iterate
            sleep(iterate)
        else:
            if len(d.find_elements_by_xpath(locatorstring)) == 0:
                
                fullstring = d.find_element_by_xpath(locatorstring)
                p( "\t:: checked elements = "+str(d.find_elements_by_xpath(locatorstring)))
            
            if (counter<sec):
                p("\telement with ID/expath/ "+s_type+ " found. waited for :"+str(counter)+" seconds")
                return True
            else:
                p("\twaited for "+counter+" seconds for "+s_type+ "to be displayed,xpath element not found")
                return False
                
    # elif s_type == "class":
    #     p("\tchecking element with class")
    elif condition == "text":
        p("\tchecking if the element has text to be implemented. please use wait_until_changed() instead")
        
    else:
        p("\t#TO_DO : element wise logic to be written.just sleeping for 3 seconds now to ensure running")
        p("\telements passed are :d"+d,"locatorstring"+locatorstring,"s_type = "+s_type,"condition = "+condition,"sec = "+str(sec), "iterate = "+str(iterate))
        sleep(3)
        return "not implemented"
    # p("\t")
    while(counter<sec):
        if len(d.find_elements_by_xpath(locatorstring)) == 0 and fullstring.is_displayed():
            return True
        else:
            counter = counter + iterate
            
            sleep(iterate)
    if (counter<sec):
        p("\telement with ID/expath/ "+s_type+ " could not be found. waited for :"+str(counter)+" seconds")
    else:
        p("\twaited for "+counter+" seconds for "+s_type+ "to be displayed")
   
# option parser
def opts(argv):
    # argv.py
    p(f"Name of the script      : {sys.argv[0]=}")
    p(f"Arguments of the script : {sys.argv[1:]=}")
    
def printresult(test_name ,res = False):  
      
    p("⣿"*os.get_terminal_size().columns)
    p("\033[;34m\033[47m Execution of Test :'"+test_name+"' completed..!")
    p("Test result = "+str(res) +"\033[m\033[0m")
    p("⣿"*os.get_terminal_size().columns)
        #    try:
        #       opts, args = getopt.getopt(argv,"m:n:",["minimum","no_prints"])
        #    except getopt.GetoptError:
        #       print ('test.py -i <inputfile> -o <outputfile>')
        #       sys.exit(2)
        #    for opt, arg in opts:
        #       if opt == '-m':
        #          print ('test.py -i <inputfile> -o <outputfile>')
        #          sys.exit()
        #       elif opt in ("-i", "--ifile"):
        #          inputfile = arg
        #       elif opt in ("-o", "--ofile"):
        #          outputfile = arg
        #    print ('Input file is "'), inputfile
        #    print ('Output file is "'), outputfile
    
def go_and_check_dashboardbalance(d):
    '''
    redirects to dashboard and find the wallet balance in them.
    '''
    try:
    #id com.bfccirrus.bfcpayments.mobile:id/txtAmtAvailBal
        print("fetching dashboard amt")
        if d.current_activity != dashboardactivity:
            back_to_dashboard(d)
            wait_until_activity(d,dashboardactivity,"visible")
        else:
            print("dashboard is already in view , may need a scroll up to on top")
            #ensuring top of dashboard
            # d.swipe(34, 406, 40, 700, duration=600)
        welcomeinhometxtid = "com.bfccirrus.bfcpayments.mobile:id/txtWelcome"
        if wait_until(d,welcomeinhometxtid,"visible"):
            walletbal = d.find_element(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtAmtAvailBal").text
            print("current balance is :",walletbal)
            return float(walletbal)
        else:
            print("some error occured while fetching balance, welcome text in dashboard not found")
            save_screenshot(d,'dashboardbalance_check')
    except Exception as e:
        print(e)# e
        
def back_to_dashboard(d,minimal = False,**kwargs ):
    '''
    d= self.driver
    starts activity to return to dashbard
    '''
    if minimal:
        try:
            # p("getting onto dashboard using activity\n")
            p("current activity = ",d.current_activity)
            sleep(1)
            if (d.current_activity =='MainActivity' ): #pin page:
                print("logged out of system ,  check for login acivity")
            elif(d.current_activity =='com.bfc.bfcpayments.modules.home.view.DashboardActivity'):
                print("\nAlready on Dashboard activity , returning True\n")
                return True
            elif ('.NexusLauncherActivity' == d.current_activity):
                print("seems like app crashed")
                return False
            else:
                print("not in logged activity")
            d.start_activity("com.bfccirrus.bfcpayments.mobile", "com.bfc.bfcpayments.modules.home.view.DashboardActivity")
            wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible") 
            snackbarfound ,snackbarmessage = check_snackbar(d,10)
            if snackbarfound:
                print("A message is showing in dashboard, it reads -\n",snackbarmessage)
            curractivity = d.current_activity
            if("com.bfc.bfcpayments.modules.home.view.DashboardActivity"== curractivity):
                walletbal = d.find_element(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtAmtAvailBal").text
                p("dashboard view success")
                return True
            else:
                p("dashboard not reached failed")
                return False
        except Exception as e:
            printred(e)
            printred("dashboard activity switch failed , make sure dashboard activity exported or app is logged in")
            # fail case to be written in calling method
            pass
    #normal flow
    else:
        try:
            p("getting onto dashboard using activity\n")
            p("current activity = ",d.current_activity)
            sleep(1)
            if (d.current_activity =='MainActivity' ): #pin page:
                print("logged out of system ,  check for login acivity")
            elif(d.current_activity =='com.bfc.bfcpayments.modules.home.view.DashboardActivity'):
                print("\nAlready on Dashboard activity , returning True\n")
                return True
                
            else:
                print("not in logged activity")
            d.start_activity("com.bfccirrus.bfcpayments.mobile", "com.bfc.bfcpayments.modules.home.view.DashboardActivity")
        
            p("=-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-=")
            p("=-=-=-==-=-=-=♠go back via button not implemented♠=-=-=-==-=-=-=")
            p("=-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-==-=-=-=")
            wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible") 
            curractivity = d.current_activity
            if ("com.bfc.bfcpayments.modules.signup.view.SignUpActivity"== curractivity):
                #flow changed from intention. repeating signin
                printred("some how reached signup , try continue with sign up")
                return "signup"
            elif("com.bfc.bfcpayments.modules.home.view.DashboardActivity"== curractivity):
                p("dashboard view success")
                return True
            else:
                p("dashboard nor signup not reached failed")
                return False
        except Exception as e:
            printred(e)
            printred("dashboard activity switch failed , make sure dashboard activity exported or app is logged in")
            # fail case to be written in calling method
            pass
        
# this definition flow is changed.    
# def is_project_text_present(self, text):
#         #return str(text) in self.driver.page_source
#         try:
#             project_list_test = self.driver.page_source
#         except NoSuchElementException as e:
#             return False
#         return "test001" in text # check if the project title text test001 is in the page, return true if it is

def scroll_down_to_view(d,element,start_x = 0,start_y=0 , end_x = 0,end_y = 0):
    ''' pass the locatorstring it will scroll until visible condition met
        if scrollpoint is not defined , it will consider it as a page or 
        if it has an value it is considered an element. and swipe will start from that 
        specific point.:::new app compatible:::
    '''
    #setting the points
    print("attempting scroll down")
    if start_x == 0 and start_y == 0:
        p("\tscrollpoint not defined,assuming it is a page scroll")
        start_x=28
        start_y=646
        end_x=37
        end_y=462 #small swipe up points
    else:
        p("\tscroll point defined")
    # strating to scroll
    endOfPage = False
    previousPageSource = d.page_source
    type = "id" # or xpath
    # sleep(3)
    if "//" in element:
        type = "xpath"
        if(element.startswith("//")):
            p("\telement is a direct xpath")
        try:
            if(len(d.find_elements_by_xpath(element))>0): 
                elem = d.find_element_by_xpath(element)
            else:
                p("\telement is not shown in the ui, check if the matter is of visibility")
        except NoSuchElementException as e:
            p("\telement not found but passing the exception in if")
            pass
    else:
        try:
            if(len(d.find_elements_by_id(element))>0): 
                elem = d.find_element_by_id(element)
            else:
                p("\telement is not shown in the ui ,check if the matter is of visibility")
        except NoSuchElementException as e:
            p("\telement not found but passing the except in else")
            pass
    x= 0
    while (not endOfPage):
        if type == "xpath": #xpath flow
            value = len(d.find_elements_by_xpath(element)) # list array len to check elements
            if(value>0):
                elem = d.find_element_by_xpath(element)
                if(elem.is_displayed()):
                    p("\telement is displayed")
                    break
                else:
                    p("\telement is present but not displayed")
        elif type == "id":
            value = len(d.find_elements_by_id(element)) # list array len to check elements
            if(value>0):
                elem = d.find_element_by_id(element)
                if(elem.is_displayed()):
                    p("\telement is displayed")
                    break
                else:
                    p("\telement is present but not displayed")
        p("\telement not found , scrolling "+"⢀"*x ,  end="\r")
        x=x+1
        sleep
        d.swipe(start_x, start_y, end_x, end_y, duration=300) #small swipe up
        endOfPage = previousPageSource == d.page_source #false until end of page
        previousPageSource = d.page_source
    else:
        if value>0 and elem.is_displayed():
            p("\telement found")
            return True
        else:
            p("\telement not found")
            return False
def scroll_to_top(d):
        start_x=20
        start_y=462
        end_x=20
        end_y=646
        endOfPage = False
        previousPageSource = d.page_source
        x=0
        try:
            while (not endOfPage):
                
                d.swipe(start_x, start_y,end_x, end_y, duration=600) #small swipe up
                endOfPage = previousPageSource == d.page_source #false until end of page
                previousPageSource = d.page_source
                p("\telement not found , scrolling "+"⢀"*x ,  end="\r")
                x=x+1
            print("")
        except Exception as e:
            print(e)
            pass
        
def scroll_on_element(d,element,start_x = 0,start_y=0 , end_x = 0,end_y = 0,topelement = ''):
    p("\ttrying to scroll on screen")
    endOfPage = False
    previousPageSource = d.page_source
    type = "id"
    if topelement != '':
        try:
            scroll_on_element(d,topelement, end_x, end_y,start_x, start_y)
            print("\tscrolling to top completed now scrolling to element")
            scroll_on_element(d,element,start_x ,start_y, end_x ,end_y )
        except:
            pass
    # if start_x == 0 and start_y == 0 and direction is not 'invert_first':
    #     p("\tscrollpoint not defined,assuming it is a page scroll down")
    #     start_x=28
    #     start_y=646
    #     end_x=37
    #     end_y=462 #small swipe up points
    elif start_x == 0 and start_y == 0 : #and direction is 'invert': removing extra check in case of accidental type
        print("\tscrollpoint not defined,assuming it is a page scroll ")
        start_x=37
        start_y=462
        end_x=28
        end_y=646
    else:
        p("\tscroll point defined")
        
    if "//" in element:
        type = "xpath"
        if(element.startswith("//")):
            p("\telement is a direct xpath")
        try:
            if(len(d.find_elements_by_xpath(element))>0): 
                elem = d.find_element_by_xpath(element)
            else:
                p("\t\element is not shown in the ui, check if the matter is of visibility")
        except NoSuchElementException as e:
            p("\telement not found but passing the exception in if")
            pass
    else:
        try:
            if(len(d.find_elements_by_id(element))>0): 
                elem = d.find_element_by_id(element)
            else:
                p("\telement is not shown in the ui ,check if the matter is of visibility")
        except NoSuchElementException as e:
            p("\telement not found but passing the except in else")
            pass

    x= 0
    while (not endOfPage):
        if type == "xpath": #xpath flow
            
            value = len(d.find_elements_by_xpath(element)) # list array len to check elements
            if(value>0):
                elem = d.find_element_by_xpath(element)
                if(elem.is_displayed()):
                    p("\telement is displayed")
                    break
                else:
                    p("\telement is present but not displayed")
        elif type == "id":
            value = len(d.find_elements_by_id(element)) # list array len to check elements
            if(value>0):
                elem = d.find_element_by_id(element)
                if(elem.is_displayed()):
                    p("\telement is displayed")
                    break
                else:
                    p("\telement is present but not displayed")
        p("\telement not found , scrolling "+"⢀"*x ,  end="\r")
        x=x+1
        # sleep
        d.swipe(start_x, start_y, end_x, end_y, duration=600) #small swipe up
        endOfPage = previousPageSource == d.page_source #false until end of page
        previousPageSource = d.page_source
    else:
        if value>0 and elem.is_displayed():
            p("\telement found")
            return True
        else:
            p("\telement not found")
            return False
        
# asserts and print results on given values       
def checkassert(d,element,condition = "",checker="",assertname = "assert"):
    '''
    returns boolean
    element = object - pass the value of current screen
    condition ["==" | "!=" | 'contains','not contains' #only string]
    checker = expected value
    \ncheck visiblility assert by passing element (not locator string) or condition = 'visible'
    TO_DO : pass multiple values in list and iterate for contains and not contains
    '''
    # RED="\033[0;31m"  # <-- [0 means not bold
    # GREEN="\033[1;32m" 
    # YELLOW="\033[1;33m" # <-- [1 means bold
    # CYAN="\033[1;36m"
    # CRESET = '\033[0m'
    # PURPLE='\033[1;35m'
    # BLACKONWHITE ='\x1b[0;30;47m'
    # BLACKONRED = '\x1b[0;30;41m'
    # BLACKONGREEN = '\x1b[6;30;42m'
    # GREYONRED = '\x1b[0;30;41m'
    # WHITEONRED = '\x1b[1;37;41m'
    
    elemstr = "*** Function Object ***" if element is None else str(element) # to avoid conflict in prints
    print("\telement string in checkassert",elemstr)
# == condition
    if condition == "==":
        #format first:::
        if type(element) == float or type(checker) == float:
            #float tend to check atmost precision ,so format it before hand
            element = float(element)
            checker = float(checker)
            import math
            # " float condition defers,returning using special condition"
            if math.isclose(element, checker):
                p(GREEN+" ✓ "+CRESET + " "+CYAN+elemstr[0:20]+"..."+elemstr[-20:]+" '==' "+assertname+" passed"+CRESET)
                assert_count["PASS"] += 1 
                return True
            else:
                p(RED+" ❌ "+CRESET + " "+PURPLE+elemstr[0:20]+"..."+elemstr[-20:]+" '==' "+assertname+" FAILED"+CRESET)
                p("\t\telement : "+elemstr+" != " +str(checker))
                assert_count["FAIL"] += 1                 
                return False
        elif(type(element) is bool or type(checker) is bool):
            if (type(element) is bool and type(checker) is bool):
                print("\t\tboth are boolean,checking for assert")
            else:
                elemstr,checker = (element,checker) if type(checker) is bool else (checker,element)
                # if type(elemstr)is not None and len(elemstr) > 60:
                #     p(RED+" ❌ "+CRESET + " "+PURPLE+elemstr[0:20]+"..."+elemstr[-20:]+" '==' "+assertname+" FAILED"+CRESET)
                #     p("\telement : "+elemstr+" != " +str(checker))
                #     assert_count["FAIL"] += 1                 
                #     return False
                # else:
                p(RED+" ❌ "+CRESET +" "+PURPLE+str(elemstr)+ " '==' "+assertname+" FAILED"+CRESET)
                p("\t\telement : "+str(elemstr)+" != " +str(checker))
                assert_count["FAIL"] += 1                 
                return False
 
        if element == checker:
            if len(elemstr) > 60:
                p(GREEN+" ✓ "+CRESET + " "+CYAN+elemstr[0:20]+"..."+elemstr[-20:]+" '==' "+assertname+" passed"+CRESET)
                assert_count["PASS"] += 1 
                return True
            else:
                p(GREEN+" ✓ "+CRESET +" "+CYAN+elemstr+ " '==' "+assertname+" passed"+CRESET)
                assert_count["PASS"] += 1 
                return True
        else : # element not = checker assert failed
            if len(elemstr) > 60:
                p(RED+" ❌ "+CRESET + " "+PURPLE+elemstr[0:20]+"..."+elemstr[-20:]+" '==' "+assertname+" FAILED"+CRESET)
                p("\t\telement : "+elemstr+" != " +str(checker))
                assert_count["FAIL"] += 1                 
                return False
            else:
                p(RED+" ❌ "+CRESET +" "+PURPLE+elemstr+ " '==' "+assertname+" FAILED"+CRESET)
                p("\t\telement : "+elemstr+" != " +str(checker))
                assert_count["FAIL"] += 1                 
                return False
# != condition    
    elif condition == "!=":
        # p(RED+" NOT IMPLEMENTED"+CRESET)
        checker = str(checker)
        if element != checker:
            if len(elemstr) > 60:
                p(GREEN+" ✓ "+CRESET + " "+CYAN+elemstr[0:20]+"..."+elemstr[-20:]+" '!=' "+assertname+" passed"+CRESET)
                assert_count["PASS"] += 1 
                return True
            else:
                p(GREEN+" ✓ "+CRESET +" "+CYAN+elemstr+ " '!=' "+assertname+" passed"+CRESET)
                assert_count["PASS"] += 1 
                return True
        else : # element not = checker assert failed
            if len(elemstr) > 60:
                p(RED+" ❌ "+CRESET + " "+PURPLE+elemstr[0:20]+"..."+elemstr[-20:]+" '!=' "+assertname+" FAILED"+CRESET)
                p("\t\telement : ",elemstr," != " ,checker)
                assert_count["FAIL"] += 1                 
                return False
            else:
                p(RED+" ❌ "+CRESET +" "+PURPLE+elemstr+ " '!=' "+assertname+" FAILED"+CRESET)
                p("\t\telement : "+elemstr+" != " +checker)
                assert_count["FAIL"] += 1                 
                return False
# contains condition for texts   
    elif(condition == 'contains'):
        if (isinstance(element, str) and isinstance(checker, str)):
            if checker.casefold() in element.casefold() :
                if len(elemstr) > 60:
                    p(GREEN+" ✓ "+CRESET + " "+CYAN+elemstr[0:20]+"..."+elemstr[-20:]+" 'contains' {"+checker+"} : "+assertname+" passed"+CRESET)
                    assert_count["PASS"] += 1 
                    return True
                else:
                    p(GREEN+" ✓ "+CRESET + " "+CYAN+elemstr+" 'contains' {"+checker+"} : "+assertname+" passed"+CRESET)
                    assert_count["PASS"] += 1 
                    return True
            else:    
                if len(elemstr) > 60:
                    p(RED+" ❌ "+CRESET + " "+PURPLE+elemstr[0:20]+"..."+elemstr[-20:]+" 'contains' {"+checker+"} "+assertname+" FAILED"+CRESET)
                    p("\telement : "+elemstr+" != " +checker)
                    assert_count["FAIL"] += 1                 
                    return False
                else:
                    p(RED+" ❌ "+CRESET +" "+PURPLE+elemstr+ "'contains' {"+checker+"}"+assertname+" FAILED"+CRESET)
                    p("\telement : "+elemstr+" != " +checker)
                    assert_count["FAIL"] += 1                 
                    return False
                
        
        else:
            p(RED+" ❌ either or both passed elements are not string "+CRESET)
            p("ype of element : "+type(elemstr)+" and type of checker : " +type(checker))
            assert_count["FAIL"] += 1                 
            return False
# not contains - condition for texts    
    elif(condition == 'not contains'):
        if (isinstance(element, str) and isinstance(checker, str)):
            if checker.casefold() not in element.casefold() :
                if len(elemstr) > 60:
                    p(GREEN+" ✓ "+CRESET + " "+CYAN+elemstr[0:20]+"..."+elemstr[-20:]+" 'does not contains' {"+checker+"} : "+assertname+" passed"+CRESET)
                    assert_count["PASS"] += 1 
                    return True
                else:
                    p(GREEN+" ✓ "+CRESET + " "+CYAN+elemstr+" 'does not contains' {"+checker+"} : "+assertname+" passed"+CRESET)
                    assert_count["PASS"] += 1 
                    return True
            else:    
                if len(elemstr) > 60:
                    p(RED+" ❌ "+CRESET + " "+PURPLE+elemstr[0:20]+"..."+elemstr[-20:]+" 'contains' {"+checker+"} "+assertname+" FAILED"+CRESET)
                    p("\telement : "+elemstr+" contains " +checker)
                    assert_count["FAIL"] += 1                 
                    return False
                else:
                    p(RED+" ❌ "+CRESET +" "+PURPLE+elemstr+ "'contains' {"+checker+"}"+assertname+" FAILED"+CRESET)
                    p("\telement : "+elemstr+" contains " +checker)
                    assert_count["FAIL"] += 1                 
                    return False
                
        
        else:
            p(RED+"\t ❌ either or both passed elements are not string "+CRESET)
            p("\ttype of element : "+type(elemstr)+" and type of checker : " +type(checker))
            assert_count["FAIL"] += 1                 
            return False
#visibility check without check
    elif((condition == '' or condition == 'visible' )and checker == '')  :
        #checker is checked here to ensure no mixed up of assert name and checker for visible only format
        try:
            print("\tchecking element visibility") 
            print("\t",element.get_attribute('displayed') , " for element visibility")
            # element.get_attribute('text')
            # element.get_attribute('visibility') == 'visible'  #visibility	visible
            if (element.get_attribute('displayed') or element.is_displayed()) :
                print("\telement text is ",element.get_attribute('text'))
                elemstr = element.get_attribute('text') if element.get_attribute('text') is not (None or '') else ...
                if len(elemstr) > 60:
                    p(GREEN+" ✓ "+CRESET + " "+CYAN+elemstr[0:20]+"..."+elemstr[-20:]+" ' is VISIBLE ' {"+checker+"} : "+assertname+" passed"+CRESET)
                    assert_count["PASS"] += 1 
                    return True
                else:
                    p(GREEN+" ✓ "+CRESET + " "+CYAN+elemstr+" ' Is VISIBLE' {"+checker+"} : "+assertname+" passed"+CRESET)
                    assert_count["PASS"] += 1 
                    return True
            else:
                if len(elemstr) > 60:
                    p(RED+" ❌ "+CRESET + " "+PURPLE+elemstr[0:20]+"..."+elemstr[-20:]+" ' Is NOT VISIBLE ' {"+checker+"} "+assertname+" FAILED"+CRESET)
                    p("\telement : "+elemstr+" contains " +checker)
                    assert_count["FAIL"] += 1                 
                    return False
                else:
                    p(RED+" ❌ "+CRESET +" "+PURPLE+elemstr+ "' Is NOT VISIBLE ' {"+checker+"}"+assertname+" FAILED"+CRESET)
                    p("\telement : "+elemstr+" contains " +checker)
                    assert_count["FAIL"] += 1                 
                    return False
                
                
        except Exception as e :
            p(RED +" ❌ Element not found in DOM "+CRESET)
            save_screenshot(d,"checkassert_"+assertname)
            print(e)
            # p("ype of element : "+type(elemstr)+" and type of checker : " +type(checker))
            assert_count["FAIL"] += 1                 
            return False
# catch any unfound condition
    else:
        
        p("❌ checkassert conditions not met")
        p('\tElement:',element,'\n\tcondition :',condition,'\n\tchecker :',checker,'\n\tassertname:',assertname)
                  
def callerfunction(d):
    return inspect.stack()[1].function


# def ensureentrypoint(self,expectedactivity = "",activityidentifier = ""):
#######################################################################
### this didnt worked because eval() didnt worked , find workaround ###
#######################################################################
#     ''' # implement img comparison here 
#         PASS SELF
#         expected activity : which activity are we expecting to rach , if null goes directly to 
#     '''
    
#     caller =  inspect.stack()[1].function  # function to execute
#     print("called function is ",caller)
#     print("inspect.stack()<<<<<<<<<<<<<<<<<<<<<<<<<<",inspect.stack())  
#     ymlkey_list = list(yml.keys())
#     ymlval_list = list(yml.values())
#     print("yml keys ::::::" ,ymlkey_list)
#     print("yml values :::::::",ymlval_list)
#     for module, value in yml.items():
#         print(type(value))
#         print(GREEN+" this is caller"+caller+CRESET)
#         defactivity = yml[module]['activity']
#         print(defactivity)
#         print("caller in yml[key]['events']",caller in yml[module]['events'])
#         if caller in yml[module]['events']:
#             firstdef = list(yml[module]['events'].keys())[0]
        
#             if self.driver.current_activity == dashboardactivity:
#                 eval(firstdef)(self)
#             elif self.driver.current_activity == defactivity:
#                 if activityidentifier != "":
#                     try:
#                         check = waitfor(self.driver,activityidentifier)
#                         if check:
#                             print("this should be entry point of {module} : {caller}")
#                         else:
#                             back_to_dashboard(self.driver)
#                             eval(firstdef)(self)
#                     except:
#                         back_to_dashboard(self.driver)
#                         eval(firstdef)(self)
#                 else:
#                     back_to_dashboard(self.driver)
#                     print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
#                     # eval(module+"."+firstdef)(self)
                    
#                     getattr(module+".py",firstdef)(self)
#             else:
#                 back_to_dashboard(self.driver)
#                 eval(module.firstdef)(self)
                    
#             print( module)
#             print(list(yml[module]['events'].keys())[0])
#             # print("\n\n\nLOKK ABOVE\n\n\n")
            
#             # if d.current_activity == dashboardactivity:
                
 
#     return "key doesn't exist"
 
#     # if expectedactivity:
def coordinate(size, location):
    '''
    coordinate to simulate clicking
    size = element.size
    location = element.location
    '''
    #sample code
            ##Use xpath and tap to simulate clicking

    #    def coordinate(size, location):
    #        _x_ = size.get('width')
    #        _y_ = size.get('height')
    #        x1 = location.get('x')
    #        y1 = location.get('y')
    #        x2 = x1 + _x_
    #        y2 = y1 + _y_
    #        return [(x1, y1), (x2, y2)]
           
    #    element = driver.find_element_by_xpath(xpath) #The xpath here should be replaced with the xpath information of the element
    #    elem_size = element.size
    #    elem_location = element.location
    #    bounds = coordinate(elem_size, elem_location)
    #    driver.tap(bounds, 100)
    
    _x_ = size.get('width')
    _y_ = size.get('height')
    x1 = location.get('x')
    y1 = location.get('y')
    x2 = x1 + _x_
    y2 = y1 + _y_
    return [(x1, y1), (x2, y2)]
        
def getclickfunction(d,activity):
    caller =  caller | inspect.stack()[1].function  # function to execute
    for module, value in yml.items():
        print(type(value))
        print(GREEN+" this is caller"+caller+CRESET)
        defactivity = yml[module]['activity']
        print(defactivity)
        print("caller in yml[key]['events']",caller in yml[module]['events'])
        if caller in yml[module]['events']:
            firstdef = list(yml[module]['events'].keys())[0]
            
#checks and waits for progress bar if found else returns false      
def check_and_waitforprogressbar(d , sec = 7 , iter = 1,maximum_wait_time =60):
    '''returns bool if progress bar found
    TRUE IF NOT FOUND ELSE FALSE
        waits till progress bar in visible or until time reach    
    '''
    p("waiting for progress bar")
    try:
        d.implicitly_wait(1)
        firstcounter = 0
        secondcounter = 0
        found = False
        while firstcounter < sec :
            if(len(d.find_elements_by_class_name('android.widget.ProgressBar'))>0):
                p("progress bar found in pagesource , checking for visibility")
                found = True
                break
            else:
                
                # p("progress bar NOT found in pagesource , checking ")
                p("progress bar NOT found in pagesource , checking ","⢀"*int(firstcounter),  end="\r")
                sleep(iter)
                # return False       visibility	visible  
                
            firstcounter +=iter
        sleep(1)  
        print('')
        snackbarfound,snackbartext =  check_snackbar(d,3)
        if snackbarfound:
            print("\n",YELLOW,snackbartext,CRESET,"\n")
        if firstcounter >= sec and len(d.find_elements_by_class_name('android.widget.ProgressBar'))>0:
            print(RED+"\nTOOK TOO LONG TO LOAD , THIS SHOULD NOT HAPPEN FREQUENTLY '"+str(firstcounter)+"seconds'"+CRESET)
            return False
        elif found : 
            p("checking and waiting for progress bar to disappear if visible")
            try:
                # wait = WebDriverWait(d, 8)
                # wait.until(expected_conditions.presence_of_element_located((By.ID, "productPrice")))
                # d.find_element_by_id("productPrice").is_displayed()
                pbar = d.find_element_by_class_name('android.widget.ProgressBar')
            except NoSuchElementException as e:
                print("progress loader is not visible now , check complete")
                return True
            except StaleElementReferenceException as e:
                print("Progres bar not in DOM")
                pass
            
            p("progress bar visibility = "+str(pbar.is_displayed()))
            
            try:
                while (secondcounter < maximum_wait_time) and len(d.find_elements_by_class_name('android.widget.ProgressBar'))>0:
                    if pbar.is_displayed() :
                            print("progress bar waiting to be invisible"+"."*secondcounter,end='\r')          
                            secondcounter +=iter
                            sleep(iter)
                    else:
                            # print("progress bar is not in view , waited for "+secondcounter+" seconds")
                            secondcounter +=iter
                            sleep(iter)
                else:
                    print("\n")
                    snackbarfound,snackbartext =  check_snackbar(d,3)
                    if snackbarfound:
                        print("\n",YELLOW,snackbartext,CRESET,"\n")
                                
                    if((len(d.find_elements_by_class_name('android.widget.ProgressBar'))<=0) and (secondcounter < maximum_wait_time) ):
                        print("progress bar is not in view , waited for "+str(secondcounter)+" seconds")
                        return True
                    elif (pbar.is_displayed() ) and (secondcounter >= maximum_wait_time):
                        print("maximum wait time reached ,waited for "+str(maximum_wait_time))
                        return False
                    elif(secondcounter < maximum_wait_time) and (pbar.is_displayed() is not True):
                        print("progress bar is not in view , waited for "+str(secondcounter)+" seconds")
                        ###################################
                        # TO_DO : check for snackbar
                        #####################################
                        return True
                    else:
                        print(RED+"\tERROR OCCURED IN PROGRESS BAR CHECK"+CRESET)     
                        return False     
            except NoSuchElementException as e:
                print("progress loader is not visible now , check complete")
                return True
            except StaleElementReferenceException as e:
                print("\nprogress not in DOM,success")
                return True
        
            
        else:
            print("\nprogressbar not found, waited for '"+str(firstcounter)+" seconds'")
            return False
    finally:
        d.implicitly_wait(10)
        
#check if any snackbar found when called and prints its results 
def check_snackbar(d,sec =5,iter =0.5,minimal = False):                                                                                  
    '''checks alert /snackbar , returns false if not found'''
    try:
        d.implicitly_wait(1)
        driver =d
        alertid = "com.bfccirrus.bfcpayments.mobile:id/snackbar_text"
                    #    com.bfccirrus.bfcpayments.mobile:id/snackbar_text
        checker = 0 
        while(len(driver.find_elements(By.ID,alertid))== 0 and checker < sec ):
            # print("checking for snackbar")
            #loading
            n =int(checker)
            print("checking for snackbar "+"⢀"*n,end="\r")
            # p("\telement not found , scrolling "+"⢀"*x ,  end="\r")
            
            checker = checker +iter #iterating with {iter} sleep
            # sleep(iter)
        else:
            print("\n")
            # print("alert check loop completed")
            if (len(driver.find_elements(By.ID,alertid))== 0 and checker >= sec ):  #alert not found
                # print("")
                if not minimal:
                    print("alert not found.")
                return False,""
            else:
                print("alert found , soft fail , in :",callerfunction(d))
                snackbartext =driver.find_element(By.ID,alertid).text
                save_screenshot(d,callerfunction(d))
                raise customclasses.failed(callerfunction(d),snackbartext)
    except customclasses.failed as e:
        if not minimal:
            print("alert message is : \n", e.message)
            print("in page : ",e.test_name)
        return True ,e.message
    finally :
        d.implicitly_wait(10)
        
def has_kwargs(kwargs):
    return True if int(kwargs.__len__()) != 0 else False

def exceltestreport(key,feedername = None):
    '''
    takes any dataframeable object
    creates a new excel file and writes test result to it
    '''
    import pandas as pd
    now = datetime.now()
    feedername = feedername if feedername else 'XXX'
    current_time = str(now.strftime("%H:%M:%S"))
    resultaslist = feedercheck[key]
    # below is test data
    # resultaslist =[{'name': 'Seetha Seetha', 'cpr': '993316450', 'amount': '1', 'testcase': 'pay BHD 1 to person Seetha Seetha with cpr 993316450 by wallet', 'status': True, 'reason': 'amount deducted from wallet,', 'expected': 'True', 'final_Result': 'Passed'}, {'name': 'Seetha Seetha', 'cpr': '993316454', 'amount': '5', 'testcase': 'pay BHD 5 to person Seetha Seetha with cpr 993316454 by wallet', 'status': False, 'reason': 'The Creditor Account Is In Dormant Stage', 'expected': 'True', 'final_Result': 'Failed'}, {'name': 'Seetha Seetha', 'cpr': '993316460', 'amount': '9', 'testcase': 'pay BHD 9 to person Seetha Seetha with cpr 993316460 by wallet', 'status': True, 'reason': 'amount deducted from wallet,', 'expected': 'True', 'final_Result': 'Passed'}]
    df = pd.DataFrame(resultaslist)
    df3 = pd.DataFrame(resultaslist)
    df2 =  pd.DataFrame([{"PASSED FEEDER TESTCASES":feedercheck['pass'],"FAILED FEEDER TESTCASES":feedercheck['fail']}])
    dff = pd.concat([df,df2])
    print(dff.fillna('')) # to remove nan values
    # path2 Output/{date}
    p("saving Output excel as : ",path2+'Test_Report_'+outputtime+'.xlsx')
    df.to_excel(path2+'/Test_Report_'+outputtime+'.xlsx', sheet_name='testcase'+feedername+outputtime)
######################33
#END of   exceltestreport
######################
    
def feederreport(key= '',feedername = ''):
    # global feedercheck
    print("passed key to feeder report is," ,key)
    if key == '':
        for key,value in feedercheck.items():
            
            feederreport(key,'feeder_'+key)
    # print(PURPLE+"\n\n\nfeedercheck["+key+"]::::::::",feedercheck[key])
    # print(CRESET+"\n\n\n\n EOF")
    try:
        n = len(feedercheck[key]) #length of 
    except TypeError as e:
        n= False
        pass
    # print("feederexceloutput inside feeder is enabled?",feederexceloutput)
    # print("feederhtmloutput inside feeder is enabled? ",feederhtmloutput)
    if(n):
        # for x in range(n):
            current_time = str(datetime.now().strftime("%H-%M-%S"))
            length = os.get_terminal_size().columns-10
            p("\033[1;34;47m♠"*os.get_terminal_size().columns)
            p("-==-=-=-==-=-=-="*int((os.get_terminal_size().columns)/5))
            p(":"+"_"*(length+7)+":")
            p(":           ######   *** FEEDER TEST REPORT   ***   ######")
            p("_"*length+current_time)
            p(":"+"_"*(length+7)+":")
            p("feeder captured and tested count ", n)
            p("\033[0;34;47m","="*(os.get_terminal_size().columns-1))
            #passed testcases
            print(CRESET +'\n\n')
            
            print("\033[0;34;47m PROCESSED DATA"+CRESET )
            for x in range(n):
                status = GREEN+str(feedercheck[key][x]['status'])+CRESET if feedercheck[key][x]['status'] else RED+str(feedercheck[key][x]['status'])+CRESET
                testcase = str(feedercheck[key][x]['testcase']) if feedercheck[key][x]['testcase'] != "" else 'pay BHD '+feedercheck[key][x]['amount']+ ' to person '+feedercheck[key][x]['name'] +' with cpr '+feedercheck[key][x]['cpr']+ ' by wallet'
                feedercheck[key][x]['testcase'] = testcase
                print('TC_'+str(x+1)+" Test Case : "+testcase +' ,is PASSED ? : '+ status+ '\n DATA: \n\tName -'+ feedercheck[key][x]['name'])  
                print( '\tcpr -'+feedercheck[key][x]['cpr'] )
                print( '\tamount -'+feedercheck[key][x]['amount'] )
                reasonmsg = feedercheck[key][x]['reason']
                if reasonmsg == 'message not specified' and not feedercheck[key][x]['status']: #if no msg for failed
                    reasonmsg = ' test failed and reason not available , check test case report'
                    print( '\tresult/reason -'+reasonmsg)
                elif reasonmsg == 'message not specified' and feedercheck[key][x]['status']:
                    reasonmsg = ' TEST PASSED SUCCESSFULLY'
                    print( '\tresult/reason -'+reasonmsg)
                else:
                    print( '\tresult/reason -'+reasonmsg)
            print("\n\nPASSED FEEDER TESTCASES",feedercheck['pass'])
            print("\n\nFAILED FEEDER TESTCASES",feedercheck['fail'])
            secdata = [{"PASSED FEEDER TESTCASES":feedercheck['pass'],"FAILED FEEDER TESTCASES":feedercheck['fail']}]
            print("feederexceloutput or feederhtmloutput",feederexceloutput or feederhtmloutput)
            print("feederexceloutput ",feederexceloutput ,"feederhtmloutput",feederhtmloutput)
            if feederexceloutput or feederhtmloutput:
                
                output_testresult_to_excel(feedercheck[key],feedername,secdata,[{'time':outputtime,'date':outputdate}])
            else:
                print("output print option disabled : enable it with --feederexceloutput and/or --feederhtmloutput")
    else:
        if str(n) == str(False):
            print("informational key ", key)
        else:    
            print("no feeder data found to process in key ",key)
            print(feedercheck.items())
        
        
def output_testresult_to_excel(resultaslist,feedername = '_test',*args,**kwargs):
    
    import pandas as pd
    import numpy as np
    from config import outputexcelpath
    tstamp =[{'time':outputtime,'date':outputdate}]

    excelname = '/TR'+feedername+outputtime+'.xlsx'
    excelpath = outputexcelpath+excelname
    if os.path.exists(excelpath):
        excelname = excelname+'[X].xlxs'
    df = pd.DataFrame(resultaslist)
    df.loc[len(df)] = ''#None#np.NaN   #to add empty row
    #used to format excel
    endoftestcase = df.shape  #The shape attribute of pandas.DataFrame -
    #stores the number of rows and columns as a tuple (number of rows, number of columns).
    if len(args):
        for x in args:
            li =[]
            try:
                for k in x[0].items():
                    li.append(k) #appending each to list to add this to df
            except AttributeError as e: # if not dict , throws error
                li = x
                pass
            # print('this is list\n',li if li else "no list")
            df = pd.concat([df,pd.DataFrame(li,index=[None,None])],ignore_index=False)
    #adding timestamp
    # df = pd.concat([df,pd.DataFrame(tstamp,index=[None,None])],ignore_index=False)
    df.columns = df.columns.str.upper() # change 
    df =df.fillna('')
    endoftestreport = df.shape
    # writer = pd.ExcelWriter(outputexcelpath, engine='xlsxwriter')
     
    try:
        writer = pd.ExcelWriter(excelpath, engine='xlsxwriter')
        
        # df.to_excel(writer, sheet_name='testcase'+feedername+outputtime)

    except PermissionError as e:
        #this should not be happening before we are creatng a new file
        print("SEEMS THE FILE IS ALREADY OPEN,or INACCESSIBLE,creating new file with name",outputexcelpath+outputdate+".xlsx")
        excelname = excelname+outputdate
        writer = pd.ExcelWriter(excelpath, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='testcase'+feedername+outputtime)
    # Formating the colour
    # Create a Pandas Excel writer using XlsxWriter as the engine.   
    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    # print(writer.sheets)
    worksheet = writer.sheets['testcase'+feedername+outputtime]
    
    # Add a format. Light red fill with dark red text.
    redbgformat = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})
    #c7ffcb
    greenbgformat = workbook.add_format({'bg_color': '#c7ffcb',
                               'font_color': '#009c17'})
    greybgformat = workbook.add_format({'bg_color': '#c7c9c8',
                               'font_color': '#000000'})
    # Apply a conditional format to the cell range.
    worksheet.conditional_format('I1:I1048576',
                             {'type':     'text',
                              'criteria': 'containing',
                              'value':    'Failed',
                              'format':   redbgformat})
    worksheet.conditional_format('I1:I1048576',
                             {'type':     'text',
                              'criteria': 'containing',
                              'value':    'Passed',
                              'format':   greenbgformat})
    worksheet.conditional_format(endoftestcase[0]+1,1,endoftestcase[1],endoftestreport[1],     #endoftestcase[1],endoftestreport[0],endoftestcase[1]+endoftestreport[1],
                             {'type':     'no_blanks',
                            #   'criteria': None,
                            #   'value':    'Passed',
                              'format':   greybgformat})
    worksheet.conditional_format(endoftestcase[0]+1,1,endoftestcase[1],endoftestreport[1],     #endoftestcase[1],endoftestreport[0],endoftestcase[1],endoftestreport[1],
                             {'type':     'blanks',
                            #   'criteria': None,
                            #   'value':    'Passed',
                              'format':   greybgformat})
    # worksheet.conditional_format(4,1,8,10,     #endoftestcase[1],endoftestreport[0],endoftestcase[1]+endoftestreport[1],
    #                          {'type':     'blanks',
    #                         #   'criteria': None,
    #                         #   'value':    'Passed',
    #                           'format':   greybgformat})
    #adding the df to Html
    #add cmd condition :for selecting
    if feederhtmloutput:
        dftohtml(df)
    else: 
        print(" html output disabled")
    
    # Close the Pandas Excel writer and output the Excel file.
    if feederexceloutput:
        writer.save()
        print("output file exported as ",excelname)
    else:
        print("output as excel disabled")

def dftohtml(df):
    from config import outputexcelpath
    df =df.fillna('')
    ############################33
    # html = df.to_html()
    ###################################
    html ='''
    <html>
    <head><title>HTML Pandas Dataframe with CSS</title></head>
    <style>
        .mystyle {{
            font-size: 11pt; 
            font-family: Arial;
            border-collapse: collapse; 
            border: 1px solid silver;
        }}
        .mystyle td, th {{
            padding: 5px;
        }}
        .mystyle tr:nth-child(even) {{
            background: #E0E0E0;
        }}
        .mystyle tr:hover {{
            background: silver;
            cursor: pointer;
        }}
    </style>
    
    <body>
        {table}
    </body>
    </html>.
    '''
    #<link rel="stylesheet" type="text/css" href="C:\Users\Administrator\Desktop\pyppium\df.css"/>
    # df.style.set_table_styles([{'selector': 'td', 'props': 'color:red;'}])

    with open(outputexcelpath+'/myhtml'+outputtime+'.html', 'w') as f:
        f.write(html.format(table=df.to_html(classes='mystyle')))
        print("successfully created html file report @"+outputexcelpath+'/myhtml'+outputtime+'.html')
    
##################################


def check_progressbar(d): #: , sec = 12 , iter = 1,maximum_wait_time =60):
    '''returns bool if progress bar found,includes snackbar check
    TRUE IF NOT FOUND ELSE FALSE
        waits till progress bar in visible or until time reach    
    '''
    p("waiting for progress bar")
    firstcounter = 0
    secondcounter = 0
    snackbarfound,snackbartext = "",""
    found = False

    try:
        # wait = WebDriverWait(d, 8)
        # wait.until(expected_conditions.presence_of_element_located((By.ID, "productPrice")))
        # d.find_element_by_id("productPrice").is_displayed()
        d.implicitly_wait(7)
        pbar = d.find_element_by_class_name('android.widget.ProgressBar')
        print("checking for snackbar after load")
        # print("maybe we need to check ")
        
        print(pbar)
        snackbarfound,snackbartext =  check_snackbarv2(d,3)
        if snackbarfound:
            print(YELLOW +snackbartext+ CRESET)
        
    except NoSuchElementException as e:
        d.implicitly_wait(10)
        print("progress loader is not visible now , check complete")
        return True
    except StaleElementReferenceException as e:
        d.implicitly_wait(10)
        print("Progres bar not in DOM")
        pass
    else: #trying this in case of loader takes too time idea is if those 
        check_progressbar(d)


    # if(len(d.find_elements_by_class_name('android.widget.ProgressBar'))>0):
    #     p("progress bar found in pagesource , checking for visibility")
    #     found = True
    # else:
        
    #     # p("progress bar NOT found in pagesource , checking ")
    #     p("progress bar NOT found in pagesource , checking ","⢀"*int(firstcounter),  end="\r")
    #     sleep(iter)
    #     # return False       visibility	visible  
    #     snackbarfound,snackbartext =  check_snackbar(d,3)
        
            
    #     # firstcounter +=iter
    # sleep(1)  
    # if snackbarfound:
    #     print("\n",YELLOW,snackbartext,CRESET,"\n")
    # if firstcounter >= sec and len(d.find_elements_by_class_name('android.widget.ProgressBar'))>0:
    #     print(RED+"\nTOOK TOO LONG TO LOAD , THIS SHOULD NOT HAPPEN FREQUENTLY '"+str(firstcounter)+"seconds'"+CRESET)
    #     return False
    # elif found : 
    #     p("checking and waiting for progress bar to disappear if visible")
    #     try:
    #         # wait = WebDriverWait(d, 8)
    #         # wait.until(expected_conditions.presence_of_element_located((By.ID, "productPrice")))
    #         # d.find_element_by_id("productPrice").is_displayed()
    #         pbar = d.find_element_by_class_name('android.widget.ProgressBar')
    #     except NoSuchElementException as e:
    #         print("progress loader is not visible now , check complete")
    #         return True
    #     except StaleElementReferenceException as e:
    #         print("Progres bar not in DOM")
    #         pass
        
    #     p("progress bar visibility = "+str(pbar.is_displayed()))
        
    #     try:
    #         while (secondcounter < maximum_wait_time) and len(d.find_elements_by_class_name('android.widget.ProgressBar'))>0:
    #             if pbar.is_displayed() :
    #                     print("progress bar waiting to be invisible"+"."*secondcounter,end='\r')          
    #                     secondcounter +=iter
    #                     sleep(iter)
    #             else:
    #                     # print("progress bar is not in view , waited for "+secondcounter+" seconds")
    #                     secondcounter +=iter
    #                     sleep(iter)
    #         else:
    #             print("\n")
    #             snackbarfound,snackbartext =  check_snackbar(d,3)
    #             if snackbarfound:
    #                 print("\n",YELLOW,snackbartext,CRESET,"\n")
                            
    #             if((len(d.find_elements_by_class_name('android.widget.ProgressBar'))<=0) and (secondcounter < maximum_wait_time) ):
    #                 print("progress bar is not in view , waited for "+str(secondcounter)+" seconds")
    #                 return True
    #             elif (pbar.is_displayed() ) and (secondcounter >= maximum_wait_time):
    #                 print("maximum wait time reached ,waited for "+str(maximum_wait_time))
    #                 return False
    #             elif(secondcounter < maximum_wait_time) and (pbar.is_displayed() is not True):
    #                 print("progress bar is not in view , waited for "+str(secondcounter)+" seconds")
    #                 ###################################
    #                 # TO_DO : check for snackbar
    #                 #####################################
    #                 return True
    #             else:
    #                 print(RED+"\tERROR OCCURED IN PROGRESS BAR CHECK"+CRESET)     
    #                 return False     
    #     except NoSuchElementException as e:
    #         print("progress loader is not visible now , check complete")
    #         return True
    #     except StaleElementReferenceException as e:
    #         print("\nprogress not in DOM,success")
    #         return True
     
         
    # else:
    #     print("\nprogressbar not found, waited for '"+str(firstcounter)+" seconds'")
    #     return False
  
def check_snackbarv2(d,sec =5,iter =0.5,minimal = False):                                                                                  
    '''checks alert /snackbar , returns false if not found'''
    try:
        driver =d
        alertid = "com.bfccirrus.bfcpayments.mobile:id/snackbar_text"
                    #    com.bfccirrus.bfcpayments.mobile:id/snackbar_text
        checker = 0 
        if (len(driver.find_elements(By.ID,alertid))== 0):
            print("there is no snackbar found")
            return None,None
        else:
            snackbartext =driver.find_element(By.ID,alertid).text
            print("alert found , soft fail , in :",callerfunction(d))
            save_screenshot(d,callerfunction(d))
            raise customclasses.failed(callerfunction(d),snackbartext)
    except customclasses.failed as e:
        if not minimal:
            p("alert message is :"+YELLOW+" \n\t", e.message)
            print(CRESET+"in page : ",e.test_name)
        return True ,e.message

def format_csv(csvpath):
    
    try:
        ######################## formatting csv ########################
        import csv
        from os.path import exists as file_exists
        # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
        if file_exists(csvpath):
            print("csv file exists  in \n",{csvpath})
        else:
            print(RED+"csv file does not exists  in \n",{csvpath},CRESET)
            raise  FileNotFoundError("file not found at "+csvpath+"\n\n")
            

        with open(csvpath, mode='r') as inp:
            reader = csv.reader(inp)
            header  = next(reader)
            global fcsv
            fcsv = dict()
            for row in reader:
                print("reading :",row)
                fcsv.update({row[1]: dict()})
                try:
                    for x in range(len(header)):
                        fcsv[row[1]].update({header[x]:row[x]})
                except IndexError:
                    fcsv[row[1]].update({header[x]:""})
                    continue#checking for empty values
        return fcsv
        # print(fcsv)
        ##############################################
    except FileNotFoundError as e:
        print (e)
    except Exception as e:
        print(e)








    
                    
                
            
            
        
        
        
        
        
             
            
        
        

    

             

        


    


























































































































































































































































def credits():
    print("⣿"*os.get_terminal_size().columns)
    print("⣿"*os.get_terminal_size().columns)
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣀⢀⢀⢀⢀⢀⢀⢀⠈⠙⠿⣦⡀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢰⣿⣠⡤⠖⣿⣯⣭⣝⡂⢀⢀⠈⠉⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣀⣀⣠⣤⣤⣒⡒⢀⣀⣠⣾⣟⣯⢀⠎⡿⠟⠿⣟⠉⠁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠁")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⠕⠉⠠⠤⠐⣥⡆⠾⠋⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣀⣄⣤⣶⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣱⢰⠄⠒⠬⠡⠃⡀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠤⠘⢉⣴⡾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣓⣽⣿⣿⣿⣿⣿⣿⢀⣥⣰⡗⣾⣾⡶⣥⣢⢄⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣠⣄⡀⢺⣿⣿⣽⣿⢿⣿⣿⣿⣿⣿⣿⢿⣯⣿⣯⣽⣾⣷⣿⣿⣿⣿⣿⡦⠽⣼⡿⣽⣿⣿⣿⣿⡿⣷⣶⠂⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢰⡀⢀⢀⠹⣷⢶⣿⣿⢻⡯⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠽⢿⢿⢹⢿⣿⣿⣿⣿⣿⣿⣎⣺⣟⣿⣿⣿⣿⣽⣮⣿⣿⣯⠿⡋⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠄")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢠⣸⣧⣄⢀⣸⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡭⣶⣷⠟⠍⠙⠙⢹⠼⠉⠽⡟⠃⡉⡿⣿⣿⣿⣿⣿⣿⣿⢿⢻⣮⡅⠄⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣻⣿⣿⣿⣾⢿⣿⢻⣗⡟⢿⡵⠈⢀⢀⠈⠐⢀⢀⢀⢀⢀⠰⢿⣿⣿⣿⣿⣮⣷⢍⢾⡟⠛⢻⣅⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠠⢼⢷⡑⡭⢿⣗⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣦⣿⣿⣿⣿⣾⡹⡇⢀⢀⠤⢀⢀⢀⢀⢀⢀⢀⢀⠸⡿⣿⣿⣿⣿⣿⣾⣭⣑⡄⠰⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢔⠇⢊⣿⣻⡯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡕⢝⣽⡿⣿⣿⡛⣿⣷⠙⢢⠁⢀⢀⢀⠁⠠⢀⢀⢀⢀⢀⠘⢿⣿⣿⣿⣿⣿⡺⢗⣛⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠸⡀⡮⠻⠿⣿⣽⣿⣿⣿⣿⣿⡿⢿⣽⣿⣷⣯⣾⣿⣿⣿⣷⣏⠁⢀⠈⢀⢀⢀⢀⠈⢀⢀⢀⢀⢀⢀⢀⠈⢿⣿⣿⣿⣿⣿⣻⣌⠑⠢⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⡇⢀⠆⡼⣿⣿⣿⣿⣿⣿⣿⡿⠿⢂⠺⠋⢨⡟⡭⣿⣿⣿⣿⡿⣤⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⢽⣿⣿⣷⣿⡟⡟⣓⠂⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠌⠠⣶⡽⣽⣿⣿⣿⣿⢿⣯⢲⣖⣿⣖⣶⣾⣿⣤⣕⣻⠿⣿⣷⣿⣶⡶⢀⢀⢀⢀⢀⣤⡶⢆⣤⣄⡀⢀⢀⠸⣿⣿⣾⢏⣿⠂⡁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⢀⠓⡫⣿⣯⣿⡿⠿⠏⠾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣶⣔⢯⣭⠉⢀⢀⢀⠈⢀⠈⠉⠉⠙⠛⠛⠿⢷⣐⣿⡾⡗⣇⣿⢀⠙⠁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠰⠄⡀⢀⠑⢌⣿⣻⣿⡳⠢⣞⠛⠛⠻⠝⠿⣿⡿⠻⠿⠿⡿⣿⣿⣿⣼⡊⢫⢀⢀⢀⡴⣆⣲⣤⡤⠂⣀⣀⡀⢀⢀⠁⣿⡍⢄⣽⣿⠈⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠐⡾⢅⢀⢞⣵⣽⣿⠃⢨⠃⣿⣷⣤⣠⣶⣿⣿⡷⠶⠗⠛⠊⣸⣿⣿⣿⣣⣿⣴⣦⢀⠾⢿⣾⣿⣍⢝⠣⢶⠟⠣⡐⢀⠙⢿⣮⢛⣿⢀⢀⢀⠄⢀⢀⢀⢀⢀⢀⢀⠈")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠁⢩⡰⣢⣿⣿⠇⢀⢀⠃⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣪⢟⣵⣿⠏⠉⢿⡆⢒⠈⢻⣿⣶⡀⠣⠄⠠⠸⠃⢀⢀⢀⠙⢾⣤⣠⣀⡀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠘⣼⣺⣟⡿⢀⢀⢀⢀⠈⠿⣿⣻⣿⣿⣿⣿⣿⣿⣿⢿⣫⡿⣿⣿⡾⢀⢀⠈⢧⢤⣠⠨⣛⣛⢛⣷⢄⢀⢀⢀⢀⢀⢀⢀⣄⣘⡘⠻⡃⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⡀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠠⣼⡦⢛⢆⢀⢀⢀⢀⢀⢀⠈⠛⠛⠛⠛⠛⣯⢩⠾⠛⠚⠒⠚⠉⢀⢀⢀⢀⠸⣞⣿⣿⣮⢬⣭⣰⣟⢳⣤⣄⡀⢀⠠⡈⣿⢀⢀⢀⢺⡂⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣤⣦⠈⢢⡿⠄⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢛⠂⢦⣶⠻⣿⣦⢀⢀⢀⢀⢀⢀⠹⣜⢿⣷⣷⣧⣗⣟⠿⠏⠅⢹⡿⢀⠿⠛⢀⢀⢀⠙⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢸⣯⣻⣶⣿⣌⡻⣖⢀⢀⢀⢀⢀⢀⣠⣤⣦⣡⣞⣇⢾⣝⣝⣷⠽⠆⢀⠙⠻⡇⢀⢀⠙⠮⡻⣿⣿⣿⣾⣯⡈⢀⢘⣵⣷⠝⠐⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠹⠿⣿⣿⡵⢧⣿⣉⠂⠄⠂⢀⣽⣿⣽⡉⣿⣹⡫⡻⢿⣿⠅⣰⣹⢀⢀⢀⠁⢀⢀⢀⢀⢀⠈⠉⠛⠛⠛⠉⠁⠈⠉⠁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣶")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠑⢾⣻⡲⢊⢏⠈⢀⡾⢀⢀⢾⡿⣌⣿⣿⢿⢼⣶⣶⣿⣄⢀⡉⠁⠑⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢸⣿⠗⠁⡗⠈⢀⢀⡨⢔⡿⡃⣉⣻⠎⠵⠋⠈⠉⠉⠙⠿⠿⠶⣤⣀⢀⢀⢀⣀⢀⢀⢀⢀⢀⢀⢀.;⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⠻⡉⡌⢬⣔⠶⣏⣼⡻⢷⡲⡂⢀⠈⠘⢀⠢⡀⢄⢀⢀⢀⢀⢀⠉⠳⢤⣄⡃⢀⢀⢀⢀⢀⢀⢀⠈⢀⢀⢀⢀⢀⢀⢀⢳⢀⢸⠁⢀⢀⢀⠂⢀⣀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢝⣧⣄⢉⢾⠱⢾⣷⣮⡞⠂⢀⢀⢀⢀⢀⢀⠉⢀⠊⠃⢀⢀⢀⢀⢀⢀⠃⢀⢀⢀⢀⢀⢀'⢀⢀⢀⢀⢀⢀⢀⢀⢀⠘⡄⢸⢀⢀⢀⢀⢀⡀⢀⢀⡀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⢝⢹⣮⣿⣿⣿⡞⡿⠂⡀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠩")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢢⡀⢀⣼⣧⢰⡺⣿⣿⢿⣿⣗⣗⠈⠅⡾⠆⣶⠔⡄⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⡄")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠉⠂⡸⡯⡠⣡⣹⣻⣿⡧⣮⡿⣧⡂⡞⠗⠂⣷⡆⡀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣀⢐⣄⠂⠁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⡀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣠⡶⢘⡐⢀⡗⣶⢮⢽⡥⡽⣹⠿⣿⣟⣶⣴⢎⢱⢩⣣⠈⠂⠂⣠⡈⣬⣅⣵⣶⣿⣏⣛⠿⠾⠤⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⠄⢀⢀⢀⢀⠄⢀⢰⡿⠁⠐⢢⠖⢀⠈⡶⢏⡙⠑⠑⡄⣾⣊⣿⣞⡟⢿⣤⣎⣷⣶⣿⣨⡳⣩⣿⣿⡿⠟⠛⠛⠓⠁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀")
    print("⠄⢀⢀⢀⠠⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢸⠃⠂⠰⡆⢏⡣⢀⠘⠬⠁⠈⠐⢖⠅⠘⠿⠧⡘⠨⡟⢻⣿⣿⣾⡏⣿⣞⡶⠏⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠋")
    print("⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⡇⢀⢀⢣⢀⠆⠄⢀⠁⠠⢌⣀⠂⢀⢀⢀⢀⠑⠂⠐⠁⠛⠙⠛⠁⠉⠁⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⠈⠹⡄")
    print("⣿"*os.get_terminal_size().columns)
    print("⣿"*os.get_terminal_size().columns)
    