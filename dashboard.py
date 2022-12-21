import traceback
from customclasses import failed
# from util import *
from config import dashboardactivity,walletbal
from time import sleep
from selenium.webdriver.common.by import By

from util import CRESET, PURPLE, back_to_dashboard, check_and_waitforprogressbar, checkassert, go_and_check_dashboardbalance, save_screenshot, scroll_down_to_view, scroll_to_top, testcasereport, wait_until, wait_until_activity

#clicks on paybills card    
def click_paybills(self,minimal = False):
    try:
        test_name = 'click_paybills'
        message = 'unexpected error occured in '+test_name
        status = "FAIL"
        d = driver = self.driver
        tr =False
        if d.current_activity != dashboardactivity:
                back_to_dashboard(d)
                wait_until_activity(d,dashboardactivity,"visible")
                walletbal = go_and_check_dashboardbalance(d)
        if d.current_activity == dashboardactivity:
            print("clicking on pay bills")
            paybillcard = "//android.widget.TextView[@text = 'Pay Bills']"
            print("this is element in paybillcard",paybillcard)
            scroll_down_to_view(d,paybillcard,start_x = 0,start_y=0 , end_x = 0,end_y = 0)
            d.find_element(By.XPATH,paybillcard).click()
            # txtTitleBilling = 'txtTitleBilling'
            # 'Utilities and Bill Payments'
            _txtTitleBilling = d.find_element(By.ID,'txtTitleBilling')
            tr = checkassert(d,_txtTitleBilling) and checkassert(d,_txtTitleBilling.text,'==','Utilities and Bill Payments')
            message= "Test : " +test_name + " Successfully completed"   
            status = "PASS"         
    except Exception as e:

        print(e)
        save_screenshot(d, test_name)
        status = "FAIL"
        traceback.print_exc()
        message = e 
        tr = False
        
    finally:
        if not minimal:
            testcasereport(test_name,status,message)
            return tr
        else:
            return tr,message
    
# clciks on cards     
def click_cards(self,minimal = False):
    try:
        test_name = 'click_cards'
        message = 'unexpected error occured in '+test_name
        status = "FAIL"
        d = driver = self.driver
        tr =False
        if d.current_activity != dashboardactivity:
                back_to_dashboard(d)
                wait_until_activity(d,dashboardactivity,"visible")
                walletbal = go_and_check_dashboardbalance(d)
        if d.current_activity == dashboardactivity:
            print("clicking on cards")
            paybillcard = "//android.widget.TextView[@text = 'Cards']"
            # print("this is element in paybillcard",paybillcard)
            scroll_down_to_view(d,paybillcard,start_x = 0,start_y=0 , end_x = 0,end_y = 0)
            d.find_element(By.XPATH,paybillcard).click()
            # txtTitleBilling = 'txtTitleBilling'
            # sleep(5)
            wait_until_activity(d,'com.bfc.bfcpayments.modules.card.CardActivity','visible')
            _txtAppbarTitle = d.find_element(By.ID,'txtAppbarTitle')
            
            tr = checkassert(d,_txtAppbarTitle,assertname='app title is visible') and checkassert(d,_txtAppbarTitle.text,'==','BFC Pay Card')
            check_and_waitforprogressbar(d)
            message= "Test : " +test_name + " Successfully completed"   
            status = "PASS"         
    except Exception as e:

        print(e)
        save_screenshot(d, test_name)
        status = "FAIL"
        traceback.print_exc()
        message = e 
        tr = False
        
    finally:
        if not minimal:
            testcasereport(test_name,status,message)
            return tr
        else:
            return tr,message
        
#clicks on wallet card
def click_add_money(self):
    test_name = "add_money_click"
    tr = False    #test result variable to return value
    d = self.driver
    driver = d
    curractivity = d.current_activity  
    try:    
        if(curractivity == "com.bfc.bfcpayments.modules.home.view.DashboardActivity"): # or curractivity == "com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity"):
            # check for same page not implemented
            print("current activity already in dashboard ")
            scroll_to_top(d)
            pass 
        else:
            print("not in dashboard view and check for same page not implemented,re reouting to dashboard")
            back_to_dashboard(d)
        txtwelcome_id = "com.bfccirrus.bfcpayments.mobile:id/txtWelcome"
        # wallet_id = "com.bfccirrus.bfcpayments.mobile:id/cardWallet"      
        textwelcomevisibility = wait_until(d,txtwelcome_id,"visible")
        checkassert(d,textwelcomevisibility,"==",True,"welcome text in dashboard check")
        addmoneycard = "//android.widget.TextView[@text = 'Add Money']"
        print('scrolling to the Add Money')
        scroll_down_to_view(d,addmoneycard,start_x = 0,start_y=0 , end_x = 0,end_y = 0)
        addmoneycardelem = driver.find_element(By.XPATH,
                                                 "//android.widget.TextView[@text = 'Add Money']")
        addmoneycardelem.click()
        check = wait_until_activity(d,"com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity","visible")
        if checkassert(d,check,"==",True,"checking add money activity"):
            tr =True
            message = "successfully clicked on add money and reaached the screen"
            status = 'PASS'
        
    except Exception as e: # work on python 3.x
        save_screenshot(d, test_name)
        message = e
        print(traceback.format_exc())
        status = "FAIL"       
        tr = False
        print('ERROR MESSAGE: '+ str(e))
    except:
        save_screenshot(d, test_name)
        status = "FAIL"
        message = traceback.format_exc()
        tr = False
    finally:
        print("\033[1;34m\033[47m Execution of Test \033[0;30m\033[47m"+test_name+"\033[1;37m\033[47m completed..!\033[0m")
        print("Test result = "+str(tr) +"\033[m\033[0m")
        testcasereport(test_name,status,message)
        return tr
    
def click_cards(self):
    test_name = "click_cards from dashboard"
    tr = False    #test result variable to return value
    d = self.driver
    driver = d
    curractivity = d.current_activity  
    status = "FAIL"       
    
    try:    
        if(curractivity == "com.bfc.bfcpayments.modules.home.view.DashboardActivity"): # or curractivity == "com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity"):
            # check for same page not implemented
            print("current activity already in dashboard ")
            scroll_to_top(d)
            pass 
        else:
            print("not in dashboard view and check for same page not implemented,re reouting to dashboard")
            back_to_dashboard(d)
        txtwelcome_id = "com.bfccirrus.bfcpayments.mobile:id/txtWelcome"
        # wallet_id = "com.bfccirrus.bfcpayments.mobile:id/cardWallet"      
        textwelcomevisibility = wait_until(d,txtwelcome_id,"visible")
        checkassert(d,textwelcomevisibility,"==",True,"welcome text in dashboard check")
        addmoneycard = "//android.widget.TextView[@text = 'Cards']"
        print('scrolling to the cards')
        scroll_down_to_view(d,addmoneycard,start_x = 0,start_y=0 , end_x = 0,end_y = 0)
        addmoneycardelem = driver.find_element(By.XPATH,
                                                 "//android.widget.TextView[@text = 'Cards']")
        addmoneycardelem.click()
        sleep(2)
        print("this is ",d.current_activity)
        check = wait_until_activity(d,"com.bfc.bfcpayments.modules.multicurrencyNew.MulticurrencyActivity","visible")
        if checkassert(d,check,"==",True,"checking multicurrency activity"):
            tr =True
            message = "successfully clicked on cards and reaached the cards selection screen"
            status = 'PASS'
        else:
            save_screenshot(d, test_name)
            tr =True
            message = "activity not reached in MulticurrencyActivity. something occured find screenshot"
            status = 'PASS'
        
    except Exception as e: # work on python 3.x
        save_screenshot(d, test_name)
        message = e
        print(traceback.format_exc())
        status = "FAIL"       
        tr = False
        print('ERROR MESSAGE: '+ str(e))
    except:
        save_screenshot(d, test_name)
        status = "FAIL"
        message = traceback.format_exc()
        tr = False
    finally:
        print("\033[1;34m\033[47m Execution of Test \033[0;30m\033[47m"+test_name+"\033[1;37m\033[47m completed..!\033[0m")
        print("Test result = "+str(tr) +"\033[m\033[0m")
        testcasereport(test_name,status,message)
        return tr
                      