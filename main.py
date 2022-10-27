
# from config import force
from modules import *
from util import p

# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait


alldir = dir()
print("connecting to appium server")
print("initialising connection : please wait..!")
multidef = []
nodef = []
okdef = []
testsran = 0

# print(f"Name of the script      : {sys.argv[0]=}")
print(f"Arguments of the script : {sys.argv[1:]=}")

toptions = "hnref:fe:fh"
targumentList = sys.argv[1:] 
noreset = False
no_run =False
no_fun = True
long_options = ["help","no-reset","no-run","printErrors","fun","force","feederhtmloutput","feederexceloutput","testreports"]

unrecognisedlist = []
recognised = []
for arg in sys.argv[1:] :recognised.append(arg) if arg.strip('--') in long_options else unrecognisedlist.append(arg)

print("recognised",recognised)
print("unrecognised",unrecognisedlist)


# force = False
# Long options
# long_options = ["Help", "My_file", "Output="]
print()
try:
    # Parsing argument

    arguments, values = getopt.getopt(recognised, toptions, long_options)
        
    
    # checking each argument
    for currentArgument, currentValue in arguments:
        print("checking for arguments")  
        print("currentargument= ",currentArgument,"value = ",currentValue)
        if currentArgument in ("-h", "--help"):
            print ("Displaying Help")
            print(" -n , --no-reset : will not reset last session of the app , useful to skip certain login scenarios")
            print ('"-r", "--no-run"',"testcases will not execute only evaluate")
            print("--fun","removes unwanted surprises")
            print("--force","forcefully tries to success")
            print("--feederhtmloutput : for html output\n","--feederexceloutput: for exceloutput","testreports :for both format output")
            print(" , no screenshot etc")
            no_run = True
        elif currentArgument in ("-n", "--no-reset"):
            print ("no reset turned on. App will not reset in each execution")
            noreset = True
             
        elif currentArgument in ("-r", "--no-run"):

            print (("testcases will not execute with no run option :: (% s) ::") % (currentValue))
            no_run = True
        elif currentArgument in ("-e","--printErrors"):
            print("opening file changes.txt , system will exit after print")
            print("text case run disabled")
            no_run = True
            with open('changes.txt') as file_object:
                for line in file_object:
                        print(line,"", end='')
            sys.exit("\n\nCHANGES AND ERRORS are printed IN changes.txt now exiting\n\n")
            
        elif currentArgument in ( "--fun"):
            print (("little (annoying 😅 ) surprises will be shown by option :: (% s) ::") % (currentValue))
            no_fun = False       
        elif currentArgument in ( "-f","--force"):
            print (("ENABLED FORCE , will try to heal and success forcefully. (% s) ::") % (currentValue))
            force = True
            print("force is now",force)
        elif currentArgument in ( "--feederhtmloutput"):
            print (("ENABLED feederhtmloutput  , feeder result will be save as Html (.html). (% s) ::") % (currentValue))
            
            feederhtmloutput = True

        elif currentArgument in ("--feederexceloutput "):
            print (("ENABLED feederexceloutput  , feeder result will be save as excel file(.xlsx). (% s) ::") % (currentValue))
            feederexceloutput = True
        elif currentArgument in ("--testreports"):
            print (("all testreports will be save to a file , feeder result will be save as excel file(.xlsx), and a HTML. (% s) ::") % (currentValue))
            feederexceloutput = True
            feederhtmloutput = True
                       
except getopt.error as err:
    # output error, and return with an error code
    print("Error while parsing options, Force turning on --no-run, to avoid unintentional runs")
    no_run = True
    print (str(err))
    pass
    
if( not no_fun):   
    credits()
else:
    print("⣿"*os.get_terminal_size().columns)
    print("⣿"*os.get_terminal_size().columns)
    print(middlespace,LIGHTGREY,"APPYTHON TEST STARTED",CRESET)
    print("⣿"*os.get_terminal_size().columns)
    print("⣿"*os.get_terminal_size().columns)
    


class Bfc():

        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '9.0'
        desired_caps['deviceName'] = 'pixel_2'
        desired_caps['appPackage'] = "com.bfccirrus.bfcpayments.mobile"
        desired_caps['app'] =apkpath
        desired_caps['autoGrantPermissions'] = 'true'
        # desired_caps['appActivity'] = "com.bfc.bfcpayments.modules.signup.view.SignUpActivity" #signup
        desired_caps['appActivity'] = "com.bfc.bfcpayments.modules.splash.view.SplashScreenActivity"
        desired_caps['noReset'] = noreset
        #  com.bfccirrus.bfcpayments.mobile/com.bfc.bfcpayments.modules.login.view.MainActivity
        print("desired caps",desired_caps)
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        def evaluate(self):
            try:
                setup_output_folder_structure()
                p("✓ ESSENTIAL FILES AND FOLDERS ARE CHECKED")
                with open('sitemap.yaml') as f:
                    sitemap = yaml.load_all(f, Loader=yaml.FullLoader)
                    #tqdm might not be working , check for workability , or remove the entire module
                    # for i in tqdm (range (1), desc="Loading..."):
                    for pages in sitemap:

                        for page,page_actions in pages.items():
                            eventkeys = pages[page]['events']
                            # print("event key event=",eventkeys)
                            # print("os.get_terminal_size().columns",os.get_terminal_size().columns)
                            print("_"*os.get_terminal_size().columns)
                            # print("event keys =",eventkeys)
                            # print("\n\n\n\n\n\n\nthis serialiser is the list to eval\n\n\n\n",serialiser,"\n\n\n")
                            for k, v in eventkeys.items():
                                print("\033[;34;47m Evaluating test "+k+ " from page -> "+ v+" in screen "+page+"\033[m" )
                                x = alldir.count(k)
                                if x>1:
                                    # printred("there are more than one definition named" +k)
                                    multidef.append(k)
                                elif x != 1:
                                    # printred("no definition named "+k)
                                    nodef.append(k)
                                else:
                                    #printblue("there is a definition named "+k)
                                    okdef.append(k)                                        
                    # print("_____________________________________________________________")
                    print("_"*os.get_terminal_size().columns)
                    
            except:
                print("exception occured in evaluating yaml")
                traceback.print_exc()

        def stop(self):
            p("closing test suite")
            p("="*os.get_terminal_size().columns)
            p("\n")
            self.driver.quit()    
        
        def initiate(self):
            print("total number of test to run :",okdef)
            global testsran
            print ("initiating tests , reading yaml files")
            try:
                with open('sitemap.yaml') as f:
                    sitemap = yaml.load_all(f, Loader=yaml.FullLoader)
                    for pages in sitemap:
                        print("\npages are\n")
                        print(pages,"\n")       
                                         
                        for page, page_actions in pages.items():
                            print("page :",page)
                            print("page_actions :",page_actions)
                            
                            # page = k      # contains modules pages
                            # page_actions = v   #contains url and events
                            try:
                            #     # eventlists = list(pages[page]['events'])
                            #     # print("yml ::::::::::::::::::" ,yml)
                                # print(eventlists)
                                eventkeys = pages[page]['events']
                                print("eventkeys::::::::::",eventkeys)
                            except KeyError:
                                pass
                            occurance = 0
                            for k, v in eventkeys.items():    
                                try:
                                    print("checking for target activity")
                                    targetpageactivity = pages[v]['activity']
                                    print("target actiivty",targetpageactivity)
                                    targetentry = pages[v]['entrypoint']
                                    if targetentry == 'dashboard' :
                                        print("targetactivity is in dashboard")
                                        back_to_dashboard(self.driver)
                                    elif targetentry == '' or targetentry is None:
                                        raise "missing entrypoint"
                                    else:
                                        print("Target entry point = ",targetentry)
                                        # for checkpage, check_page_actions in pages.items():
                                        #     print("")
                                        #     pages[checkpage]['events']
                                        print("retrying to get to entrypoint")
                                        back_to_dashboard(self.driver)
                                        retcheck = eval(k)(self)                                
    
                                except KeyError:
                                    if(v == 'dashboard'):
                                        p("key {v} missing in yaml , is it commented?")
                                        pass
                                    else:
                                        p("key {v} missing in yaml , is it commented?")
                                if targetpageactivity == dashboardactivity and page != "login":
                                    back_to_dashboard(self.driver)
                                elif page == "login" :
                                    print("page is before dashboard activities,go normal")
                                    print("TO_DO : write logic to implement travel through activity")
                                    
                                    print (pages[v]['activity'])

                                # print("target activity:::::::::::::::::",targetpageactivity)
                                # print ("k:::::::::::",k)
                                # print("v:::::::::::",v)
                                activity = self.driver.current_activity
                                if activity == '.NexusLauncherActivity' and occurance > 0:
                                    sleep (5)
                                print("\n\033[42mexcecuting test \033[104m" +k+ "\033[42m from page -> " + v +" ;on screen "+page+"\033[0m")
                                
                                if activity != '.NexusLauncherActivity':
                                    # normal flow.
                                    # print("\n\033[42mexcecuting test \033[104m" +k+ "\033[42m from page -> " + v +" ;next screen "+page+"\033[0m")
                                    print("test "+k+" started")
                                    print(":"*os.get_terminal_size().columns)
                                    ret = eval(k)(self)  
                                    print("this is ret",ret)
                                    testsran = testsran + 1
                                    activity = self.driver.current_activity
                                    print("ACTIVITY",activity)
                                else:
                                    print("\n\033[1;41mExecution of TEST: \033[104m"+k+"\033[1;41m Failed,from page -> "+v+" ;on screen "+page+"\033[0m")
                                    print("\033[1;41m Seems App crashed \033[0m")
                                    occurance += 1
                                    ret = False
                                if ret == True :
                                    check["pass"] = check["pass"] + 1
                                    check["p_test"].append(k)
                                elif ret == False :
                                    check["fail"] = check["fail"] + 1
                                    check["f_test"].append(k)
                                else:
                                    print("testcase return value is ",ret)
                                    check["warn"] = check["warn"] + 1
                                    check["w_test"].append(k)
                                if page == "dashboard" and self.driver.current_activity != dashboardactivity:
                                    print("rerouting to dashboard since point routes to dashboard")
                                    back_to_dashboard(self.driver)
                                    
            except Exception:
                traceback.print_exc()
                error_message = traceback.format_exc()
                print(error_message)  

        def initiate_from_formatted_serialiser(self):
            # x = 0
            occurance = 0
            testsran =0
            # self.driver.implicitly_wait(3)
            self.driver.implicitly_wait(10)
            try:
                for n in range(len(serialiser)) :
                    
                    activity = serialiseractivity[n]
                    k=serialiser[n] 
                    v = page = serialiserpages[n]
                    sleep(2)
                    if self.driver.current_activity == '.NexusLauncherActivity' and occurance > 0:
                        print("seems app is a out of app , sleeping unconditionally for 5 seconds")
                        sleep (5)
                        # print("\n\033[42mexcecuting test \033[104m" +k+ "\033[42m from page -> " + v +" ;on screen "+page+"\033[0m")
                    print("activity check = ",activity)
                    if self.driver.current_activity != '.NexusLauncherActivity':
                        # normal flow.
                        print("\n\033[42mexcecuting test \033[104m" +k+ "\033[42m from page -> " + v +" ;next screen "+page+"\033[0m")
                        print("test "+k+" started")
                        print(":"*os.get_terminal_size().columns)
     
                        # print("this is check before eval",check,"\n\n\n")
                        ret = eval(k)(self)  
                        print("this is return of formatted serialiser",ret)
                        print("checking if it is a important test case fail :", ret is not True and k in nofailtestcase)
                        if ret is not True and k in nofailtestcase:
                            p(RED+":"*os.get_terminal_size().columns)
                            p(RED+"this TESTCASE is marked as important, and should never FAILED,")
                            p(RED+":"*os.get_terminal_size().columns)
                            p(CRESET)
                            break
                            # self.stop()
                            
                            
                        testsran = testsran + 1
                        activity = self.driver.current_activity
                        print("ACTIVITY",activity)
                    else:
                        # print("\n\033[196mexcecuting test \033[104m" +"this is k"+ "\033[196m from page -> " + "v" +" ;next screen "+"page"+"\033[0m")
                        print("\n\033[1;41mExecution of TEST: \033[104m"+k+"\033[1;41m Failed,from page -> "+v+" ;on screen "+page+"\033[0m")
                        print("\t\t\033[1;41m Seems App crashed \033[0m")
                        occurance += 1
                        ret = False
                    if ret == True :
                        check["pass"] = check["pass"] + 1
                        check["p_test"].append(k)
                    elif ret == False :
                        check["fail"] = check["fail"] + 1
                        check["f_test"].append(k)
                    else:
                        print("testcase return value is ",ret)
                        check["warn"] = check["warn"] + 1
                        check["w_test"].append(k)
            except:
                save_screenshot(self.driver,"Initialisation_Fail")
                traceback.print_exc()
                # error_message = traceback.format_exc()
                # print(error_message)  
        
        # def fail(msg):
        #     print(msg)




# ---START OF SCRIPT
if __name__ == '__main__':
    print("script started")
    print("testran",testsran)
    
    tests = Bfc()
    tests.evaluate()
    totdef =len(multidef)+len(nodef)+len(okdef)
    
    if (len(multidef)>0 or len(nodef)>0):
        if len(multidef)>0:
            printblue("change name of one module or check for redundancy")
            print("redundancy found as : "+str(len(multidef)/2)+"/"+str(totdef))
            printred("there are more than one definitions for \n" )
            print(multidef)
             
        if len(nodef)>0:
            printred("make sure def's are added accurately in their pages, check for commented def's")
            print("chances are the page maynot be imported properly","\nmake sure module is added to the main function")
            print("no definition found as : "+str(len(nodef))+"/"+str(totdef))
            printred("there are NO definitions found for " )
            print(nodef)
    else:
        print("\n\nEvaluations completed, everything seems to be in order")
        if( not no_run):
            tests.initiate_from_formatted_serialiser()
        else:
            print("!""*""|""*""!"*int(os.get_terminal_size().columns/5))    
            p("only folder check and and configuration checks are executed in --no-run")
    print("!""*""|""*""!"*int(os.get_terminal_size().columns/5))    
    print("\nTOTAL TEST RUN COUNT = ",str(testsran)) 
    if( not no_run):
        print("this is check \n",check)
        reportcard(check)
        if (feederexceloutput or feederhtmloutput):
            print("feederexceloutput is enabled?",feederexceloutput)
            print("feederhtmloutput is enabled? ",feederhtmloutput)
#feeder report written in util.py use loop to get all line
            # print("\n\n\n\n"+CYAN+"this is feedercheck before passing to report\n\n",feedercheck,CRESET)
            feederreport()
        else:
            print("feeder Output file will not be generated, no available options found")
        # tests.stop()
    else:
        p("TESTS NOT EXECUTED ON --no-run")

