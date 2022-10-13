import traceback
from customclasses import failed
# from util import *
from config import dashboardactivity,walletbal
from time import sleep
from selenium.webdriver.common.by import By

from util import back_to_dashboard, checkassert, go_and_check_dashboardbalance, save_screenshot, scroll_down_to_view, testcasereport, wait_until_activity
    
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
            tr = checkassert(d,_txtTitleBilling) and checkassert(d,_txtTitleBilling,'==','Utilities and Bill Payments')
            
            
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
    
            
        
        
        