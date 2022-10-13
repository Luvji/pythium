
from customclasses import failed, splashloadtooklong
from util import *
from config import *
# from util import wait_until_activity
from time import sleep
import traceback
from selenium.webdriver.common.by import By


def enterdate(self,dateselected = loggeddob):
    d = driver = self.driver

    dob = dateselected.rsplit("-") #['2009', '03', '20']
    bday =  dob[2]    #format dd
    bmonth =  dob[1]  #format mm
    byear =  dob[0] #format yyyy
    print("DOB verification in process - adding date ",dateselected)
    print("selecting day - "+bday)
    day = d.find_element_by_xpath("//android.widget.TextView[@text = 'Day']")
    day.click()
    daytextxpath ="//android.widget.TextView[@text = '"+bday+"']"
    print("daytextxpath",daytextxpath)
    scroll_on_element(d,daytextxpath,start_x=248, start_y=1608,
                                                end_x=243, end_y=1066)
    _bday = d.find_element_by_xpath(daytextxpath) 
    _bday.click()
    print("selecting month - ",bmonth)
    _month = driver.find_element(By.XPATH,
                                "//android.widget.TextView[@text = 'Month']")
    _month.click()
    _monthtextxpath = "//android.widget.TextView[@text = '"+bmonth+"']"
    scroll_on_element(d,_monthtextxpath,start_x=476, start_y=1343,
                            end_x=471, end_y=1196)
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
    #clicking on proceed
    d.find_element(By.ID,"imgEmail").click() # proceed button
    


def signin_with_cpr(self):
    test_name = 'signup_with_cpr_with_known_number'
    message = 'unexpected error occured in '+test_name
    status = "FAIL"
    d = driver = self.driver
    tr =False

    try:
        print("checking the entry gateway as signup or signin")
        if not len(d.find_elements(By.ID,"txtHeading")) > 0 and len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack"))>0:
            print("signin flow")
            tr,message = signinwithpin(self,minimal=True)
            if tr == True:
                status = "PASS"
                # message = "sign in with pin success"
            else:
                status = "FAIL"
                # message = "not reached the dashboard , call_check dashboard here"
            
        elif len(d.find_elements(By.ID,"txtHeading")) > 0 and not len(d.find_elements(By.ID,"txtWelcomeDialog")) > 0: #d.find_element_by_id("txtWelcomeDialog").is_displayed():
            print("signupflow")
            print("this is activity")
            signupwelcometext = d.find_element(By.ID,"txtHeading").text
            if not checkassert(d,signupwelcometext ,"==","International money transfers at great rates","welcome text displayed?"):
                raise splashloadtooklong 
            
            print("clicking on the register button")
            d.find_element(By.ID,"btnRegister").click()
            
            entercprlabel = d.find_element(By.ID,"txtLabelEnterCpr").text
            checkassert(d,entercprlabel ,"==","Enter your CPR number","enter CPR label displayed?")
            
            print("entering cpr , ",loggedcpr)
            entercpr = d.find_element(By.ID,"edtCPR")
            entercpr.send_keys(loggedcpr)
            
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
                print(YELLOW+"\n\n\n\nthis is hardecoded in here, \n\n\n\n"+CRESET)
                # rbtn = d.find_element(By.XPATH,"//android.widget.RadioButton[@text = '+973 3****369']")
                # rbtn1 = d.find_element_by_xpath("//android.widget.RadioButton[@text = '+973 "+formattednumber+"']")
                # print("radio button checked?",rbtn1.get_attribute("checked"))
                # print("radio button is selected with the mobile number text '+973 "+formattednumber+"'")
                d.find_element_by_xpath("//android.widget.Button[@text = 'Proceed']").click()
            
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
                
                raise failed(test_name,"Alert :"+snackbartext)
                
            print("proceed button clicked , reaching onto mobile number page:")
            # id	@id/txtVerifyDobLabel
            lblverifydate = d.find_element(By.ID,"txtVerifyDobLabel").text
            
            checkassert(d,lblverifydate ,"==","Verify date of birth","verify date page reached?")
            
            #####
            # verifying dates id	@id/etDOBDay
            # d.find_element(By.ID,"etDOBDay").click()
            #//android.widget.TextView[@text = 'Day']
            
            #//android.widget.TextView[@text = '01']
            
            # adding date as function
            enterdate(self)
             

            # print("\n\nmonths",months)
            if len(driver.find_elements(By.ID,'txtHeading'))>0:
                # id	@id/btnOk text	DOB Verification
                if driver.find_element(By.ID,'txtHeading').text == 'DOB Verification':
                    print("dob change sscreen shown")
                    # id	@id/btnOk
                    driver.find_element(By.ID,'btnOk').click()
                    
                else:
                    print("new screen found but it is not dob")
                    save_screenshot(d)
                
            # txtHeading
            
            # year =  d.find_element_by_xpath("//android.widget.TextView[@text = 'YYYY']")
            # year.send_keys(1990)
            # print("year selected")
            check_and_hide_keyboard(d)
            # id	@id/imgEmail txtLabelSetMpin
            txtLabelSetMpin = d.find_element(By.ID,"txtLabelSetMpin").text
            checkassert(d,txtLabelSetMpin ,"==","Set a PIN","Pin set page reached?")
            
            #id	@id/edtPin  id	@id/edtConfirmPin
            print("confirming pin")
            d.find_element(By.ID,"edtPin").send_keys(loggeduserpin)
            print("OTP entered ,confirming otp now")
            d.find_element(By.ID,"edtConfirmPin").send_keys(loggeduserpin)
            print("pin entered is",loggeduserpin,"now clicking proceed")
            # check_and_hide_keyboard(d)
            check_progressbar(d)
            # d.find_element(By.ID,"btnSubmit").click()
            # id	@id/txtPersonName
            loggedpersonname = d.find_element(By.ID,"txtPersonName").text

            tr = checkassert(d,loggedpersonname ,"==",loggedname,"checking logged name is :"+loggedname+"?")
            if tr == True:
                status = "PASS"
            else:
                status = "Fail"
                message = "not reached the dashboard , call_check dashboard here"
                
        else:
            print("this is else in signup !!!,this means normal flow is not working")
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
                    
                    shufti_initiation(self,minimal = True)
                else:
                    print("Unknown ")
            else:
                print("it is not expected to be in Dashboard as the test already failed")
        else:
            if tr:
                message = message + " and Dashboard activity Reach confirmed"
            else:
                print("the activity is not expected to reach in Dashboard as the test already failed")
                message = message + " But the Activity UNEXPECTEDLY reached Dashboard "
           
        
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
    
def signinwithpin(self,minimal = False):
    """
    minimal : true doesnt call test report
    returns 2 variables if minimal
    
    """
    test_name = 'signin_with_pin'
    message = 'unexpected error occured in '+test_name
    status = "FAIL"
    d = driver = self.driver
    tr =False
    try:
        d = driver = self.driver
        # id	@id/txtWelcomeBack
        print("checking for sign in strategy")
        if not len(d.find_elements(By.ID,"txtHeading")) > 0 and len(d.find_elements(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack"))>0:
            printred("app is already logged in. if not intended it is a FAIL")
            c1 = driver.find_element(By.ID,"txtWelcomeBack")
            print("\nwelcome back text :::::::::::::",c1.text)
            if (checkassert(d,c1.text ,"contains",loggedname," intended user check")):
                c1.click()

                com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_1 = driver.find_element(By.ID,
                                                                                        "circleField")
                com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_1.send_keys(str(loggeduserpin))
                check_progressbar(d)
                # d.find_element(By.ID,"btnSubmit").click()
                # id	@id/txtPersonName
                print("checking for dashboard activity visibility",d.current_activity == dashboardactivity)
                loggedpersonname = d.find_element(By.ID,"txtPersonName").text
                tr = checkassert(d,loggedpersonname ,"==",loggedname,"checking logged name in dashboard is :"+loggedname+"?")
                if tr == True:
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
                    signin_with_cpr(self)
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
        

def shufti_initiation(self,minimal = True):
    test_name = 'signup_with_cpr_with_known_number'
    message = 'unexpected error occured in '+test_name
    status = "FAIL"
    d = driver = self.driver
    tr =False
    if d.find_element(By.ID,'txtVerifyDobLabel') and d.find_element(By.ID,'txtVerifyDobLabel').text == 'Consent for verification':
        print("shufti initiation started")
        
        
        
        
        tr = True
        status = "incomplete"
    else:
        print("shufti couldnt be initialted as consent screen not found")
        
    
    
    # id	@id/text	
    
    
    




#