from customclasses import failed
from util import *
from time import sleep
from selenium.webdriver.common.by import By
from login import signin_with_cpr


def p2p_click(self):
    try:
        test_name = "p2p_click"
        tr = False    #test result variable to return value
        d = self.driver
        occurred = 0
        
        #TO_DO: LEARN HOW TO STARTACTIVITY DYNAMICALLY #done
        # d.start_activity("com.bfccirrus.bfcpayments.mobile", "com.bfc.bfcpayments.modules.home.view.DashboardActivity")
        curractivity = d.current_activity
        print("currentactivity ::::::::",curractivity)
        if(curractivity != "com.bfc.bfcpayments.modules.home.view.DashboardActivity" or curractivity =="com.bfc.bfcpayments.modules.pay.view.PayMainActivity"):
            print("activity is not in dashboard or pay main activity,proceeding to get to dashboard")
            dashboardstatus = back_to_dashboard(d)
            if dashboardstatus == "signup":
                signin_with_cpr()
            wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible")
        if(curractivity == "com.bfc.bfcpayments.modules.home.view.DashboardActivity"):
            print("(15)proceeding to click and navigate to entity :"+test_name)
           
            print("dashboard found")
            txtwelcome_id = "com.bfccirrus.bfcpayments.mobile:id/txtWelcome"
            wallet_id = "com.bfccirrus.bfcpayments.mobile:id/cardWallet"
            textwelcomevisibility = True
            textwelcomevisibility = wait_until(d,txtwelcome_id,"visible","",1)

            wait_until(d,wallet_id,"visible")
            # 2. Make a Swipe gesture from ('708','1628') to ('728','802')
            d.swipe(start_x=708, start_y=1628, end_x=728, end_y=802, duration=300)
            paywalletcard = d.find_element_by_xpath("//android.widget.TextView[@text = 'Pay Wallet']")
            if(len(d.find_elements_by_xpath("//android.widget.TextView[@text = 'Pay Wallet']"))== 1):  #note elements
                paywalletcard.click()
                wait_until(d,"com.bfccirrus.bfcpayments.mobile:id/txtAppbarTitle","visible")            
                # print("show dashboard screen needs to be implemented yet")
            # save_screenshot(d, test_name)
            message = "Test "+test_name+" Successful"
            status = "PASS"       
            tr = True
                # return tr
            # except:
            #     # self.fail("Encountered an unexpected exception.test failed in "+test_name)
            #     save_screenshot(d, test_name)
            #     status = "FAIL"
            #     # traceback.print_exc()
            #     message = traceback.format_exc()
                
            #     message = message +"\nclick failed, check everything!. did you check the screen? \n"
            #     tr = False
            # finally:
            #     print("\033[1;34m\033[47m Execution of Test \033[0;30m\033[47m"+test_name+"\033[1;37m\033[47m completed..!\033[0m")
            #     print("Test result = "+str(tr) +"\033[m\033[0m")
            #     testcasereport(test_name,status,message)
            #     return tr
        elif(curractivity =="com.bfc.bfcpayments.modules.pay.view.PayMainActivity"):
            print("already in screen "+curractivity+" pass")
            wait_until(d,"com.bfccirrus.bfcpayments.mobile:id/txtSendTo","visible")            
            txtSendTo = d.find_element(By.ID,
                                                "com.bfccirrus.bfcpayments.mobile:id/txtSendTo")
            check = checkassert(d,txtSendTo.text ,"==","Send to")
            if check:
                message = "the screen is in pay wallet screen"
                status = "PASS"       
                tr = True
            else:
                if not occurred:
                    print("seems it is in screen  but different fragent trying heal")
                    occurred +=1
                    tr = "FAIL" #not returning the value to self heal
                    back_to_dashboard(d)
                    wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible")
                    p2p_click(self)
                    
                else:
                # start_activity(self, appPackage, dashboard_activity)
                # d.start_activity("com.bfccirrus.bfcpayments.mobile", "com.bfc.bfcpayments.modules.home.view.DashboardActivity")
                    print("p2p is failed")
                    save_screenshot(d, test_name)
                    message = traceback.format_exc()
                    status = "FAIL"       
                    tr = False
                    return tr
                    #check for force heal : if force heal do this: right now getting it straight
                    
        else:
            print("view is not in dashboard or p2p click")
            print("currentactivity ::::::::",curractivity)
            if not occurred:
                occurred +=1
                tr = "FAIL" #not returning the value to self heal
                back_to_dashboard(d)
                wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible")
                p2p_click(self)    
            else:
            # start_activity(self, appPackage, dashboard_activity)
            # d.start_activity("com.bfccirrus.bfcpayments.mobile", "com.bfc.bfcpayments.modules.home.view.DashboardActivity")
                print("p2p is failed")
                save_screenshot(d, test_name)
                message = traceback.format_exc()
                status = "FAIL"       
                tr = False
                return tr
    # except:
    #     raise failed("click failed, check everything!. did you check the screen?")
                
    except Exception as e: # work on python 3.x
        save_screenshot(d, test_name)
        message = traceback.format_exc()
        status = "FAIL"       
        tr = False
        print('ERROR MESSAGE: '+ str(e))
    # except:
    #     # self.fail("Encountered an unexpected exception.test failed in "+test_name)
    #     save_screenshot(d, test_name)
    #     status = "FAIL"
    #     # traceback.print_exc()
    #     message = traceback.format_exc()
        
    #     message = message+RED +"\nclick failed, check everything!. did you check the screen? \n"+GREEN
    #     tr = False
        # print(error_message)  
        # return False
    finally:
        print("\033[1;34m\033[47m Execution of Test \033[0;30m\033[47m"+test_name+"\033[1;37m\033[47m completed..!\033[0m")
        print("Test result = "+str(tr) +"\033[m\033[0m")
        testcasereport(test_name,status,message)
        return tr

def add_money_click(self):
    test_name = "add_money_click"
    tr = False    #test result variable to return value
    d = self.driver
    driver = d
    curractivity = d.current_activity   
    once = 0 # special variable for click functions to stop recursive hell
    #implement better logic if you got one.
    print("proceeding to click and navigate to entity :"+test_name)
    wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible",7)
    if(curractivity == "com.bfc.bfcpayments.modules.home.view.DashboardActivity"): # or curractivity == "com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity"):
        # check for same page not implemented
        print("current activity already in dashboard or add money page")
        pass 
    else:
        print("not in dashboard view and check for same page not implemented,re reouting to dashboard")
        back_to_dashboard(d)
    try:
            txtwelcome_id = "com.bfccirrus.bfcpayments.mobile:id/txtWelcome"
            wallet_id = "com.bfccirrus.bfcpayments.mobile:id/cardWallet"
            textwelcomevisibility = wait_until(d,txtwelcome_id,"visible")
            checkassert(d,textwelcomevisibility,"==",True,"welcome text in dashboard")
            check = wait_until(d,wallet_id,"visible") 
            checkassert(d,check,"==",True,"checking wallet id visibility")
            # swipe in dashboard to view add money ('764','1182') to ('781','450')
            driver.swipe(start_x=764, start_y=1182, end_x=781, end_y=450, duration=300)
            # 6. Click 'com.bfccirrus.bfcpayments.mobile:id/c...7'
            ### BETTER XPATH WRITTEN BELOW
            # com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_7 = driver.find_element(By.XPATH,
            #                                                                         "//androidx.cardview.widget.CardView[6]")
            # com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_7.click()

            #  # swipe in dashboard to view add money('538','1577') to ('553','287')
            # driver.swipe(start_x=538, start_y=1577, end_x=553, end_y=287, duration=300)

            # 5. Click 'com.bfccirrus.bfcpayments.mobile:id/i...2'
            com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_2 = driver.find_element(By.XPATH,
                                                                                    "//android.widget.TextView[@text = 'Add Money']")
            com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_2.click()
            check = wait_until_activity(d,"com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity","visible")
            checkassert(d,check,"==",True,"checking add money activity")

            # 6. Click 'Pay'
            # pay = driver.find_element(By.ID,
            #                         "com.bfccirrus.bfcpayments.mobile:id/txtAppbarTitle")
            # pay.click()
            status = "PASS"
            message = "Add money click is successfull"
            tr = True
            print("sleeping for 2 second")
            sleep(2)
            
    except Exception as e: # work on python 3.x
        save_screenshot(d, test_name)
        message = traceback.format_exc()
        status = "FAIL"       
        tr = False
        print('ERROR MESSAGE: '+ str(e))
    except:
        # self.fail("Encountered an unexpected exception.test failed in "+test_name)
        save_screenshot(d, test_name)
        status = "FAIL"
        # traceback.print_exc()
        message = traceback.format_exc()
        tr = False
        # print(error_message)  
        # return False
    finally:
        print("\033[1;34m\033[47m Execution of Test \033[0;30m\033[47m"+test_name+"\033[1;37m\033[47m completed..!\033[0m")
        print("Test result = "+str(tr) +"\033[m\033[0m")
        testcasereport(test_name,status,message)
        return tr
          
            
            

# def show_dashboard(d):
#     print("showing the dashboard")

def tabib_click(self):
    test_name = "tabib_click"
    tr = False    #test result variable to return value
    d = self.driver
    driver = d
    curractivity = d.current_activity  
    status = "FAIL" 
    # once = 0 # special variable for click functions to stop recursive hell
    # #implement better logic if you got one.
    print("proceeding to click and navigate to entity :"+test_name)
    wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible",7)
    if(curractivity == "com.bfc.bfcpayments.modules.home.view.DashboardActivity" or curractivity == "com.bfc.bfcpayments.modules.tabibHealthCard.ActivityTabibHealthCard"):
        if (curractivity == "com.bfc.bfcpayments.modules.home.view.DashboardActivity"):
            print("it is now in dashboard view ,proceeding to get to tabib module")
            pass
        elif(curractivity == "com.bfc.bfcpayments.modules.tabibHealthCard.ActivityTabibHealthCard"):
            print(" it is currently in tabib health card activity , assuming it is not in any inner page.")
            pass 
    else:
        print("not in dashboard view or tabib view ,proceeding to click on dashboard")
        back_to_dashboard(d)
    sleep(3)
    try:
        curractivity = d.current_activity
        if(curractivity == "com.bfc.bfcpayments.modules.home.view.DashboardActivity"):
            txtwelcome_id = "com.bfccirrus.bfcpayments.mobile:id/txtWelcome"
            wallet_id = "com.bfccirrus.bfcpayments.mobile:id/cardWallet"
            textwelcomevisibility = True
            textwelcomevisibility = wait_until(d,txtwelcome_id,"visible","",1)
            wait_until(d,wallet_id,"visible")
            ...
            # 1. Make a Swipe gesture from ('451','1253') to ('434','356')("to reach card view")
            driver.swipe(start_x=451, start_y=1253, end_x=434, end_y=356, duration=300)

            # 2. Click 'com.bfccirrus.bfcpayments.mobile:id/i...4'
            com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_4 = driver.find_element(By.XPATH,
                                                                                    "//androidx.cardview.widget.CardView[4]//android.widget.ImageView")
            com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_4.click()

            # 3. Click 'TABIIB Card Home'
            waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/toolbar_title")
            tabiib_card_home = driver.find_element(By.ID,
                                                "com.bfccirrus.bfcpayments.mobile:id/toolbar_title")
            # tabiib_card_home.click()
            assert tabiib_card_home.is_displayed()

            # 4. Click 'Offers'
            offers = driver.find_element(By.ID,
                                        "com.bfccirrus.bfcpayments.mobile:id/txtOffers")
            assert offers.is_displayed()

            # 5. Is 'com.bfccirrus.bfcpayments.mobile:id/c...10' visible?
            com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_10 = driver.find_element(By.ID,
                                                                                    "com.bfccirrus.bfcpayments.mobile:id/cardTabibPlusImage")
            assert com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_10.is_displayed()

            # 6. Make a Swipe gesture from ('534','1551') to ('551','346')
            driver.swipe(start_x=534, start_y=1551, end_x=551, end_y=346, duration=300)

            # 7. Is 'com.bfccirrus.bfcpayments.mobile:id/c...11' visible?
            com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_11 = driver.find_element(By.ID,
                                                                                    "com.bfccirrus.bfcpayments.mobile:id/cardFamilyMembers")
            assert com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_11.is_displayed()
  
            tr = True
            printblue("sleeping for 2 second")
            message = "Test : " +str(test_name)+ " is Successfull"
            sleep(2)
        elif(curractivity == "com.bfc.bfcpayments.modules.tabibHealthCard.ActivityTabibHealthCard"):
            print("check for intended activity fragment , assuming it is in currect fragment")
            print("if this fails frquently try to check for fragments")
        else:
            print("current activity : ",curractivity)
            print(" some exception occured , check for current activity must be failed.")
            raise failed(test_name,"this should not be reached , condition to reach desired activity failed.")
        status = "PASS"
    except Exception as e: # work on python 3.x
        save_screenshot(d, test_name)
        
        message = traceback.format_exc()
        status = "FAIL"        
        print('ERROR MESSAGE: '+ str(e))
    
    except:
            # self.fail("Encountered an unexpected exception.test failed in "+test_name)
            save_screenshot(d, test_name)
            status = "FAIL"
            # traceback.print_exc()
            message = traceback.format_exc()
            tr = False
            # print(error_message)  
            # return False
    
    finally:
        print("\033[1;34m\033[47m Execution of Test \033[0;30m\033[47m"+test_name+"\033[1;37m\033[47m completed..!\033[0m")
        print("Test result = "+str(tr) +"\033[m\033[0m")
        testcasereport(test_name,status,message)
        return tr  
    
    
    
    ### this function moved to util in new v2
# def go_and_check_dashboardbalance(d):
#     '''
#     redirects to dashboard and find the wallet balance in them.
#     '''
#     try:
#     #id com.bfccirrus.bfcpayments.mobile:id/txtAmtAvailBal
#         print("fetching dashboard amt")
#         if d.current_activity != dashboardactivity:
#             back_to_dashboard(d)
#             wait_until_activity(d,dashboardactivity,"visible")
#         else:
#             print("dashboard is already in view , may need a scroll up to on top")
#             #ensuring top of dashboard
#             # d.swipe(34, 406, 40, 700, duration=600)
#         welcomeinhometxtid = "com.bfccirrus.bfcpayments.mobile:id/txtWelcome"
#         wait_until(d,welcomeinhometxtid,"visible")
#         walletbal = d.find_element(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtAmtAvailBal").text
#         print("current balance is :",walletbal)
#         return float(walletbal)
#     except Exception as e:
#         print(e)# e
        
        
        
def p2p_click2(self,minimal =False):
    test_name = "p2p_click"
    status = "incomplete"
    message = test_name+" : default message :"
    
    try:
       
        tr = False    #test result variable to return value
        d = self.driver
        driver = d
        occurred = 0
        heal = True #argument variable , now hard coded
        print("command line variable heal is hardcoded here")
        curractivity = d.current_activity
        print("currentactivity ::::::::",curractivity)
        if not minimal:
            try:
                if(curractivity != "com.bfc.bfcpayments.modules.home.view.DashboardActivity" and curractivity !="com.bfc.bfcpayments.modules.pay.view.PayMainActivity"):
                    print("activity is not in dashboard or pay main activity,proceeding to get to dashboard")
                    p("this should not happen frequently , investigate if this happens frequently")
                    dashboardstatus = back_to_dashboard(d)
                    if dashboardstatus == "signup" and heal:
                        # click action is in signup
                        print("somehow ended up in login , trying to recover using heal")
                        signin_with_cpr(d)
                        wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible")
                    elif(not dashboardstatus):
                        save_screenshot(d, test_name)
                        print("show dashboard in p2p click failed")
                        message = traceback.format_exc()
                        status = "FAIL"       
                        tr = False        
                        return tr
                    if occurred == 0:
                        p2p_click2(self)
                        check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                    else:
                        print(RED+"this went to a loop ,Escaping"+CRESET+"\n\t Checking for assert")
                        check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                        
                elif(curractivity == "com.bfc.bfcpayments.modules.home.view.DashboardActivity"):
                    ########################################3
                    # write logic 
                    #######################################
                    print("dashboard found")
                    txtwelcome_id = "com.bfccirrus.bfcpayments.mobile:id/txtWelcome"
                    wallet_id = "com.bfccirrus.bfcpayments.mobile:id/cardWallet"
                    textwelcomevisibility = wait_until(d,txtwelcome_id,"visible","",1)

                    wait_until(d,wallet_id,"visible")
                    # 2. Make a Swipe gesture from ('708','1628') to ('728','802')
                    d.swipe(start_x=708, start_y=1628, end_x=728, end_y=802, duration=300)
                    paywalletcard = d.find_element_by_xpath("//android.widget.TextView[@text = 'Pay Wallet']")
                    if(len(d.find_elements_by_xpath("//android.widget.TextView[@text = 'Pay Wallet']"))== 1):  #note elements
                        paywalletcard.click()
                        wait_until(d,"com.bfccirrus.bfcpayments.mobile:id/txtAppbarTitle","visible")            
                        # print("show dashboard screen needs to be implemented yet")
                    # save_screenshot(d, test_name)
                    check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                    if (check):
                        message =  "\nthe screen is in pay wallet screen"
                        status = "PASS"       
                        tr = True
                    else:
                        message = RED+"PAY WALLET SCREEN FAILED"+CRESET +traceback.format_exc()
                        status = "FAIL"       
                        tr = False  
                    
                    # message = "Test "+test_name+" Successful"
                    # status = "PASS"       
                    # tr = True
                elif(curractivity =="com.bfc.bfcpayments.modules.pay.view.PayMainActivity"):
                    print("the screen is shown as peer to peer . checking if valid entry points")
                    check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                    wait_until(d,"com.bfccirrus.bfcpayments.mobile:id/txtSendTo","visible")
                    txtSendTo = d.find_element(By.ID,
                                                        "com.bfccirrus.bfcpayments.mobile:id/txtSendTo")
                    check = checkassert(d,txtSendTo.text ,"==","Send to")
                    if (check):
                        message =  "\nthe screen is in pay wallet screen entry point"
                        status = "PASS"       
                        tr = True
                    else:
                        dashboardstatus = back_to_dashboard(d)
                        sleep(1)
                        if dashboardstatus == "signup" and heal:
                            # click action is in signup
                            print("somehow ended up in login , trying to recover using heal")
                            signin_with_cpr(d)
                            wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible")
                            occurred = 0

                            p2p_click2(self)

                        elif occurred == 0:
                            p2p_click2(self)
                            check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                        elif(not dashboardstatus):
                            save_screenshot(d, test_name)
                            print("show dashboard in p2p click failed")
                            message = traceback.format_exc()
                            status = "FAIL"       
                            tr = False        
                            return tr
                        else:
                            print(RED+"this went to a loop ,Escaping"+CRESET+"\n\t Checking for assert")
                            check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                        if (check):
                            message =  "\nthe screen is in pay wallet screen"
                            status = "PASS"       
                            tr = True
                        else:
                            message = RED+"PAY WALLET SCREEN FAILED"+CRESET +traceback.format_exc()
                            status = "FAIL"       
                            tr = False  
                    
                else:
                    print(RED+"\n\n\\t\tthis should not happen i guess\nSTILL CHECKING FOR ACTIVITY\n  "+CRESET)
                    check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                    if (check):
                        message =  "\nthe screen is in pay wallet screen"
                        status = "PASS"       
                        tr = True
                    else:
                        message = RED+"PAY WALLET SCREEN FAILED"+CRESET +traceback.format_exc()
                        status = "FAIL"       
                        tr = False  
                
                if checkassert(d,check,"==",True,"checking activity p2p"):
                    message =  "\nthe screen is in pay wallet screen"
                    status = "PASS"       
                    tr = True
                else:
                    
                    save_screenshot(d, test_name)
                    message = RED+"PAY WALLET SCREEN FAILED"+CRESET +traceback.format_exc()
                    status = "FAIL"       
                    tr = False        
                    return tr
            except Exception as e: # work on python 3.x
                save_screenshot(d, test_name)
                message = traceback.format_exc()
                status = "FAIL"       
                tr = False
                print('ERROR MESSAGE: '+ str(e))
                
            finally:
                print("\033[1;34m\033[47m Execution of Test \033[0;30m\033[47m"+test_name+"\033[1;37m\033[47m completed..!\033[0m")
                print("Test result = "+str(tr) +"\033[m\033[0m")
                testcasereport(test_name,status,message)
                return tr
        elif minimal:
            try:
                if(curractivity != "com.bfc.bfcpayments.modules.home.view.DashboardActivity" and curractivity !="com.bfc.bfcpayments.modules.pay.view.PayMainActivity"):
                    # print("activity is not in dashboard or pay main activity,proceeding to get to dashboard")
                    # p("this should not happen frequently , investigate if this happens frequently")
                    dashboardstatus = back_to_dashboard(d)
                    if dashboardstatus == "signup" and heal:
                        # click action is in signup
                        # print("somehow ended up in login , trying to recover using heal")
                        signin_with_cpr(d)
                        wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible")
                    elif(not dashboardstatus):
                        save_screenshot(d, test_name)
                        print("p2p click failed")
                        message = traceback.format_exc()
                        status = "FAIL"       
                        tr = False        
                        return tr
                    if occurred == 0:
                        p2p_click2(self)
                        check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                    else:
                        print(RED+"this went to a loop ,Escaping"+CRESET+"\n\t Checking for assert")
                        check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                        
                elif(curractivity == "com.bfc.bfcpayments.modules.home.view.DashboardActivity"):
                    ########################################3
                    # write logic 
                    #######################################
                    print("dashboard found")
                    txtwelcome_id = "com.bfccirrus.bfcpayments.mobile:id/txtWelcome"
                    wallet_id = "com.bfccirrus.bfcpayments.mobile:id/cardWallet"
                    textwelcomevisibility = wait_until(d,txtwelcome_id,"visible","",1)

                    # wait_until(d,wallet_id,"visible")
                    # 2. Make a Swipe gesture from ('708','1628') to ('728','802')
                    d.swipe(start_x=708, start_y=1628, end_x=728, end_y=802, duration=300)
                    paywalletcard = d.find_element_by_xpath("//android.widget.TextView[@text = 'Pay Wallet']")
                    if(len(d.find_elements_by_xpath("//android.widget.TextView[@text = 'Pay Wallet']"))== 1):  #note elements
                        paywalletcard.click()
                        wait_until(d,"com.bfccirrus.bfcpayments.mobile:id/txtAppbarTitle","visible")            
                        # print("show dashboard screen needs to be implemented yet")
                    # save_screenshot(d, test_name)
                    check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                    if (check):
                        message =  "\nthe screen is in pay wallet screen"
                        status = "PASS"       
                        tr = True
                    else:
                        message = RED+"PAY WALLET SCREEN FAILED"+CRESET +traceback.format_exc()
                        status = "FAIL"       
                        tr = False  
                    
                    # message = "Test "+test_name+" Successful"
                    # status = "PASS"       
                    # tr = True
                elif(curractivity =="com.bfc.bfcpayments.modules.pay.view.PayMainActivity"):
                    print("the screen is shown as peer to peer . checking if valid entry points")
                    check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                    wait_until(d,"com.bfccirrus.bfcpayments.mobile:id/txtSendTo","visible")
                    txtSendTo = d.find_element(By.ID,
                                                        "com.bfccirrus.bfcpayments.mobile:id/txtSendTo")
                    check = checkassert(d,txtSendTo.text ,"==","Send to")
                    if (check):
                        message =  "\nthe screen is in pay wallet screen entry point"
                        status = "PASS"       
                        tr = True
                    else:
                        dashboardstatus = back_to_dashboard(d)
                        sleep(1)
                        if dashboardstatus == "signup" and heal:
                            # click action is in signup
                            print("somehow ended up in login , trying to recover using heal")
                            signin_with_cpr(d)
                            wait_until_activity(d,"com.bfc.bfcpayments.modules.home.view.DashboardActivity","visible")
                            occurred = 0

                            p2p_click2(self)

                        elif occurred == 0:
                            p2p_click2(self)
                            check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                        elif(not dashboardstatus):
                            save_screenshot(d, test_name)
                            print("show dashboard in p2p click failed")
                            message = traceback.format_exc()
                            status = "FAIL"       
                            tr = False        
                            return tr
                        else:
                            print(RED+"this went to a loop ,Escaping"+CRESET+"\n\t Checking for assert")
                            check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                        if (check):
                            message =  "\nthe screen is in pay wallet screen"
                            status = "PASS"       
                            tr = True
                        else:
                            message = RED+"PAY WALLET SCREEN FAILED"+CRESET +traceback.format_exc()
                            status = "FAIL"       
                            tr = False  
                    
                else:
                    print(RED+"\n\n\\t\tthis should not happen i guess\nSTILL CHECKING FOR ACTIVITY\n  "+CRESET)
                    check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
                    if (check):
                        message =  "\nthe screen is in pay wallet screen"
                        status = "PASS"       
                        tr = True
                    else:
                        message = RED+"PAY WALLET SCREEN FAILED"+CRESET +traceback.format_exc()
                        status = "FAIL"       
                        tr = False  
                
                if checkassert(d,check,"==",True,"checking activity p2p"):
                    message =  "\nthe screen is in pay wallet screen"
                    status = "PASS"       
                    tr = True
                else:
                    
                    save_screenshot(d, test_name)
                    message = RED+"PAY WALLET SCREEN FAILED"+CRESET +traceback.format_exc()
                    status = "FAIL"       
                    tr = False        
                    return tr
            except Exception as e: # work on python 3.x
                save_screenshot(d, test_name)
                message = traceback.format_exc()
                status = "FAIL"       
                tr = False
                print('ERROR MESSAGE: '+ str(e))
                # need a feeder report
            # finally:
            #     print("\033[1;34m\033[47m Execution of Test \033[0;30m\033[47m"+test_name+"\033[1;37m\033[47m completed..!\033[0m")
            #     print("Test result = "+str(tr) +"\033[m\033[0m")
            #     testcasereport(test_name,status,message)
            #     return tr
        else:
            print("there is absolutely no way this could reach")
    except Exception as e: # work on python 3.x
        save_screenshot(d, test_name)
        message = traceback.format_exc()
        status = "FAIL"       
        tr = False
        print('ERROR MESSAGE: '+ str(e))
            
    finally:
        print("\033[1;34m\033[47m Execution of Test \033[0;30m\033[47m"+test_name+"\033[1;37m\033[47m completed..!\033[0m")
        print("Test result = "+str(tr) +"\033[m\033[0m")
        testcasereport(test_name,status,message)
        return tr
    
    
    
    
def click_paybills(self,minimal =False):
    test_name = "paybills_click"
    status = "incomplete"
    message = test_name+" : default message :"
    
    try:
        print("clicking pay bills")
        
        
        tr = False    #test result variable to return value
        d = self.driver
        driver = d
        occurred = 0
        if d.current_activity != dashboardactivity :#and force:
            # if current activity = pay bill check for entry point
            back_to_dashboard(d)
        check_and_waitforprogressbar(d)
        d.swipe(start_x=708, start_y=1628, end_x=728, end_y=802, duration=300)
        if(len(d.find_elements_by_xpath("//android.widget.TextView[@text = 'Pay Bills']"))== 1):  #note elements
            paybillscard = d.find_element_by_xpath("//android.widget.TextView[@text = 'Pay Bills']")
            paybillscard.click()
            wait_until(d,"com.bfccirrus.bfcpayments.mobile:id/txtAppbarTitle","visible") 
            titletxt = d.find_element_by_id("com.bfccirrus.bfcpayments.mobile:id/txtAppbarTitle").text
            titlecheck = checkassert(d,titletxt,'==','Pay Bills')
            if titlecheck:
                wait_until(d,"//android.widget.TextView[@text = 'Most Used']",'visible')
                checkassert(d, d.find_element_by_xpath("//android.widget.TextView[@text = 'Most Used']"))
                
                status = 'PASS'
                message = 'pay bills click successful'
                tr = True
            elif titletxt == 'Enable Send Money':
                status = 'FAIL'
                message = 'person is not enabled avenues services'
                tr = False
                return
            else:
                status = 'FAIL'
                message = 'pay bills click Unsuccessful , "Pay Bills" card not found'
                tr = False
                return
            
        else:
            status = 'FAIL'
            message = 'pay bills click Unsuccessful , "Pay Bills" card not found'
            tr = False
        
    except Exception as e: # work on python 3.x
        save_screenshot(d, test_name)
        # message = traceback.format_exc()
        message = str(e)
        status = "FAIL"       
        tr = False
        print('ERROR MESSAGE: '+ str(e))
        
    finally:
        print("\033[1;34m\033[47m Execution of Test \033[0;30m\033[47m"+test_name+"\033[1;37m\033[47m completed..!\033[0m")
        print("Test result = "+str(tr) +"\033[m\033[0m")
        testcasereport(test_name,status,message)
        return tr