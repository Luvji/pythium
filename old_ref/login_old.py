
from customclasses import failed, splashloadtooklong
from util import *
from config import *
from util import wait_until_activity
from time import sleep
import traceback
from selenium.webdriver.common.by import By
# import base64

def signin_with_cpr(self):
        test_name = 'signup_with_cpr_with_unknown_number'
        message = 'unexpected error occured in '+test_name
        status = "FAIL"
        try:
            #activity not implemented
            d = self.driver
            driver = d
            # test_name: str = ("test_login")
            splashactivity ="com.bfc.bfcpayments.modules.splash.view.SplashScreenActivity"
            splash_loads_ok = wait_until_activity(d,splashactivity,"notvisible")
            if not splash_loads_ok:
                raise splashloadtooklong({"message":"splash screen took too long to load", "test_name":test_name}) 
            #below code just ensures that it has reached the specific page to begin test.
            #
            print("etcpr",len(self.driver.find_elements_by_id('etCPRNumber')) > 0,"textwelcome", len(self.driver.find_elements_by_id("txtWelcomeBack"))>0)
            if not len(self.driver.find_elements_by_id('etCPRNumber')) > 0 and len(self.driver.find_elements_by_id("txtWelcomeBack"))>0:
                print("no etcprnumber and yes txtwelcome back")
                print(self.driver.find_elements_by_id("txtWelcomeBack"))
                
                print("signup/long signin skipped, seems like already signed up, did you set pin login check?")  # needs pin login check
            elif len(self.driver.find_elements_by_id('etCPRNumber')) > 0 and not len(self.driver.find_elements_by_id("txtWelcomeBack"))>0:
                print("len(self.driver.find_elements_by_id('etCPRNumber')) > 0",len(self.driver.find_elements_by_id('etCPRNumber')))
                print("len(self.driver.find_elements_by_id('txtWelcomeBack'))>0",len(self.driver.find_elements_by_id("com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack")))
            else:
                if d.current_activity != "com.bfc.bfcpayments.modules.login.view.MainActivity":
                    print("the view is not in main activity, trying to sleep 5 second.")
                    print("if this fails frequently , write logic to get to dashboard")
                    printblue("sleeping starts now")
                    sleep(5)
                else:
                    print("the view is in main activity")
                    printred("this logic isnt written, might never want to... IDK ;D")
                    ...
            
            print("test started , checking for login strategy")
            if len(d.find_elements_by_id('etCPRNumber')) > 0 and d.find_element_by_id("txtWelcomeDialog").is_displayed():  # pay attention: find_element*s*
                print("seems app isn't logged in and need to signin first")
                sleep(2)
                etCPRNumber = d.find_element_by_id('etCPRNumber')
                waitfor(d,"etCPRNumber")
                etCPRNumber.click()  # pay attention: find_element ,cpr text field
                print("entering cpr : ",loggedcpr)
                d.find_element_by_id('etCPRNumber').send_keys(loggedcpr)  # cpr text field
                check_and_hide_keyboard(d)
                eltnccpr = d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/checkBoxTnCCPR")
                eltnccpr.click()  # tnc accepted
                d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/btnVerifyCPR").click() #proceed button
                d.find_element_by_id("txtWelcomeDialog").is_displayed()
                sleep(1)
                # android.widget.TextView[@text = 'Mobile Number']
                _txtmobileid = "com.bfccirrus.bfcpayments.mobile:id/txtMobileNo"
                wait_until(d,_txtmobileid,"visible")
                txtMobileNo = d.find_element_by_id(_txtmobileid)
                checkassert(d,txtMobileNo.text,"==","Mobile Number")
                if (txtMobileNo.is_displayed()):
                    print("mobile number page is visible")
                print("entering new mobile : 333333333")
                d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/etPhoneNumber").send_keys("333333333")
                sleep
                d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/btnRegisterPhone").click()
                sleep(2)
                # check = d.find_element_by_xpath("//android.widget.TextView[@text = 'Another registered mobile number found']").is_displayed()
                anothermobiletext = wait_until(d,"//android.widget.TextView[@text = 'Another registered mobile number found']","visible")
                
                check = checkassert(d,anothermobiletext,"==",True,"check another mobile text")
                #below check must be deprecated
                if not check:
                    print("element text not visible. proceeding with test though")
                else:
                    print("alternate mobile number view is visible")
                # rbtn1 = d.find_element_by_xpath("//android.widget.RadioButton[@text = '+973 6****011']")
                formattednumber = loggedmobile[0]+"****"+loggedmobile[5:8] #making it into format = 6****011
                rbtn1 = d.find_element_by_xpath("//android.widget.RadioButton[@text = '+973 "+formattednumber+"']")
                print("radio button checked?",rbtn1.get_attribute("checked"))
                print("radio button is selected with the mobile number text '+973 "+formattednumber+"'")
                d.find_element_by_xpath("//android.widget.Button[@text = 'Proceed']").click()
                _txtOTP = "com.bfccirrus.bfcpayments.mobile:id/txtOTPVerification"
                wait_until(d,_txtOTP,"visible")
                txtMobileNo = d.find_element_by_id(_txtOTP)
                
                check = checkassert(d,txtMobileNo.text,"==","OTP Verification")
                # check = d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/txtOTPVerification").is_displayed()
                if not check:
                    print("element text not visible. proceeding with test though")
                else:
                    print("OTP view is visible")
                sleep(1)
                class_list = d.find_elements_by_class_name("android.widget.EditText")
                # print(class_list)
                for singlefield in class_list:
                    singlefield.send_keys("1")
                print("setting 1 in each field")
                d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/btnRegisterOtp").click()
                sleep(2)
                id ="com.bfccirrus.bfcpayments.mobile:id/txtDOB"
                wait_until(d,id,"==",'Verify Date Of Birth')
                d.find_element_by_xpath("//android.widget.TextView[@text = 'Verify Date Of Birth']").click() 
                print("DOB verification in process - adding date 21/04/1990 ")
                print("selecting day - "+bday)
                day = d.find_element_by_xpath("//android.widget.TextView[@text = 'Day']")
                day.click()
                daytextxpath ="//android.widget.TextView[@text = '"+bday+"']"
                print("daytextxpath",daytextxpath)
                scroll_on_element(d,daytextxpath,start_x=248, start_y=1608,
                                                            end_x=243, end_y=1066)
                _bday = d.find_element_by_xpath(daytextxpath) 
                _bday.click()

                print("selecting month - 04")
                month = driver.find_element(By.XPATH,
                                            "//android.widget.TextView[@text = 'Month']")
                month.click()
                _monthtextxpath = "//android.widget.TextView[@text = '"+bmonth+"']"
                scroll_on_element(d,_monthtextxpath,start_x=476, start_y=1343,
                                        end_x=471, end_y=1196)
                # 32. Click 'mm'            
                _month = driver.find_element(By.XPATH,
                                        _monthtextxpath)
                _month.click()

                # 33. Click 'YYYY'
                yyyy = driver.find_element(By.ID,
                                        "com.bfccirrus.bfcpayments.mobile:id/etDOBYear")
                yyyy.click()

                # 34. Type '####' in 'YYYY'
                yyyy = driver.find_element(By.ID,
                                        "com.bfccirrus.bfcpayments.mobile:id/etDOBYear")
                yyyy.send_keys(byear)

                # print("\n\nmonths",months)
                print("typing year ",byear)
                
                # year =  d.find_element_by_xpath("//android.widget.TextView[@text = 'YYYY']")
                # year.send_keys(1990)
                # print("year selected")
                check_and_hide_keyboard(d)
                
                sleep(1)
                d.find_element_by_xpath("//android.widget.Button[@text = 'Proceed']").click()
                waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/circleField")
                print("entering pin creation")
                pincreation = d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/circleField")
                if(pincreation.is_displayed()):
                    print("PIN creation page reached")
                    txt = d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/txtSetupPin").text
                    print("text of current screen is '"+txt+"'")
                    pincreation.click()
                    pincreation.send_keys(loggeduserpin)
                    
                else:
                    raise failed 
                # id	@id/txtSetupPin
                # pincreation = d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/circleField")
                txt2 = d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/txtSetupPin").text
                # waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/circleField")
                id = "com.bfccirrus.bfcpayments.mobile:id/txtSetupPin"
                print("waiting to confirm PIN")
                
                wait_until(d,id,"==","Confirm PIN")
                print("checking assert here")
                # assert(txt2 == "Confirm PIN")
                # wait_until(d,locatorstring,condition ="==",checker ="",sec = 15, iterate = .5)
                
                if(pincreation.is_displayed()):
                    print("PIN creation page reached")
                    txt = d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/txtSetupPin").text
                    print("text of current screen is '"+txt+"'")
                    pincreation.click()
                    pincreation.send_keys(loggeduserpin)
                    print("confirmed pin")
                print("checking if the page view reached dashboard")
                sleep(3)
            elif not len(self.driver.find_elements_by_id('etCPRNumber')) > 0 and len(self.driver.find_elements_by_id("com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack"))>0:
                printred("app is already logged in. if not intended it is a FAIL")
                c1 = driver.find_element(By.ID,"txtWelcomeBack")
                print("\nc1:::::::::::::",c1.text)
                if (checkassert(d,c1.text ,"contains",loggedname)):
                    c1.click()
                    # 2. Type '123321' in 'com.bfccirrus.bfcpayments.mobile:id/c...1'
                    com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_1 = driver.find_element(By.ID,
                                                                                            "circleField")
                    com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_1.send_keys(str(loggeduserpin))
                else:
                    print("the logged in user is not intended user,restart login process")
                    print("logged in user",c1.text.strip('Welcome Back,'),"intended user",loggedname)
                    self.driver.find_element_by_id('txtForgotPin').click()
                    waitfor(d,"etCPRNumber")
                    signin_with_cpr(self) 
            else:
                print("len(self.driver.find_elements_by_id('etCPRNumber')) > 0",len(self.driver.find_elements_by_id('etCPRNumber')))
                print("len(self.driver.find_elements_by_id('txtWelcomeBack'))>0",len(self.driver.find_elements_by_id("com.bfccirrus.bfcpayments.mobile:id/txtWelcomeBack")))

                message ="something unexpected happened"
                print(message)
                status = "failed"
                raise failed
            check = wait_until_activity(d,'com.bfc.bfcpayments.modules.home.view.DashboardActivity','visible') 
            if (checkassert(d,check,"==",True)):
                status = "PASS"
                message = "Test passed Successfully"
                return True
            else:
                status = "FAIL"
                message = "activity is not in dashboard , it is currently in "+d.current_activity
                return False
        except:
            # self.fail("Encountered an unexpected exception.test failed in "+test_name)
            save_screenshot(d, test_name)
            status = "FAIL"
            # traceback.print_exc()
            message = traceback.format_exc()
            
            # print(error_message)  
            return False
        finally:
            testcasereport(test_name,status,message)
           
