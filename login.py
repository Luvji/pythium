from customclasses import failed, splashloadtooklong
from util import *
from config import *
# from util import wait_until_activity
from time import sleep
import traceback
from selenium.webdriver.common.by import By

#enter date - as a function module
def enterdate(self,dateselected):
    # try:
        self.driver.implicitly_wait(3)

        if dateselected not in  ['',None]:
            global lastbday, lastbmonth,lastbyear
            
            d = driver = self.driver

            dob = dateselected.rsplit("-") #'2009-03-20' => ['2009', '03', '20']
            bday =  dob[2]    #format dd
            bmonth =  dob[1]  #format mm
            byear =  dob[0] #format yyyy
            print("DOB verification in process - adding date ",dateselected)
            print("selecting day - "+bday)
            try:
                day = d.find_element_by_xpath("//android.widget.TextView[@text = 'Day']")
            except NoSuchElementException:
                day = d.find_element_by_xpath("//android.widget.TextView[@text = '"+lastbday+"']")
                #####Scroll here to top
                
            day.click()
            daytextxpath ="//android.widget.TextView[@text = '"+bday+"']"
            print("daytextxpath",daytextxpath)
            scroll_on_element(d,daytextxpath,start_x=248, start_y=1608,
                                                        end_x=243, end_y=1066,topelement="//android.widget.TextView[@text = '01']")
            _bday = d.find_element_by_xpath(daytextxpath) 
            _bday.click()
            print("selecting month - ",bmonth)
            try:
                _month = driver.find_element(By.XPATH,
                                        "//android.widget.TextView[@text = 'Month']")
            except NoSuchElementException:
                        _month = driver.find_element(By.XPATH,
                                        "//android.widget.TextView[@text = '"+lastbmonth+"']")
            _month.click()
            _monthtextxpath = "//android.widget.TextView[@text = '"+bmonth+"']"
            scroll_on_element(d,_monthtextxpath,start_x=476, start_y=1343,
                                    end_x=471, end_y=1196,topelement="//android.widget.TextView[@text = '01']")
            # 32. Click 'mm'            
            _month = driver.find_element(By.XPATH,
                                    _monthtextxpath)
            _month.click()
            # 33. Click 'YYYY'
            _yyyy = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/etDOBYear")
            _yyyy.click()
            # 34. Type '####' in 'YYYY'
            _yyyy = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/etDOBYear")
            print("typing year ",byear)
            _yyyy.send_keys(byear)
            
            lastbday =  dob[2]    #format dd
            lastbmonth =  dob[1]  #format mm
            lastbyear =  dob[0] #format yyyy
            
            #clicking on proceed
            d.find_element(By.ID,"imgEmail").click() # proceed button
            check_snackbarv2(d)
            print("checking for flow change after date submit")
            dobverificationpopup = d.find_elements(By.ID,"txtHeading")
            
            if len(dobverificationpopup)>0 and dobverificationpopup[0].text == "DOB Verification":
                print("flow is Dob change")
            sleep(1)
            if len(driver.find_elements(By.ID,'txtHeading'))>0 or len(driver.find_elements(By.ID,'btnOk'))>0 or len(driver.find_elements(By.XPATH,"//android.widget.Button[@text = 'CANCEL']"))>0:
                # id	@id/btnOk text	DOB Verification
                print("Normal flow interupted , pop up found")
                
                if len(driver.find_elements(By.ID,'txtHeading'))>0:
                    if driver.find_element(By.ID,'txtHeading').text == 'DOB Verification':
                        print("dob change sscreen shown")
                    # id	@id/btnOk
                        if len(driver.find_elements(By.ID,'btnOk'))>0: #on dob verification page
                            print("clicking on ok button on popup")
                            driver.find_element(By.ID,'btnOk').click()
                            print("ok button clicked")
                        else:
                            print("ok button not found on dob verification popup.")
                    else:
                        if len(driver.find_elements(By.ID,'title_template'))>0:
                            print("\t\talert displayed , if below codes fsils frequently please proceed the code here, with this check")
                            alerttext = driver.find_elements(By.ID,'title_template').find_element(By.ID,"message").text
                            print("alert is :" ,alerttext)
                    
                    
                    if len(driver.find_elements(By.XPATH,"//android.widget.Button[@text = 'CANCEL']"))>0:
                        alerttexts = driver.find_elements(By.ID,'message')
                        if len(alerttexts)>0:
                            if alerttext == 'Do you want to proceed with passport number instead?':
                                print("alert with passport verification text found")
                                if 'passport' in expectedloginflow and loggedpassport not in ['',None]:
                                    print("expected passport flow , clicking on ok button")
                                    driver.find_element(By.XPATH,"//android.widget.Button[@text = 'OK']").click()
                                    txtLabelEnterCpr = driver.find_element(By.ID,'txtLabelEnterCpr').text #passport verification text
                                    
                                    if checkassert(d,txtLabelEnterCpr,'==','Passport Verification'):
                                        print("verifying passport as ",loggedpassport)
                                        
                                        driver.find_element(By.ID,'edtCPR').send_keys(loggedpassport)
                                        d.find_element(By.ID,"btnSubmit").click()
                                        return True
                                        
                                        
                                    else:
                                        print("passport verification page not reached")
                                        return 
                                    return True
                                elif force:
                                    print("passport flow not expected . but with force enabled ,contunuing to complete test")
                                else:
                                    if loggedpassport in ['',None]:
                                        print(RED+"\tpassport is not defined"+CRESET)
                                        if 'passport' in expectedloginflow:
                                            raise failed("sign in with cpr with passport","passport is not defined")
                                    else:
                                        print("passport flow not intended, clciking on cancel")
                                        
                                    driver.find_element(By.XPATH,"//android.widget.Button[@text = 'CANCEL']").click()
                        else:            
                            print("no alert message found")
                            # print("clicking on ok cancel button on alert popup with message - ",alerttext)
                        checklocked = driver.find_elements(By.XPATH,"//android.widget.TextView[@text = 'Sorry your profile is locked, Do you want to unlock it now?']")
                        if len(checklocked)>0:
                            # driver.find_element(By.XPATH,"//android.widget.Button[@text = 'CANCEL']").click()
                            raise failed ('signup',checklocked[0].text+ "use portal to unlock user")
                        # "//android.widget.Button[@text = 'OK']"
                        driver.find_element(By.XPATH,"//android.widget.Button[@text = 'CANCEL']").click()
                    
                    elif len(driver.find_elements(By.XPATH,"//android.widget.Button[@text = 'CANCEL']"))>0:
                        print("cancel shown")
                        #remove this check
                    
                        checklocked = driver.find_elements(By.XPATH,"//android.widget.TextView[@text = 'Sorry your profile is locked, Do you want to unlock it now?']")
                        checkpp = driver.find_elements(By.XPATH,"//android.widget.TextView[@text = 'Do you want to proceed with passport number instead?']")
                        # TOD:handle these seperately
                        if len(checklocked)>0:
                            print("\n"+driver.find_element(By.ID,'message').text+"\n")
                            
                            driver.find_element(By.XPATH,"//android.widget.Button[@text = 'CANCEL']").click()
                            raise failed ('signup',checklocked[0].text)
                        if len(checkpp)>0:
                            # print("\n"+driver.find_element(By.ID,'message').text+"\n")
                            print("passport proceed flow needed to be implemented here")

                            if 'passport' in expectedloginflow and loggedpassport not in ['',None]:
                                    print("expected passport flow , clicking on ok button")
                                    driver.find_element(By.XPATH,"//android.widget.Button[@text = 'OK']").click()
                                    txtLabelEnterCpr = driver.find_element(By.ID,'txtLabelEnterCpr').text #passport verification text
                                    
                                    if checkassert(d,txtLabelEnterCpr,'==','Passport Verification'):
                                        print("verifying passport as ",loggedpassport)
                                        
                                        driver.find_element(By.ID,'edtCPR').send_keys(loggedpassport)
                                        d.find_element(By.ID,"btnSubmit").click()
                                        return True

                                    else:
                                        print("passport verification page not reached")
                                        return False
                            else:                     
                                print("passport flow not intended","no passport number found" if loggedpassport in ['',None] else "passport number is +"+loggedpassport)
                                driver.find_element(By.XPATH,"//android.widget.Button[@text = 'CANCEL']").click()
                            
                        # getting message text
                        # driver.find_elements(By.XPATH,"//android.widget.Button[@text = 'CANCEL']").click()
                        
                    elif len(driver.find_elements(By.ID,'btnOk'))>0:
                        print("ok button shown")
                        checklocked = driver.find_element(By.XPATH,"//android.widget.TextView[@text = 'Sorry your profile is locked, Do you want to unlock it now?']")
                        checklockeddisplayed = driver.find_element(By.XPATH,"//android.widget.TextView[@text = 'Sorry your profile is locked, Do you want to unlock it now?']").is_displayed()           
                        # android:id/message
                        if checklockeddisplayed:
                            return False

                        print("\nthis is meessage found"+driver.find_element(By.ID,'message').text+"\n")
                        driver.find_element(By.ID,'btnOk').click()
                            # 'Do you want to proceed with passport number instead?'
                            
                    # else:
                    #     print("new screen found but it is not dob")
                    #     save_screenshot(d,"register with cpr- enter date")
                    #     return False
   
                elif len(driver.find_elements(By.XPATH,"//android.widget.Button[@text = 'CANCEL']"))>0:
                    print("cancel shown")
                    #remove this check
                
                    checklocked = driver.find_elements(By.XPATH,"//android.widget.TextView[@text = 'Sorry your profile is locked, Do you want to unlock it now?']")
                    checkpp = driver.find_elements(By.XPATH,"//android.widget.TextView[@text = 'Do you want to proceed with passport number instead?']")
                    # TOD:handle these seperately
                    if len(checklocked)>0:
                        print("\n"+driver.find_element(By.ID,'message').text+"\n")
                        
                        driver.find_element(By.XPATH,"//android.widget.Button[@text = 'CANCEL']").click()
                        raise failed ('signup',checklocked[0].text)
                    if len(checkpp)>0:
                        # print("\n"+driver.find_element(By.ID,'message').text+"\n")
                        print("passport proceed flow needed to be implemented here")

                        if 'passport' in expectedloginflow and loggedpassport not in ['',None]:
                                print("expected passport flow , clicking on ok button")
                                driver.find_element(By.XPATH,"//android.widget.Button[@text = 'OK']").click()
                                txtLabelEnterCpr = driver.find_element(By.ID,'txtLabelEnterCpr').text #passport verification text
                                
                                if checkassert(d,txtLabelEnterCpr,'==','Passport Verification'):
                                    print("verifying passport as ",loggedpassport)
                                    
                                    driver.find_element(By.ID,'edtCPR').send_keys(loggedpassport)
                                    d.find_element(By.ID,"btnSubmit").click()
                                    return True

                                else:
                                    print("passport verification page not reached")
                                    return False
                        else:                     
                            print("passport flow not intended","no passport number found" if loggedpassport in ['',None] else "passport number is +"+loggedpassport)
                            driver.find_element(By.XPATH,"//android.widget.Button[@text = 'CANCEL']").click()
                        
                    # getting message text
                    # driver.find_elements(By.XPATH,"//android.widget.Button[@text = 'CANCEL']").click()
                    
                elif len(driver.find_elements(By.ID,'btnOk'))>0:
                    print("ok button shown")
                    checklocked = driver.find_element(By.XPATH,"//android.widget.TextView[@text = 'Sorry your profile is locked, Do you want to unlock it now?']")
                    checklockeddisplayed = driver.find_element(By.XPATH,"//android.widget.TextView[@text = 'Sorry your profile is locked, Do you want to unlock it now?']").is_displayed()           
                    # android:id/message
                    if checklockeddisplayed:
                        return False

                    print("\nthis is meessage found"+driver.find_element(By.ID,'message').text+"\n")
                    driver.find_element(By.ID,'btnOk').click()
                        # 'Do you want to proceed with passport number instead?'
                        
                else:
                    print("new screen found but it is not dob")
                    save_screenshot(d)
                    return False
                
                # enterdate(self,'2009-03-20')
            else:
                print("no flow change occured until now , proceeding now")
                
                return True
        else:
            print("no date passed passed")

#register with cpr - main login logic
def register_with_cpr(self):
    test_name = 'Register with cpr'
    testflow = test_name
    message = 'unexpected error occured in '+test_name
    status = "FAIL"
    d = driver = self.driver
    tr =False

    try:
        print("current activity at start = ",d.current_activity)
        'com.bfc.bfcpayments.modules.splash.view.SplashScreenActivity'
        splash_activity_check = wait_until_activity(d,'com.bfc.bfcpayments.modules.splash.view.SplashScreenActivity','notvisible',sec=30)
        if not splash_activity_check:
            message = "splash screen took too long time to complete loading"
            raise splashloadtooklong
        print("checking the entry gateway as signup or signin")
        if not len(d.find_elements(By.ID,"txtHeading")) > 0 and len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack"))>0:
            print("signin flow")
            testflow = testflow + ">sign in with pin"
            print("add logic to implement decision on signin with pin or logout")
            tr,message = signinwithpin(self,minimal=True)
            if tr == True:
                status = "PASS"
                # message = "sign in with pin success"
            else:
                status = "FAIL"
                # message = "not reached the dashboard , call_check dashboard here"
        elif len(d.find_elements(By.ID,"txtHeading")) > 0 and not len(d.find_elements(By.ID,"txtWelcomeDialog")) > 0: #d.find_element_by_id("txtWelcomeDialog").is_displayed():
            print("getting on the signupflow")
            signupwelcometext = d.find_element(By.ID,"txtHeading").text
            print("checking if text ",signupwelcometext," is actually intended welcome text")
            if not checkassert(d,signupwelcometext in ['Instant Recharges & Bill Payments',"International money transfers at great rates",'Secure Digital Wallet'] ,"==",True,"welcome text displayed is expected?"):
                raise splashloadtooklong 
            
            print("clicking on the register button")
            d.find_element(By.ID,"btnRegister").click()
            
            entercprlabel = d.find_element(By.ID,"txtLabelEnterCpr").text
            checkassert(d,entercprlabel ,"==","Enter your CPR number","enter CPR label displayed?")
            
            entercpr = d.find_element(By.ID,"edtCPR")
            entercpr.send_keys(loggedcpr)
            print("entered cpr , ",loggedcpr)
            
            d.find_element(By.ID,"checkBoxTermsAndConditions").click()
            
            d.find_element(By.ID,"btnSubmit").click()
            # check_snackbarv2(d)
            snackbarfound,snackbartext =  check_snackbarv2(d)
            if snackbarfound:
                print("\n",YELLOW,snackbartext,CRESET,"\n")
                print(RED+"\n\tUNLOCK the user from cxportal to continue"+CRESET)
                
                raise failed(test_name,"Alert :"+snackbartext)
            print("proceed button clicked , reaching onto mobile number page:")
            # check_and_waitforprogressbar(d,sec=2)
            check_progressbar(d)

            lblentermobnum = d.find_element(By.ID,"txtLabelAlmostHere").text
            checkassert(d,lblentermobnum ,"==","Enter your mobile number","enter mobile number label displayed?")
            # loggedmobile = "33333333"
            formattednumber = loggedmobile[0]+"****"+loggedmobile[5:8] #making it into format = 6****011
            
            
            print("entering mobile number , ",loggedmobile)
            print(YELLOW+"\n\n\n changing mobilenumber to null for test , change it back to variable after development"+CRESET+"\n\n\n")
            # id	@id/viewEditBg
            if loggedmobile == "33333333":
                d.find_element(By.ID,"editMobileNumber").send_keys('31336333')
            else:  
                d.find_element(By.ID,"editMobileNumber").send_keys(loggedmobile)
            
            d.find_element(By.ID,"btnSubmit").click()
            # id	@id/txtLabelAlmostHere id	@id/txtHeading
            anothermobileregistered = False
            try:
                anothermobileregistered = d.find_element(By.ID,"txtHeading").is_displayed()
            except NoSuchElementException as e:
                print("the mobile number is as same as registered one")
            if anothermobileregistered:
                print("another mobile seems to be registered with this account,proceeding with that","+973 "+formattednumber)
                # //android.widget.RadioButton[@text = '+973 3****369']
                print(YELLOW+"\n\n\n\nthis is hardecoded in here, \n\n used changemobile in expectedloginflow \n\n"+CRESET)
                # rbtn = d.find_element(By.XPATH,"//android.widget.RadioButton[@text = '+973 3****369']")

                # print("radio button checked?",rbtn1.get_attribute("checked"))
                # print("radio button is selected with the mobile number text '+973 "+formattednumber+"'")
                if 'changemobile' in expectedloginflow:
                    testflow = testflow + ">change mobile"
                    rbtn1 = d.find_element_by_xpath("//android.widget.RadioButton[@text = '+973 "+loggedmobile+"']")
                    rbtn1.click()
                    formattednumber = loggedmobile
                    print("clciking on another mobile")  
                else:
                    testflow = testflow + ">no mobile change"
                    print("moile number change flow not intended,selecting the already registered number")  
            else:
                print("no other mobile number for is registered with this account")
                if not checkassert(d,'changemobile' in expectedloginflow , "expected flow check"):
                    print("expected flow cannot be executed , proceeding with normal flow.")
            d.find_element_by_xpath("//android.widget.Button[@text = 'Proceed']").click()
            check_progressbar(d)
            enterotplabel = d.find_element(By.ID,"txtLabelAlmostHere").text
            txt ="Enter the 6 digit OTP sent to +973 "+formattednumber
            checkassert(d,enterotplabel ,"==",txt,"enter OTP label displayed?")
            # id	@id/edtOtp
            d.find_element(By.ID,"edtOtp").send_keys(loggedotp)
            print("OTP entered ")
            d.find_element(By.ID,"btnSubmit").click()
            
            snackbarfound,snackbartext =  check_snackbarv2(d)
            if snackbarfound:
                print("\n",YELLOW,snackbartext,CRESET,"\n")
                # print(RED+"\n\tUNLOCK the user from cxportal to continue"+CRESET)
                save_screenshot(d,test_name)
                raise failed(test_name,"Alert :"+snackbartext)
                
            print("proceed button clicked , reaching onto mobile number page:")
            # id	@id/txtVerifyDobLabel
            lblverifydate = d.find_element(By.ID,"txtVerifyDobLabel").text
            
            checkassert(d,lblverifydate ,"==","Verify date of birth","verify date page reached?")

# adding date as function
            if isinstance(loggeddob, list):
                testflow = testflow + ">multiple DOB"
                for selecteddate in loggeddob:
                    checkdate = enterdate(self,selecteddate)
                    if checkdate == True:
                        break
            else:
                testflow = testflow+ ">single DOB"
                enterdate(self,loggeddob)
            print("checking if dob verification ")
#wait time reduced inside enter dob section returning it to normal now
            self.driver.implicitly_wait(10)
                        
            check_and_hide_keyboard(d)
            # id	@id/imgEmail txtLabelSetMpin
            txtLabelSetMpin = d.find_element(By.ID,"txtLabelSetMpin").text
            checkassert(d,txtLabelSetMpin ,"==","Set a PIN","Pin set page reached?")
            
            #id	@id/edtPin  id	@id/edtConfirmPin
            print("confirming pin")
            d.find_element(By.ID,"edtPin").send_keys(loggeduserpin)
            print("PIN entered ,confirming PIN now")
            d.find_element(By.ID,"edtConfirmPin").send_keys(loggeduserpin)
            print("pin entered is",loggeduserpin,"now clicking proceed")
            # check_and_hide_keyboard(d)
            check_progressbar(d)
            # d.find_element(By.ID,"btnSubmit").click()
            # id	@id/txtPersonName
            print('checking for shufti screen')
            if len(d.find_elements(By.ID,"txtPersonName"))== 0:
                testflow = testflow + ">shufti "
                print("screen proceeded to shufti")
                if 'shufti' in expectedloginflow:
                    testflow = testflow + "initiated"
                    shufti_initiation(self)
                elif force :
                    print(RED+ "\n\t\tthis went to shufti , which was not intended.but with force enabled test continues with shufti."+CRESET)
                    testflow = testflow + "forcefully initiated"
                    test_name = 'signup_with_cpr_with_known_number_with_force_shufti'
                    tr,status,message = shufti_initiation(self)
                    print("shufti completed ,tr,status,message are  " ,tr,status,message)
                else:
                    testflow = testflow + "unexpected"
                    print("this is not expected to be in shufti")
            else:
                
                if 'shufti' in expectedloginflow:
                    print(RED+ "\n\t\tshufti flow expected,but flow didnt reached shufti. check your login user data. this might be an issue"+CRESET)
                
                loggedpersonname = d.find_element(By.ID,"txtPersonName").text
                testflow = testflow + ">dashboard"
                tr = checkassert(d,loggedpersonname ,"==",loggedname,"checking logged name is :"+loggedname+"?")
                if tr == True:
                    print("updating wallet balance")
                    walletbal = d.find_element(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtAmtAvailBal").text
                    status = "PASS"
                    message = test_name+" completed successfully"
                else:
                    status = "Fail"
                    message = "not reached the dashboard , call_check dashboard here"
                
        else:
            print("\nthis is else in signup !!!,this means normal flow is not working\n")
            save_screenshot(d,test_name)
            
            print("first condition: ",not len(d.find_elements(By.ID,"txtHeading")) > 0 and len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack"))>0)
            print('len(d.find_elements(By.ID,"txtHeading")) (invert): ',len(d.find_elements(By.ID,"txtHeading")))
            print('len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack")) : ',len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack")))
            print("this second condition",len(d.find_elements(By.ID,"txtHeading")) > 0 and len(d.find_elements(By.ID,"txtWelcomeDialog")) > 0)
            print('len(d.find_elements(By.ID,"txtHeading"))',len(d.find_elements(By.ID,"txtHeading")))
            print('len(d.find_elements(By.ID,"txtWelcomeDialog")) > 0',len(d.find_elements(By.ID,"txtWelcomeDialog")) > 0)
            
        print("checking current activity is dashboard ,if not the flow might have changed to shufti")
        if (d.current_activity != "com.bfc.bfcpayments.modules.home.view.DashboardActivity"):
            if tr:
                message = message + " , But the activity dashboard not reached"
                tr = "warn"
                checkshufti = d.find_element(By.ID,'txtVerifyDobLabel') and d.find_element(By.ID,'txtVerifyDobLabel').text == 'Consent for verification'
                if checkshufti:
                    print("shufti procedure needed to be proccessed\n")
                    print("\n\n\n check if this call to shufti is needed , it may not be needed after all")
                    if force:
                        
                        tr,status,message = shufti_initiation(self,minimal = True)
                    # if tr:
                    else:
                        print("shufti procedure will not be initiated")
                        
                else:
                    print("consent for verification not found. ")
            else:
                print("it is not expected to be in Dashboard as the test already failed")
        else:
            if tr:
                message = message + " and Dashboard activity Reach confirmed"
            else:
                message = 'the activity is not expected to reach in Dashboard as the test already failed' + " But the Activity UNEXPECTEDLY reached Dashboard "
           
        print(message)
        
    except Exception as e:
        # self.fail("Encountered an unexpected exception.test failed in "+test_name)
        print(e)
        save_screenshot(d, test_name)
        status = "FAIL"
        traceback.print_exc()
        message = e 
        tr = False
        
        # print(error_message)  
    
    finally:
        #may need to check the crash
        testcasereport(test_name,status,message)
        return tr
     
#second option to login if already logged in    
def signinwithpin(self,minimal = False,logged = None):
    """
    minimal : true doesnt call test report
    returns 2 variables if minimal
    
    """
    test_name = 'signin_with_pin'
    
    if logged == None : #if not feeder take the variable from global ie. from config.py
        global loggedname
    if logged != None and len(logged)>0: #if this is of a feeder there will be a logged
        loggedcpr = logged['cpr']
        loggedmobile = logged['mobile']
        expectedloginflow = logged['expectedloginflow'] if len(logged['expectedloginflow'])>0 else []
        loggeddob = logged['dob']
        force = False
        loggedname = logged['name']
        test_name = test_name + " IN FEEDER"

        
    message = 'unexpected error occured in '+test_name
    status = "FAIL"
    d = driver = self.driver
    tr =False
    try:
        d = driver = self.driver
        # id	@id/txtWelcomeBack
        print("checking for sign in strategy")
        check_snackbarv2(d)
        
        # print("        user is logged in on another device case to be ijmplement        ")
        if not len(d.find_elements(By.ID,"txtHeading")) > 0 and len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack"))>0:
            printred("\tapp is already logged in. if not intended it is a FAIL")
            print("current activity in simple login ",d.current_activity)
            c1 = driver.find_element(By.ID,"txtWelcomeBack")
            # print("\nwelcome back text :::::::::::::",c1.text)
            if (checkassert(d,c1.text ,"contains",loggedname," intended user check")):
                c1.click()
                com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_1 = driver.find_element(By.ID,
                                                                                        "circleField")
                com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_1.send_keys(str(loggeduserpin))
                check_snackbarv2(d)
                check_progressbar(d)
                # d.find_element(By.ID,"btnSubmit").click()
                # id	@id/txtPersonName
                print("checking for dashboard activity visibility",d.current_activity == dashboardactivity)
                loggedpersonname = d.find_element(By.ID,"txtPersonName").text
                tr = checkassert(d,loggedpersonname ,"==",loggedname,"checking logged name in dashboard is :"+loggedname+"?")
                if tr == True:
                    print("updating wallet balance")
                    walletbal = d.find_element(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtAmtAvailBal").text
                    status = "PASS"
                    message = "Test passed with signing in with pin"
                else:
                    status = "Fail"
                    #message = "not reached the dashboard , call_check dashboard here"
            else:
                print("the logged in user is not intended user,restart login process")
                print("logged in user",c1.text.strip('Welcome Back,'),"intended user",loggedname)
                self.driver.find_element_by_id('txtForgotPin').click()
                waitfor(d,"txtHeading")
                if force:
                    register_with_cpr(self)
                else:
                    print("force not turned on , and the user logged in is not intended")     
        else:
            print("user not logged in ")

    except Exception as e:
        # self.fail("Encountered an unexpected exception.test failed in "+test_name)
        print(e)
        save_screenshot(d, test_name)
        status = "FAIL"
        traceback.print_exc()
        message = e 
        tr = False
    finally:
        # print("moniimal is ",minimal)
        if not minimal:
            testcasereport(test_name,status,message)
            return tr
        else:
            return tr,message
        
#signout of already logged in account
def signout(self,signouttoregister = True,minimal = False):
    '''
        put minimal as true , if just checking on a routine - it will not raise any issues
        put signouttoregister = True , reach till register page , setting it false will just logs you out, you may enter back with giving pin
    '''
    test_name = 'signout_and_reach_register_page'
    message = 'unexpected error occured in '+test_name
    status = "FAIL"
    d = driver = self.driver
    tr =False
    try:
        print('signout')
        mainactivitycheck = wait_until_activity(d,'com.bfc.bfcpayments.modules.login.view.MainActivity','visible',5)
        if not mainactivitycheck:
            save_screenshot(d, test_name+" activity check fail")
            
        # //android.widget.TextView[@text = 'Forgot PIN']
        # com.bfccirrus.bfcpayments.mobile:id/txtForgotPin
        #                         com.bfc.bfcpayments.modules.login.view.MainActivity
        if d.current_activity == 'com.bfc.bfcpayments.modules.login.view.MainActivity':
            # print("print it is not in dashboard,ensure not in log in screen")\
            print("screen in mainactivity")
            # back_to_dashboard(self.driver,True)
            d.find_element(By.ID,'txtForgotPin').click()
            wait_until_activity(d,'com.bfc.bfcpayments.modules.login.view.MainActivity','notvisible',5)
            if checkassert(d,d.current_activity,'==','SignUpSliderActivity'):
                tr = True
                status = "PASS"
                message = "user signed out successfullty"
                
        elif d.current_activity == 'SignUpSliderActivity' or d.current_activity == signupactivity:
            print("user not logged in . if it is not intended , raise failed ")
            if not minimal or force:
                status = "FAIL"
                message = "user cannot be signed out as user is not logged in in the first place"
                tr = 'warn'
                raise failed(test_name,message)
            else:
                status = "PASS"
                message = "user already signed out"
                tr = 'warn'
                raise failed(test_name,message)
                
                    
        elif d.current_activity == 'com.bfc.bfcpayments.modules.home.view.DashboardActivity':
            print("in dashboard")
            
            d.find_element(By.ID,'btnDashBoardIcon').click()
            signoutelem = d.find_element(By.ID,'txtNavTitle')
            scroll_down_to_view(d,'txtNavTitle',)
            # signoutelem.click() text	Sign Out "//*[@text = 'Sign Out']"
            driver.find_element(By.XPATH,"//*[@text = 'Sign Out']").click()
            wait_until_activity(d,'com.bfc.bfcpayments.modules.login.view.MainActivity','visible',5)
            if checkassert(d,d.current_activity,'==','com.bfc.bfcpayments.modules.login.view.MainActivity'):
                if signouttoregister:
                    print("screen in mainactivity after clicking signout from dashboard")
                    # back_to_dashboard(self.driver,True)
                    d.find_element(By.ID,'txtForgotPin').click()
                    wait_until_activity(d,'com.bfc.bfcpayments.modules.login.view.MainActivity','notvisible',5)
                    if checkassert(d,d.current_activity,'==', signupactivity):
                        tr = True
                        status = "PASS"
                        message = "user signed out successfullty"
                    else:
                        tr = False
                        status = "FAIL"
                        message = "user signed Failed , register screen not reached"
                else:
                    tr = True
                    status = "PASS"
                    message = "user signed out to main activity successfully"
                        
            else:
                print("intended activity not reached yet")
                status = "FAIL"
                message = "intended activity not reached after clicking on signout"
                tr = False

        else:
            print("current activity is : ",d.current_activity)
            print("current activity is : ",d.current_activity == 'com.bfc.bfcpayments.modules.login.view.MainActivity' )
            
    except Exception as e:
        # self.fail("Encountered an unexpected exception.test failed in "+test_name)
        print(e)
        save_screenshot(d, test_name)
        status = "FAIL"
        traceback.print_exc()
        message = e 
        tr = False
        
        # print(error_message)  
    
    finally:
        testcasereport(test_name,status,message)
        return tr
    
#shufti flow automation function
def shufti_initiation(self,minimal = True):
    test_name = 'signup_with_cpr_with_known_number_with_shufti'
    message = 'unexpected error occured in '+test_name
    status = "FAIL"
    d = driver = self.driver
    tr =False
    try:
        if d.find_element(By.ID,'txtVerifyDobLabel') and checkassert(d,driver.find_element(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtVerifyDobLabel").text,"==",'Consent for verification'," shufti verification reached"):
            print("shufti verification initiated")
            print("confirm consent window")
            # 2. Click 'Yes, Proceed'
            yes_proceed = driver.find_element(By.ID,
                                            "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
            yes_proceed.click()
            # 3. check 'shuftipro-verification-process' to be not seen - shufti loader
            # shuftipro_verification_process = driver.find_element(By.XPATH,
            #                                                     "//android.webkit.WebView[@text = 'shuftipro-verification-process']")
            # shuftipro_verification_process.click()
            wait_until(d,"//android.webkit.WebView[@text = 'shuftipro-verification-process']",'not visible')

            # 4. Click 'How would you like to submit your Nat...'
            wait_until(d,"//android.view.View[@text = 'How would you like to submit your National ID ?']",'visible')
            how_would_you_like_to_submit_your_id = driver.find_element(By.XPATH,
                                                                        "//android.view.View[@text = 'How would you like to submit your National ID ?']")
            
            if checkassert(d,how_would_you_like_to_submit_your_id.text,'==','How would you like to submit your National ID ?'):

                # 5. Click 'Upload file'
                upload_file = driver.find_element(By.XPATH,
                                                "//android.widget.Button[@text = 'Upload file ']")
                upload_file.click()

                # 6. Click 'Upload a photo of the frontside of yo...'
                upload_a_photo_of_the_frontside_of_yo_ = driver.find_element(By.XPATH,
                                                                            "//android.view.View[@text = 'Upload a photo of the frontside of your Bahraini National ID']")
                upload_a_photo_of_the_frontside_of_yo_.click()
                print("image uploading start")
                # 7. Click 'Upload'
                upload = driver.find_element(By.XPATH,
                                            "//android.widget.Button[@text = 'Upload']")
                upload.click()
                # upload.send_keys(r'C:\Users\Administrator\Desktop\pyppium_new_app\data\ID_front.jpeg')

                # # 8. Click 'ANDROID.WIDGET.RELATIVELAYOUT' choose cam or gallery
                # android_widget_relativelayout = driver.find_element(By.XPATH,
                #                                                     "//android.widget.RelativeLayout")
                # # android_widget_relativelayout.click()
                # android_widget_relativelayout.send_keys(r'C:\Users\Administrator\Desktop\pyppium_new_app\data\ID_front.jpeg')
                image_choose = driver.find_element(By.XPATH,"//android.widget.TextView[@text = 'Image Chooser']")
                # 9. Click 'android:id/icon' select files
                android_colon_id_slash_icon = driver.find_element(By.XPATH,
                                                                "//android.widget.TextView[@text = 'Files']")
                                                                # "//android.widget.LinearLayout[2]//android.widget.ImageView") 
                
                # android_colon_id_slash_icon.send_keys(r'C:\Users\Administrator\Desktop\pyppium_new_app\data\ID_front.jpeg')
                android_colon_id_slash_icon.click()
                print("\n\n\n self.driver.context is current context",self.driver.current_context)

                # 10. Click 'com.android.documentsui:id/icon_thumb'
                com_android_documentsui_colon_id_slash_icon_thumb = driver.find_element(By.XPATH,
                                                                                        "//android.widget.TextView[@text = 'ID_front.jpeg']")
                com_android_documentsui_colon_id_slash_icon_thumb.click()

                # # 11. Click 'More options'
                # more_options = driver.find_element(By.XPATH,
                #                                 "//android.widget.ImageButton[@content-desc = 'More options']")
                # more_options.click()

                # 12. Click 'Continue'
                # wait_until(d,"//android.view.View[@text = 'Can you see the entire document clearly in the photo?'])",'visible')
                print("clicking on continue to confirm")
                _continue = driver.find_element(By.XPATH,
                                                "//android.widget.Button[@text = 'Continue']")
                _continue.click()

                # 13. Click 'Upload1'
                print("uploading backside of the national id")
                
                
                wait_until(d,"//android.view.View[@text = 'Upload a photo of the backside of your Bahraini National ID']",'visible')
                
                
                upload1 = driver.find_element(By.XPATH,
                                            "//android.widget.Button[@text = 'Upload']")
                upload1.click()
                print("\n\n\n self.driver.context is current context",self.driver.current_context)

                # 14. Click 'android:id/icon' image chooser found selecting files
                android_colon_id_slash_icon = driver.find_element(By.XPATH,
                                                                "//android.widget.TextView[@text = 'Files']")
                android_colon_id_slash_icon.click()
                


                # 15. Click 'com.android.documentsui:id/icon_thumb1'
                # com_android_documentsui_colon_id_slash_icon_thumb1 = driver.find_element(By.XPATH,
                                                                                        # "//android.widget.LinearLayout[2]//android.widget.ImageView")
                com_android_documentsui_colon_id_slash_icon_thumb1 = driver.find_element(By.XPATH,
                                                                                        "//android.widget.TextView[@text = 'ID_back.jpeg']")
                
                print("\n\n\n self.driver.context is current context after file click",self.driver.current_context)
                
                
                com_android_documentsui_colon_id_slash_icon_thumb1.click()

                # # 16. Click 'More options'
                # more_options = driver.find_element(By.XPATH,
                #                                 "//android.widget.ImageButton[@content-desc = 'More options']")
                # more_options.click()

                # 17. Click 'Can you see the entire document clear...'
                can_you_see_the_entire_document_clear_ = driver.find_element(By.XPATH,
                                                                            "//android.view.View[@text = 'Can you see the entire document clearly in the photo?']")
                can_you_see_the_entire_document_clear_.click()

                # 18. Click 'Continue'
                _continue = driver.find_element(By.XPATH,
                                                "//android.widget.Button[@text = 'Continue']")
                _continue.click()
                wait_until(d,"//android.view.View[@text = 'Uploading document ...']",'not visible')
                
                print("uplaoding face")
                wait_until(d,"//android.view.View[@text = 'How would you like to verify your face?']",'visible')

                # 19. Click 'Upload file'
                upload_file = driver.find_element(By.XPATH,
                                                "//android.widget.Button[@text = 'Upload file ']")
                upload_file.click()
                # driver.switch_to.context('WEBVIEW')

                # 20. Click 'Upload'      self.driver.find_element_by_partial_link_text("YOUR CHOICES")
                upload = driver.find_element(By.XPATH,
                                            "//android.widget.Button[@text = 'Upload']")
                upload.click()

                # 21. Click 'android:id/icon'
                android_colon_id_slash_icon = driver.find_element(By.XPATH,
                                                                "//android.widget.TextView[@text = 'Files']")
                                                                
                                                                # "//android.widget.LinearLayout[2]//android.widget.ImageView")
                android_colon_id_slash_icon.click()

                # 22. Click 'com.android.documentsui:id/icon_thumb2'
                com_android_documentsui_colon_id_slash_icon_thumb2 = driver.find_element(By.XPATH,
                                                                                        "//android.widget.TextView[@text = 'face_photo.jpeg']")
                com_android_documentsui_colon_id_slash_icon_thumb2.click()


                # 24. Click 'Continue'
                _continue = driver.find_element(By.XPATH,
                                                "//android.widget.Button[@text = 'Continue']")
                _continue.click()

                # 25. Click 'Please wait while your information is...'
                please_wait_while_your_information_is_ = driver.find_element(By.XPATH,
                                                                            "//android.view.View[@text = 'Please wait while your information is being verified']")
                # please_wait_while_your_information_is_.click()

                # 26. Click 'Verification successful'
                verification_successful = driver.find_element(By.XPATH,
                                                            "//android.view.View[@text = 'Verification successful']")
                verification_successful.click()

                # 27. Click 'Proceed'
                proceed = driver.find_element(By.XPATH,
                                                            "//android.widget.Button[@text = 'Proceed']")
                proceed.click()
                print("shufti flow completed, returning now")
                
                tr = True
                status = "PASS"
                message = "shufti verification completed successfully"
            
            else:
                tr = False
                status = "FAIL"
                print("national id submition page not reached")
                raise failed(test_name,"submition page not reached")
            
            # print("check cancel button present ") #com.bfccirrus.bfcpayments.mobile:id/btnCancel
            # print("click com.bfccirrus.bfcpayments.mobile:id/btnProceed (yes,proceed") #//android.widget.Button[@text = 'Yes, Proceed']
            # print("wait for shufti loading disablrd") #com.bfccirrus.bfcpayments.mobile:id/main_tv
            # print("check and confirm reached - //android.view.View[@text = 'How would you like to submit your National ID ?']")
            
            
            
            
            # print("after image update check to finish this ,//android.view.View[@text = 'Please wait while your information is being verified']")
            # print('click proceed')
            # print("then after clicking proceed , check this is invisible //android.view.View[@text = 'Redirecting, please wait…']")
            # print("check if reached dsahboard")

        else:
            print("shufti couldnt be initialted as consent screen not found")
            
    except Exception as e:
        print(e)
        tr = False
        status = 'Fail'
        message = e
    finally:
        return tr,status,message
    
# a feeder function to feed multiple test case data - INCOMPLETE - ON HOLD
def login_feeder(self,minimal = False):
    print("tis is login feeder")
    driver = d = self.driver
    tr = False
    test_name1 = 'login_feeder'
    message = ""
    finaltr = ''
    feederresult = {}
    # tc1 = tc2 = tc3 = False
    status = True
    fullmessage = ""
    respmesg = ''
    global feedercheck
    fcsv = format_csv(r'C:\Users\Administrator\Desktop\pyppium_new_app\2022-10-19\data\logindata17-10-51.csv')
    print("\n",YELLOW,fcsv,CRESET)
    # print("\n\n\n\n\n")
    # print(fcsv,"\n\n\n\n")
    # print(fcsv.keys())
    logged = {}


    if len(fcsv.keys())>0:
        for key,value in fcsv.items():
            print("⣿"*os.get_terminal_size().columns)
            print("\n\u001b[4m\u001b[44m STARTING NEW TEST WITH TEST DATA -\u001b[0m")
            print(key ," : ", list[value])
            print(CRESET+"."*os.get_terminal_size().columns)
            
            
            print("this is something")
            logged = {}
            print("key is",key)
            print("value is ",value)
            logged['cpr'] = fcsv[key]['EmployeeCPRId']
            logged['mobile'] = fcsv[key]['MobileNumber']
            logged['name'] = fcsv[key]['FirstName']
            logged['dob'] = fcsv[key]['DateOfBirth']
            logged['expectedloginflow'] = ['shufti']
            # fcsv = format_csv(csvpath) 
            print(RED,"this is current logged data",logged,CRESET)
            try:
                d.start_activity("com.bfccirrus.bfcpayments.mobile", 'com.bfc.bfcpayments.modules.splash.view.SplashScreenActivity')
                wait_until_activity(d,'com.bfc.bfcpayments.modules.onboarding_journey.view.ui.SignUpSliderActivity','visible')
                print("current activity is",d.current_activity)
                tr = feed_signin(self,logged)
                feedercheck['paybywallet'].append({'name':fcsv[key]['name'],
                                              'cpr':fcsv[key]['cpr'],
                                              'amount' :fcsv[key]['amount'],
                                              'testcase' :testcasename,
                                              'status':tr,
                                              'reason':respmesg,
                                              'expected':fcsv[key]['expect'],
                                              'final_Result':finalres })
                
                
                
                
                
                
            except Exception as e:
                print(e)
                
# re written attempt on feeder function to feed multiple test case data - INCOMPLETE - ON HOLD   
def feed_signin(self,logged ):
    
    loggedcpr = logged['cpr']
    loggedmobile = logged['mobile']
    expectedloginflow = logged['expectedloginflow'] if len(logged['expectedloginflow'])>0 else []
    loggeddob = logged['dob']
    force = False
    loggedname = logged['name']
    
    
    test_name = 'signin feeder'
    testflow = test_name
    message = 'unexpected error occured in '+test_name
    status = "FAIL"
    d = driver = self.driver
    tr =False

    try:
        print("current activity at start = ",d.current_activity)
        'com.bfc.bfcpayments.modules.splash.view.SplashScreenActivity'
        splash_activity_check = wait_until_activity(d,'com.bfc.bfcpayments.modules.splash.view.SplashScreenActivity','notvisible',sec=30)
        if not splash_activity_check:
            message = "splash screen took too long time to complete loading"
            raise splashloadtooklong
        print("checking the entry gateway as signup or signin")
        if not len(d.find_elements(By.ID,"txtHeading")) > 0 and len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack"))>0:
            print("signin flow")
            testflow = testflow + ">sign in with pin"

            tr,message = signinwithpin(self,minimal=True,logged=logged)
            if tr == True:
                status = "PASS"
                # message = "sign in with pin success"
            else:
                status = "FAIL"
                # message = "not reached the dashboard , call_check dashboard here"
        elif len(d.find_elements(By.ID,"txtHeading")) > 0 and not len(d.find_elements(By.ID,"txtWelcomeDialog")) > 0: #d.find_element_by_id("txtWelcomeDialog").is_displayed():
            print("getting on the signupflow")
            signupwelcometext = d.find_element(By.ID,"txtHeading").text
            if not checkassert(d,signupwelcometext ,"==","International money transfers at great rates","welcome text displayed?"):
                raise splashloadtooklong 
            
            print("clicking on the register button")
            d.find_element(By.ID,"btnRegister").click()
            
            entercprlabel = d.find_element(By.ID,"txtLabelEnterCpr").text
            checkassert(d,entercprlabel ,"==","Enter your CPR number","enter CPR label displayed?")
            
            entercpr = d.find_element(By.ID,"edtCPR")
            entercpr.send_keys(loggedcpr)
            print("entered cpr , ",loggedcpr)
            
            d.find_element(By.ID,"checkBoxTermsAndConditions").click()
            
            d.find_element(By.ID,"btnSubmit").click()
            # check_snackbarv2(d)
            snackbarfound,snackbartext =  check_snackbarv2(d)
            if snackbarfound:
                print("\n",YELLOW,snackbartext,CRESET,"\n")
                print(RED+"\n\tUNLOCK the user from cxportal to continue"+CRESET)
                
                raise failed(test_name,"Alert :"+snackbartext)
            print("proceed button clicked , reaching onto mobile number page:")
            # check_and_waitforprogressbar(d,sec=2)
            check_progressbar(d)

            lblentermobnum = d.find_element(By.ID,"txtLabelAlmostHere").text
            checkassert(d,lblentermobnum ,"==","Enter your mobile number","enter mobile number label displayed?")
            # loggedmobile = "33333333"
            formattednumber = loggedmobile[0]+"****"+loggedmobile[5:8] #making it into format = 6****011
            
            
            print("entering mobile number , ",loggedmobile)
            print(YELLOW+"\n\n\n changing mobilenumber to null for test , change it back to variable after development"+CRESET+"\n\n\n")
            # id	@id/viewEditBg
            if loggedmobile == "33333333":
                d.find_element(By.ID,"editMobileNumber").send_keys('31336333')
            else:  
                d.find_element(By.ID,"editMobileNumber").send_keys(loggedmobile)
            
            d.find_element(By.ID,"btnSubmit").click()
            # id	@id/txtLabelAlmostHere id	@id/txtHeading
            anothermobileregistered = False
            try:
                anothermobileregistered = d.find_element(By.ID,"txtHeading").is_displayed()
            except NoSuchElementException as e:
                print("the mobile number is as same as registered one")
            if anothermobileregistered:
                print("another mobile seems to be registered with this account,proceeding with that","+973 "+formattednumber)
                # //android.widget.RadioButton[@text = '+973 3****369']
                print(YELLOW+"\n\n\n\nthis is hardecoded in here, \n\n used changemobile in expectedloginflow \n\n"+CRESET)
                # rbtn = d.find_element(By.XPATH,"//android.widget.RadioButton[@text = '+973 3****369']")

                # print("radio button checked?",rbtn1.get_attribute("checked"))
                # print("radio button is selected with the mobile number text '+973 "+formattednumber+"'")
                if 'changemobile' in expectedloginflow:
                    testflow = testflow + ">change mobile"
                    rbtn1 = d.find_element_by_xpath("//android.widget.RadioButton[@text = '+973 "+loggedmobile+"']")
                    rbtn1.click()
                    formattednumber = loggedmobile
                    print("clciking on another mobile")  
                else:
                    testflow = testflow + ">no mobile change"
                    print("moile number flow not intended")  
            else:
                print("no other mobile number for is registered with this account")
                if not checkassert(d,'changemobile' in expectedloginflow , "expected flow check"):
                    print("expected flow cannot be executed , proceeding with normal flow.")
            d.find_element_by_xpath("//android.widget.Button[@text = 'Proceed']").click()
            check_progressbar(d)
            enterotplabel = d.find_element(By.ID,"txtLabelAlmostHere").text
            if '****' in enterotplabel:
                
                txt ="Enter the 6 digit OTP sent to +973 "+formattednumber
                print("this number has registered once")
            else:
                txt ="Enter the 6 digit OTP sent to +973 "+loggedmobile
                print("first time registering this number")
            checkassert(d,enterotplabel ,"==",txt,"enter OTP label displayed?")
            # id	@id/edtOtp
            d.find_element(By.ID,"edtOtp").send_keys(loggedotp)
            print("OTP entered ")
            d.find_element(By.ID,"btnSubmit").click()
            
            snackbarfound,snackbartext =  check_snackbarv2(d)
            if snackbarfound:
                print("\n",YELLOW,snackbartext,CRESET,"\n")
                # print(RED+"\n\tUNLOCK the user from cxportal to continue"+CRESET)
                save_screenshot(d,test_name)
                raise failed(test_name,"Alert :"+snackbartext)
                
            print("proceed button clicked , reaching onto mobile number page:")
            # id	@id/txtVerifyDobLabel
            lblverifydate = d.find_element(By.ID,"txtVerifyDobLabel").text
            
            checkassert(d,lblverifydate ,"==","Verify date of birth","verify date page reached?")

            # adding date as function
            if isinstance(loggeddob, list):
                testflow = testflow + ">multiple DOB"
                for selecteddate in loggeddob:
                    enterdate(self,selecteddate)
            else:
                testflow = testflow+ ">single DOB"
                enterdate(self,loggeddob)
             
            
            check_and_hide_keyboard(d)
            # id	@id/imgEmail txtLabelSetMpin
            txtLabelSetMpin = d.find_element(By.ID,"txtLabelSetMpin").text
            checkassert(d,txtLabelSetMpin ,"==","Set a PIN","Pin set page reached?")
            
            #id	@id/edtPin  id	@id/edtConfirmPin
            print("confirming pin")
            d.find_element(By.ID,"edtPin").send_keys(loggeduserpin)
            print("PIN entered ,confirming PIN now")
            d.find_element(By.ID,"edtConfirmPin").send_keys(loggeduserpin)
            print("pin entered is",loggeduserpin,"now clicking proceed")
            # check_and_hide_keyboard(d)
            check_progressbar(d)
            # d.find_element(By.ID,"btnSubmit").click()
            # id	@id/txtPersonName
            print('checking for shufti screen')
            if len(d.find_elements(By.ID,"txtPersonName"))== 0:
                testflow = testflow + ">shufti "
                print("screen proceeded to shufti")
                if 'shufti' in expectedloginflow:
                    testflow = testflow + "initiated"
                    shufti_initiation(self)
                elif force:
                    testflow = testflow + "forcefully initiated"
                    test_name = 'signup_with_cpr_with_known_number_with_force_shufti'
                    tr,status,message = shufti_initiation(self)
                    print("shufti completed ,tr,status,message are  " ,tr,status,message)
                else:
                    testflow = testflow + "unexpected"
                    print("this is not expected to be in shufti")
            else:
                loggedpersonname = d.find_element(By.ID,"txtPersonName").text
                testflow = testflow + ">dashboard"
                tr = checkassert(d,loggedpersonname ,"==",loggedname,"checking logged name is :"+loggedname+"?")
                if tr == True:
                    status = "PASS"
                else:
                    status = "Fail"
                    message = "not reached the dashboard , call_check dashboard here"
                
        else:
            print("\nthis is else in signup !!!,this means normal flow is not working\n")
            # print("first condition: ",not len(d.find_elements(By.ID,"txtHeading")) > 0 and len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack"))>0)
            # print('len(d.find_elements(By.ID,"txtHeading")) (invert): ',len(d.find_elements(By.ID,"txtHeading")))
            # print('len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack")) : ',len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack")))
            # print("this second condition",len(d.find_elements(By.ID,"txtHeading")) > 0 and len(d.find_elements(By.ID,"txtWelcomeDialog")) > 0)
            # print('len(d.find_elements(By.ID,"txtHeading"))',len(d.find_elements(By.ID,"txtHeading")))
            # print('len(d.find_elements(By.ID,"txtWelcomeDialog")) > 0',len(d.find_elements(By.ID,"txtWelcomeDialog")) > 0)
            
        print("checking current activity is dashboard ,if not the flow might have changed to shufti")
        if (d.current_activity != "com.bfc.bfcpayments.modules.home.view.DashboardActivity"):
            if tr:
                message = message + " , But the activity dashboard not reached"
                tr = "warn"
                checkshufti = d.find_element(By.ID,'txtVerifyDobLabel') and d.find_element(By.ID,'txtVerifyDobLabel').text == 'Consent for verification'
                if checkshufti:
                    print("shufti procedure needed to be proccessed\n")
                    print("\n\n\n check if this call to shufti is needed , it may not be needed after all")
                    if force:
                        
                        tr,status,message = shufti_initiation(self,minimal = True)
                    # if tr:
                    else:
                        print("shufti procedure will not be initiated")
                        
                else:
                    print("consent for verification not found. ")
            else:
                print("it is not expected to be in Dashboard as the test already failed")
        else:
            if tr:
                message = message + " and Dashboard activity Reach confirmed"
            else:
                message = 'the activity is not expected to reach in Dashboard as the test already failed' + " But the Activity UNEXPECTEDLY reached Dashboard "
           
        print(message)
        
    except Exception as e:
        # self.fail("Encountered an unexpected exception.test failed in "+test_name)
        print(e)
        save_screenshot(d, test_name)
        status = "FAIL"
        traceback.print_exc()
        message = e 
        tr = False
        
        # print(error_message)  
    
    finally:
        testcasereport(test_name,status,message)
        return tr

#sample code for feeder for reference remove it after development
def xxxxxxxxxpaybywalletfeeder(self):
    d = self.driver
    driver = d
    tr = False
    test_name1 = 'paybywalletfeeder'
    message = ""
    finaltr = ''
    feederresult = {}
    tc1 = tc2 = tc3 = False
    status = True
   
    fullmessage = ""
    respmesg = ''
    global feedercheck
    

    try:
        print("\n\n")
        global fcsv
        fcsv = format_csv(csvpath) 
        print(fcsv)
        print(fcsv.keys())
        # success only if csv has value
        # print(0/0)
        print("turning off force")
        
        force = False
        print("this is force::::::::::::::",force)
        if force: #ensure minimum balance, if false , test will continue without trying to add money,
            #which might shows failed
            #check balance needed
            totalamountinfeeder = sum(float(dkey['amount']) for dkey in fcsv.values() if dkey)
            print("this is total amount needed :",totalamountinfeeder)
            
            currentbalance = go_and_check_dashboardbalance(d)
            print("current balance = ",currentbalance)
            
            if (currentbalance is None):
                print("current balance fetch is unsuccessful")
                raise failed(test_name1,"current balance is unfetchable")
                
            else:
                print("current balance check successfull",currentbalance)

                
            if currentbalance>=totalamountinfeeder:
                print("minimum amount is available. Current balance = ",currentbalance)
            else:
                #call add money to input required balance.
                print("proceeding to add money feeder total amt :",totalamountinfeeder,"current balance :",currentbalance)
                
                addamount = 10**(len(str(abs(int(totalamountinfeeder))))) #rounding the figure to higher value
                
                if addamount > addmoneyupperlimit: # check the limit
                    if totalamountinfeeder - currentbalance >addmoneyupperlimit : #possible way to pass the condition
                        raise failed(test_name1,"the total feeder amount '",totalamountinfeeder,"' exceeds the 'add money upper limit '",addmoneyupperlimit  )
                    else:
                        addamount = totalamountinfeeder - currentbalance
                else:
                    ... # amount can be added
                    pass
                        
                        
                        
                if(d.current_activity != dashboardactivity):
                    back_to_dashboard(d)
                add_money_click(self)
                try:
                    
                    addmoneysuccess = add_money_to_wallet_from_input(self,addamount,test_name = 'feeder')
                    # addmoneysuccess = add_money_to_wallet_from_card_by_BHD_40_button(self)
                except Exception as e:
                    addmoneysuccess = False
                    print(e) 
                    
                if not addmoneysuccess:
                    print("add money failed with force on , and there is no balance to continue")
                    tr = 'warn'
                    raise failed(test_name1,'add money failed with force on , and there is no balance to continue')
                    
        else:
            #only check balance needed
            totalamountinfeeder = sum(int(dkey['amount']) for dkey in fcsv.values() if dkey)
            print("total amount needed :",totalamountinfeeder)
        #dictionary is not empty
        # print("fcsv.items():::::::::::::::::::::::::::::::::::::::::::::::::::::\n",fcsv.items())
        # print("\n\nfcsv lenght LLLLLLLLLLLLLLLLLLLLL",len(fcsv.keys()))
        if len(fcsv.keys())>0:
            for key,value in fcsv.items():
                print("⣿"*os.get_terminal_size().columns)
                print("\n\u001b[4m\u001b[44m STARTING NEW TEST WITH TEST DATA -\u001b[0m")
                print(key ," : ", list[value])
                print(CRESET+"."*os.get_terminal_size().columns)
                #initialising key value
                feederresult.update({key:dict()})
                feederresult[key].update({'status':False})
                feederresult[key].update({'tc1':str(tc1)})
                feederresult[key].update({'tc2':str(tc2)})
                feederresult[key].update({'tc3':str(tc3)})
                try:
                    d_status = back_to_dashboard(d,minimal=True)
                    if d_status:
                        p2p_click_status = p2p_click2(self,minimal=True)
                        if p2p_click_status:
                            resp,respmesg = paytoperson(self,cpr = key,amount = fcsv[key]['amount'])
                            print("\u001b[1m CHECKING FOR TESTPASS CONDITIONS \u001b[0m")
                            print("_"*os.get_terminal_size().columns)
                            
                            tc1 = checkassert(d,d_status,'==',True,'Task_1: reach Dashboard success')
                            tc2 = checkassert(d,p2p_click_status,'==',True,'Task_2: activity clicked P2p')
                            tc3 =checkassert(d,resp,'==',True,'Task_3: sendCPR = '+str(key)+';Amount = '+str(fcsv[key]['amount']))
                            if not tc3:
                                now = datetime.now()
                                current_time = str(now.strftime("%H-%M-%S"))
                                save_screenshot(d,'Task3:sendCPR'+str(key)+';Amt'+str(fcsv[key]['amount'])+current_time)
                                print("saving screenshot"+YELLOW)
                            print("below is tc1 ,tc2 ,tc3")
                            print(tc1 , tc2 , tc3)
                            if tc1 & tc2 & tc3 :
                                print(CYAN+"TEST P2P PASSED FOR CPR : ",str(key),' .for amount : ',str(fcsv[key]['amount']),CRESET)
                                feederresult[key].update({'status':'passed'})
                                feederresult[key].update({'tc1':str(tc1)})
                                feederresult[key].update({'tc2':str(tc2)})
                                feederresult[key].update({'tc3':str(tc3)})
                                tr =True
                            else:
                                if not tc3:
                                    feederresult[key].update({'status':'failed'})
                                    feederresult[key].update({'tc1':str(tc1)})
                                    feederresult[key].update({'tc2':str(tc2)})
                                    feederresult[key].update({'tc3':str(tc3)})
                                    status = False
                                    tr = False 
                                else:
                                    feederresult[key].update({'status':'failed'})
                                    feederresult[key].update({'tc1':str(tc1)})
                                    feederresult[key].update({'tc2':str(tc2)})
                                    feederresult[key].update({'tc3':str(tc3)})
                                    status = 'warn' if status else False
                                    tr = False 
                                    
                            print("TEST STATUS :: ",status)
                                    
                        else:
                            
                            print("P2P click failed")
                            tr =checkassert(d,p2p_click_status,'==',True,'task: sendCPR = '+str(key)+';Amount = '+str(fcsv[key]['amount']))
                            status = 'warn'
                            break

                    else:
                        print("Dashboard activity failed")
                        status = 'warn'
                        tr = checkassert(d,d_status,'==',True,'task: sendCPR = '+str(key)+';Amount = '+str(fcsv[key]['amount']))
                        break
                    print("this is tr after everything",tr)
                    
                except Exception as e:
                    print(e)
                    # if message == "" :
                    #     message = "message not specified"
                    message = e
                finally:
                    # print(fcsv)
                    if finaltr == '':
                        finaltr = tr
                    elif finaltr == tr:
                        pass #false == false | true ==true
                    else: #finaltr == True and tr == False or finaltr == False and tr == True or any WARN
                        finaltr = 'Warn'
                        
                            
                    print(YELLOW)
                    print('TC data :')
                    print(PURPLE)
                    print('Name :',fcsv[key]['name'])
                    print('cpr :',fcsv[key]['cpr'])
                    print('Mobile :',fcsv[key]['mobile'])
                    print('amount :',fcsv[key]['amount'])
                    if respmesg != 'message not specified' or respmesg != '' :
                        print('reason : ',respmesg)
                    print(CRESET+"\u001b[1m")
                    print('TC1:REACH DASHBOARD',feederresult[key]['tc1'])
                    print('TC2:CLICK ON P2P BUTTON IN DASHBOARD',feederresult[key]['tc2'])
                    print('TC3:SEND MONEY',feederresult[key]['tc3'])
                    print(CRESET)
                    if respmesg in ['' ,None , 'message not specified']:
                        respmesg = message
                    teststatus =feederresult[key]['tc1'].lower() and feederresult[key]['tc2'].lower() and feederresult[key]['tc3'].lower() in ('pass', "true", 'passed')
                    testcasename = str(fcsv[key]['testcase']) if str(fcsv[key]['testcase']) is not (None or '') else 'send BHD '+str(fcsv[key]['amount'])+' to CPR '+fcsv[key]['cpr']
                    # print("\n\n\n\n\n\n\n\n")
                    # print(type(tr))
                    # print(type(fcsv[key]['expect']))
                    # print("::::::n\n\nXXXXX"+str(fcsv[key]['testcase'])+"XXXXX\n\nn")
                    # print("this is tesct case::::\n\n",str(fcsv[key]['testcase']) is not None or '')
                    # print("this is tescstcases :::::::",testcasename,":::::::::\n\n\n")
                    currenttr = tr not in [False,'false','False','FALSE','FAIL','Fail','fail','WARN','Warn','warn']

                    if fcsv[key]['expect'] in [False,'false','False','FALSE','FAIL','Fail','fail']:
                        expected = False
                    else:
                        expected = True
                    if tr == expected:
                        finalres = 'Passed'
                    else: 
                        finalres = 'Failed'
                    
                    # print("tr===fcsv[key]['expect']",tr==fcsv[key]['expect'])
                    print("test result is expected to be",expected,"\nIs the result expected? ",tr==expected)
                    feedercheck['paybywallet'].append({'name':fcsv[key]['name'],
                                              'cpr':fcsv[key]['cpr'],
                                              'amount' :fcsv[key]['amount'],
                                              'testcase' :testcasename,
                                              'status':tr,
                                              'reason':respmesg,
                                              'expected':fcsv[key]['expect'],
                                              'final_Result':finalres })
                    if teststatus:
                        # feedercheck['paybywallet']['pass'] =  1 if not feedercheck['paybywallet']['pass'] else feedercheck['paybywallet']['pass'] +1
                        feedercheck['pass'] =feedercheck['pass']+1
                    else:
                        # feedercheck['paybywallet']['fail'] =  1 if not feedercheck['paybywallet']['fail'] else feedercheck['paybywallet']['fail'] +1
                        
                        feedercheck['fail'] =feedercheck['fail']+1
                    ##############################################3
                    ############################################3
                    
                    #do expect value check
                    ##########################################
                    # feedercheck['failedtestcases'][x].values()
                    print("tc for fcsv["+key+"] : completed ")
        else:
            print("\n\nCSV has no Value\n")
            tr = False
        # print("logic incomplete")
    except failed as e:
        print( LIGHTGREY+ "FULL ERROR PRINT",str(e) +"\n\n"+ traceback.format_exc() , CRESET)
        
        message = RED + e.message +CRESET
        tr = False
        
    except Exception as e:
        print("this is failed exception")
        # fullmessage = str(e) +"\n\n"+ traceback.format_exc()
        print( LIGHTGREY+ "FULL ERROR PRINT",str(e) +"\n\n"+ traceback.format_exc() , CRESET)
        message = RED +e.args[1] +CRESET
        tr = False
    except:
        print("this is something")
    else:
        print("this is in else of try catch")
    finally:

        print("\033[;34m\033[47m Execution of Test "+test_name1+" completed..!")
        print("Final STATUS calculated :",finaltr)
        print("Test result = "+str(tr) +"\033[m\033[0m")
        status = finaltr
        # print(feederresult)
        # print("\n\n",feedercheck['paybywallet'])
        #pay_wallet_feeder_testreport
        exceltestreport('paybywallet',feedername = "")
        # print("\n\n",feedercheck['pass'])
        # print("\n\n",feedercheck['fail'])
        if status == 'Warn' or 'warn':
            message = YELLOW+"SOME TEST CASES IN FEEDPAYBYWALLET FAILED \n  "+CRESET +message
        elif status == True:
            message = GREEN+"ALL FEEDPAYBYWALLET TEST CASES PASSED \n  "+CRESET +message
        elif status == False:
            message = RED+"ALL FEEDPAYBYWALLET TEST CASES FAIlED \n  "+CRESET +message
            
        testcasereport(test_name1,status,message )
        return finaltr