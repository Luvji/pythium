from customclasses import failed, splashloadtooklong
from dashboard import go_and_check_dashboardbalance
from util import *
from time import sleep
import traceback
from selenium.webdriver.common.by import By


# try:
#     test_first_time_login.test_main(driver)
# except Exception:
#     # Failure Behaviour: Continue
#     pass
def add_money_to_wallet(self):
    d = self.driver
    driver = d
    """add money to wallet flow."""
    test_name = 'test_test_name'
    status = "FAIL"
    try:
        driver.swipe(start_x=764, start_y=1182, end_x=781, end_y=450, duration=300)

        # 6. Click 'com.bfccirrus.bfcpayments.mobile:id/c...7'
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_7 = driver.find_element(By.XPATH,
                                                                                "//androidx.cardview.widget.CardView[6]")
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_c_7.click()
        # 7. Click 'BHD 20'
        bhd_20 = driver.find_element(By.XPATH,
                                    "//android.widget.RadioButton[@text = 'BHD 20']")
        bhd_20.click()

        # 8. Make a Swipe gesture from ('831','738') to ('801','290')
        driver.swipe(start_x=831, start_y=738, end_x=801, end_y=290, duration=300)

        # 9. Click 'BHD 20.000'
        bhd_20_000 = driver.find_element(By.ID,
                                        "com.bfccirrus.bfcpayments.mobile:id/txtTotalAmt")
        bhd_20_000.click()

        # 10. Click 'Proceed'
        proceed = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnVerifyCPR")
        proceed.click()

        # 11. Click 'Payment Method'
        payment_method = driver.find_element(By.XPATH,
                                            "//android.widget.TextView[@text = 'Payment Method']")
        payment_method.click()

        # 12. Click 'Benefit - Debit/ATM Card'
        benefit_debit_slash_atm_card = driver.find_element(By.ID,
                                                        "com.bfccirrus.bfcpayments.mobile:id/txtPaymentMethodName")
        benefit_debit_slash_atm_card.click()
        
        sleep(5)
    except:
        #
        ##except related cases.
        #<copy paste this except and finally block , add any if anything occurs>
        # self.fail("Encountered an unexpected exception.test failed in "+test_name)
        save_screenshot(d, test_name)
        status = "FAIL"
        # traceback.print_exc()
        message = traceback.format_exc()
        # print(error_message)
        return False
    finally:
        testcasereport(test_name,status,message)


# def add_money_to_wallet_from_card_by_BHD_20_button(self,cardholdername = "redlohdrac eman"):
#     '''
#     adds money to wallet by specif flow:
#     from debit card.
#     utilises 20 bhd dedicated button.
#     '''
#     try:
#         d= driver =  self.driver
#         cardnumber = "4600411234567899"
#         test_name = 'addmoney20bhd'
#         status = "FAIL"
#         print("current activity",d.current_activity)
#         assert "com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity" == d.current_activity,"it is not in view of add money wallet"
    
#         #TO_DO:: randomise / config file for user input on data
        
        
#         print("adding money to wallet ")
        
#         # check if title is reached by checking if it contains  "Add Money" as text
#         title = driver.find_element(By.ID,
#                                 "com.bfccirrus.bfcpayments.mobile:id/txtAppbarTitle").text
#         assert title and ("Add Money" in title)

#         # 1. Check 'Available Balance text'
#         available_balance_id = driver.find_element(By.ID,
#                                                 "com.bfccirrus.bfcpayments.mobile:id/txtWalletBal")
        
#         assert available_balance_id

#         # 3. C'
#         # print("type:::",type(available_balance_id.text),"available_balance_id.text",available_balance_id.text)
#         available_balance = float(available_balance_id.text)
#         #TO_DO::  hardcoding 20 here. make it dynamic
#         expected_balance = available_balance +20

#         # 4. Click 'BHD 20' button
#         bhd_20 = driver.find_element(By.XPATH,
#                                     "//android.widget.RadioButton[@text = 'BHD 20']")
#         bhd_20.click()

#         # 5. Does '20.000' contain '20.000'?
#         _20_000 = driver.find_element(By.ID,
#                                     "com.bfccirrus.bfcpayments.mobile:id/etAmount")
#         step_output = _20_000.text
#         assert step_output and ("20.000" in step_output)

#         # 6. Does 'BHD 20.000' contain 'BHD 20.000'?
#         bhd_20_000 = driver.find_element(By.ID,
#                                         "com.bfccirrus.bfcpayments.mobile:id/txtTotalAmt")
#         step_output = bhd_20_000.text
#         assert step_output and ("BHD 20.000" in step_output)

#         # 7. Make a Swipe gesture from ('605','1482') to ('585','255')
#         driver.swipe(start_x=605, start_y=1482, end_x=585, end_y=255, duration=300)

#         # 8. Is 'Proceed1' is clickable?
#         proceed1 = driver.find_element(By.ID,
#                                     "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
#         assert proceed1.is_enabled()

#         # 9. Click 'Proceed1'
#         proceed1 = driver.find_element(By.ID,
#                                     "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
#         proceed1.click()
#         waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/imgArrow",)

#         # 10. Click 'Benefit - Debit/ATM Card' link
#         com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_3 = driver.find_element(By.ID,
#                                                                                 "com.bfccirrus.bfcpayments.mobile:id/imgArrow")
#         com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_3.click()
#         # wait_until(d,"//android.view.View[@text = 'Card Number']",)
#         waitfor(d,"//android.view.View[@text = 'Card Number']","xpath")

#         # 11. Click 'debitCardNumber'
#         debitcardnumber = driver.find_element(By.XPATH,
#                                             "//android.view.View[6]/android.widget.EditText")
#         debitcardnumber.click()

#         # 12. Type '4600411234567890' in 'debitCardNumber'
#         # debitcardnumber = driver.find_element(By.XPATH,
#         #                                       "//android.view.View[6]/android.widget.EditText")
#         debitcardnumber.send_keys(cardnumber)
#         check_and_hide_keyboard(d)

#         # 13. Click 'MM'
#         mm = driver.find_element(By.XPATH,
#                                 "//android.widget.Spinner[@text = 'MM']")
#         mm.click()
#         sleep(2) #making sure the list is visible
#         #TO_DO ::: write better code to select on date at random
#         # 14. Make a Swipe gesture from ('510','1605') to ('508','177')
#         driver.swipe(start_x=510, start_y=1605, end_x=508, end_y=177, duration=300)

#         # 15. Click '121'
#         _12m = driver.find_element(By.XPATH,
#                                 "//android.widget.CheckedTextView[@text = '12']")
#         _12m.click()

#         # 16. Click 'YYYY1'
#         yyyy = driver.find_element(By.XPATH,
#                                     "//android.widget.Spinner[@text = 'YYYY']")
#         yyyy.click()
#         waitfor(d,"//android.widget.ListView","xpath",sec = 5)
#         # 17. Click '2026'
#         _2026y = driver.find_element(By.XPATH,
#                                     "//android.widget.CheckedTextView[@text = '2026']")
#         _2026y.click()
#         # if len(d.find_elements(By.XPATH,"//android.widget.ListView"))>0:
#         #     android_widget_listview = driver.find_element(By.XPATH,
#         #                                           "//android.widget.ListView")
#         #     assert not android_widget_listview.is_displayed()

#         # 18. Click 'debitCardholderName'
#         waitfor(d,"//android.view.View[8]//android.widget.EditText","xpath",sec = 5)
#         debitcardholdername = driver.find_element(By.XPATH,
#                                                 "//android.view.View[8]//android.widget.EditText")
#         debitcardholdername.click()

#         # 19. Type 'card name' in 'debitCardholderName'
#         # debitcardholdername = driver.find_element(By.XPATH,
#         #                                           "//android.view.View[8]//android.widget.EditText")
#         debitcardholdername.send_keys(cardholdername)
#         check_and_hide_keyboard(d)
        
#         # 20. Click 'cardPin1'
#         print("now starting to enter pin code '1111' from the UI")
#         # cardpin1 = driver.find_element(By.XPATH,
#         #                             "//android.view.View[9]//android.widget.EditText")
#         cardpinxpath2 = driver.find_element(By.XPATH,"//android.view.View[9]/android.view.View[2]")

#         cardpinxpath2.click()
        
#         waitfor(d,"//android.widget.Button[@text = 'Clear']","xpath")
#         # 21. Click '1'
#         _1 = driver.find_element(By.XPATH,
#                                 "//android.widget.Button[@text = '1']")
#         _1.click()

#         # 22. Click '1'
#         _1 = driver.find_element(By.XPATH,
#                                 "//android.widget.Button[@text = '1']")
#         _1.click()

#         # 23. Click '1'
#         _1 = driver.find_element(By.XPATH,
#                                 "//android.widget.Button[@text = '1']")
#         _1.click()

#         # 24. Click '1'
#         _1 = driver.find_element(By.XPATH,
#                                 "//android.widget.Button[@text = '1']")
#         _1.click()

#         # 25. Click 'Enter'
#         enter = driver.find_element(By.XPATH,
#                                     "//android.widget.Button[@text = 'Enter']")
#         enter.click()
#         check_and_hide_keyboard(d)

#         # 26. Make a Swipe gesture from ('832','1484') to ('840','274')
#         driver.swipe(start_x=832, start_y=1484, end_x=840, end_y=274, duration=300)

#         # 27. Click 'Pay2'
#         pay2 = driver.find_element(By.XPATH,
#                                 "//android.widget.Button[@text = 'Pay']")
#         pay2.click()

#         # 28. Click 'Success!'
#         success_ = driver.find_element(By.ID,
#                                     "com.bfccirrus.bfcpayments.mobile:id/txtSuccessfullyTransferred")
#         success_.click()

#         # 29. Click 'Your transaction has been completed s...'
#         txnresp = driver.find_element(By.ID,
#                                                                     "com.bfccirrus.bfcpayments.mobile:id/txtMessage")
#         txnresp.click()

#         # 30. Make a Swipe gesture from ('754','1274') to ('745','380')
#         driver.swipe(start_x=754, start_y=1274, end_x=745, end_y=380, duration=300)

#         # 31. Click 'com.bfccirrus.bfcpayments.mobile:id/i...'
#         com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_ = driver.find_element(By.ID,
#                                                                                 "com.bfccirrus.bfcpayments.mobile:id/imgMoneyTransfer")
#         com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_.click()

#         # 32. Is 'Proceed1' is clickable?
#         proceed1 = driver.find_element(By.ID,
#                                     "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
#         assert proceed1.is_enabled()

#         # 33. Click 'Proceed1'
#         proceed1 = driver.find_element(By.ID,
#                                     "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
#         proceed1.click()
#         sleep(2)
#         #check for true status in here
#         status = "PASS"
#         return True
#     except AssertionError:
#         print("ASSERT ERROR")
#         message = traceback.format_exc()
#         print("ERROR :: ",message)
        
#     except:
#         #
#         ##except related cases.
#         #<copy paste this except and finally block , add any if anything occurs>
#         # self.fail("Encountered an unexpected exception.test failed in "+test_name)
#         save_screenshot(d, test_name)
#         status = "FAIL"
#         # traceback.print_exc()
#         message = traceback.format_exc()
#         # print(error_message)
#         return False
#     finally:
#         testcasereport(test_name,status,message)
        
def add_money_to_wallet_from_card_by_BHD_20_button(self):
    '''
    adds money to wallet by specif flow:
    from debit card.
    utilises 20 bhd dedicated button.
    '''
    try:
        d= driver =  self.driver
        test_name = 'add_money_to_wallet_from_card_by_BHD_20_button'
        status = "FAIL"
        print("current activity",d.current_activity)
        assert "com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity" == d.current_activity,"it is not in view of add money wallet"
        checkassert(d,"com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity","==",d.current_activity)
        #TO_DO:: randomise / config file for user input on data
        # ensureentrypoint(self)
        
        
        print("adding money to wallet ")
        
        # check if title is reached by checking if it contains  "Add Money" as text
        title = driver.find_element(By.ID,
                                "com.bfccirrus.bfcpayments.mobile:id/txtAppbarTitle").text
        assert title and ("Add Money" in title)
        checkassert(d,title,"==","Add Money","check title is Add Money")

        # 1. Check 'Available Balance text'
        available_balance_id = driver.find_element(By.ID,
                                                "com.bfccirrus.bfcpayments.mobile:id/txtWalletBal")
        
        assert available_balance_id

        # 3. C'
        # print("type:::",type(available_balance_id.text),"available_balance_id.text",available_balance_id.text)
        available_balance = float(available_balance_id.text)
        #TO_DO::  hardcoding 20 here. make it dynamic
        expected_balance = available_balance +20

        # 4. Click 'BHD 20' button
        bhd_20 = driver.find_element(By.XPATH,
                                    "//android.widget.RadioButton[@text = 'BHD 20']")
        bhd_20.click()

        # 5. Does '20.000' contain '20.000'?
        _20_000 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/etAmount")
        step_output = _20_000.text
        assert step_output and ("20.000" in step_output)
        
        check_and_waitforprogressbar(d)
        waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/txtTotalAmt")
        # 6. Does 'BHD 20.000' contain 'BHD 20.000'?
        bhd_20_000 = driver.find_element(By.ID,
                                        "com.bfccirrus.bfcpayments.mobile:id/txtTotalAmt")      
        step_output = bhd_20_000.text
        assert step_output and ("BHD 20.000" in step_output)

        # 7. Make a Swipe gesture from ('605','1482') to ('585','255')
        driver.swipe(start_x=605, start_y=1482, end_x=585, end_y=255, duration=300)

        # 8. Is 'Proceed1' is clickable?
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        assert proceed1.is_enabled()

        # 9. Click 'Proceed1'
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        proceed1.click()
        waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/imgArrow",)

        # 10. Click 'Benefit - Debit/ATM Card' link
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_3 = driver.find_element(By.ID,
                                                                                "com.bfccirrus.bfcpayments.mobile:id/imgArrow")
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_3.click()
        # wait_until(d,"//android.view.View[@text = 'Card Number']",)
        waitfor(d,"//android.view.View[@text = 'Card Number']","xpath")
        # 20. Click 'cardPin1'
        print("now starting to enter pin code '1111' from the UI ,because later xpath might change")
        # cardpin1 = driver.find_element(By.XPATH,
        #                             "//android.view.View[9]//android.widget.EditText")
        cardpinxpath2 = driver.find_element(By.XPATH,"//android.view.View[9]/android.view.View[2]/android.widget.EditText[1]")

        # print(cardpinxpath2.class)
        cardpinxpath2.click()
        
        clearfound = waitfor(d,"//android.widget.Button[@text = 'Clear']","xpath")
        # 21. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 22. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 23. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 24. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 25. Click 'Enter'
        enter = driver.find_element(By.XPATH,
                                    "//android.widget.Button[@text = 'Enter']")
        enter.click()
        # 11. Click 'debitCardNumber'
        debitcardnumber = driver.find_element(By.XPATH,
                                            "//android.view.View[6]/android.widget.EditText")
        debitcardnumber.click()

        # 12. Type '4600411234567890' in 'debitCardNumber'
        # debitcardnumber = driver.find_element(By.XPATH,
        #                                       "//android.view.View[6]/android.widget.EditText")
        debitcardnumber.send_keys(cardnumber)
        check_and_hide_keyboard(d)

        # 13. Click 'MM'
        mm = driver.find_element(By.XPATH,
                                "//android.widget.Spinner[@text = 'MM']")
        mm.click()
        sleep(2) #making sure the list is visible
        #TO_DO ::: write better code to select on date at random
        # 14. Make a Swipe gesture from ('510','1605') to ('508','177')
        driver.swipe(start_x=510, start_y=1605, end_x=508, end_y=177, duration=300)

        # 15. Click '121'
        _12m = driver.find_element(By.XPATH,
                                "//android.widget.CheckedTextView[@text = '12']")
        _12m.click()

        # 16. Click 'YYYY1'
        yyyy = driver.find_element(By.XPATH,
                                    "//android.widget.Spinner[@text = 'YYYY']")
        yyyy.click()
        waitfor(d,"//android.widget.ListView","xpath",sec = 5)
        # 17. Click '2026'
        _2026y = driver.find_element(By.XPATH,
                                    "//android.widget.CheckedTextView[@text = '2026']")
        _2026y.click()
        # if len(d.find_elements(By.XPATH,"//android.widget.ListView"))>0:
        #     android_widget_listview = driver.find_element(By.XPATH,
        #                                           "//android.widget.ListView")
        #     assert not android_widget_listview.is_displayed()

        # 18. Click 'debitCardholderName'
        waitfor(d,"//android.view.View[8]//android.widget.EditText","xpath",sec = 5)
        debitcardholdername = driver.find_element(By.XPATH,
                                                "//android.view.View[8]//android.widget.EditText")
        debitcardholdername.click()

        # 19. Type 'card name' in 'debitCardholderName'
        # debitcardholdername = driver.find_element(By.XPATH,
        #                                           "//android.view.View[8]//android.widget.EditText")
        debitcardholdername.send_keys(cardholdername)
        check_and_hide_keyboard(d)
        
        ##############################
        # pin enter function was here 
        ###########################

        # 26. Make a Swipe gesture from ('832','1484') to ('840','274')
        driver.swipe(start_x=832, start_y=1484, end_x=840, end_y=274, duration=300)

        # 27. Click 'Pay2'
        pay2 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = 'Pay']")
        pay2.click()

        # 28. Click 'Success!'
        waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/txtSuccessfullyTransferred")
        success_ = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/txtSuccessfullyTransferred")
        success_.click()

        # 29. Click 'Your transaction has been completed s...'
        txnresp = driver.find_element(By.ID,
                                                                    "com.bfccirrus.bfcpayments.mobile:id/txtMessage")
        txnresp.click()

        # 30. Make a Swipe gesture from ('754','1274') to ('745','380')
        driver.swipe(start_x=754, start_y=1274, end_x=745, end_y=380, duration=300)

        # 31. Click 'com.bfccirrus.bfcpayments.mobile:id/i...'
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_ = driver.find_element(By.ID,
                                                                                "com.bfccirrus.bfcpayments.mobile:id/imgMoneyTransfer")
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_.click()

        # 32. Is 'Proceed1' is clickable?
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        assert proceed1.is_enabled()

        # 33. Click 'Proceed1'
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        proceed1.click()
        sleep(2)
        #check for true status in here
                # check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
        # visibility	visible
        # true android.widget.ProgressBar
        check_and_waitforprogressbar(d)
        if checkassert(d,expected_balance,"==",go_and_check_dashboardbalance(d)):
            status = "PASS"
            message = "successfully added money"
            return True
        else:
            status = "FAIL"
            message = "successfully added money not updated in dashboard"
            return False
    # except AssertionError:
    #     print("ASSERT ERROR")
    #     message = traceback.format_exc()
    #     print("ERROR :: ",message)
        
    except:
        #
        ##except related cases.
        #<copy paste this except and finally block , add any if anything occurs>
        # self.fail("Encountered an unexpected exception.test failed in "+test_name)
        save_screenshot(d, test_name)
        status = "FAIL"
        # traceback.print_exc()
        message = traceback.format_exc()
        # print(error_message)
        return False
    finally:
        testcasereport(test_name,status,message)
        
        
def add_money_to_wallet_from_card_by_BHD_40_button(self):
    '''
    adds money to wallet by specif flow:
    from debit card.
    utilises 40 bhd dedicated button.
    '''
    try:
        d= driver =  self.driver
        test_name = 'add_money_to_wallet_from_card_by_BHD_40_button'
        status = "FAIL"
        print("current activity",d.current_activity)
        if not checkassert(d,"com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity", "==", d.current_activity ,"check activity is in AddMoneyWalletActivity"):
            back_to_dashboard(d)
        else:
            print("starting point is in Dashboard ")
        # if()
        # use force if want to start always
        #TO_DO:: randomise / config file for user input on data
        
        print("adding money to wallet ")
        
        # check if title is reached by checking if it contains  "Add Money" as text
        title = driver.find_element(By.ID,
                                "com.bfccirrus.bfcpayments.mobile:id/txtAppbarTitle").text
        assert title and ("Add Money" in title)
        checkassert(d,title,"==","Add Money","check title is Add Money")

        # 1. Check 'Available Balance text'
        available_balance_id = driver.find_element(By.ID,
                                                "com.bfccirrus.bfcpayments.mobile:id/txtWalletBal")
        
        assert available_balance_id

        # 3. C'
        # print("type:::",type(available_balance_id.text),"available_balance_id.text",available_balance_id.text)
        available_balance = float(available_balance_id.text)
        #TO_DO::  hardcoding 40 here. make it dynamic
        expected_balance = available_balance +40

        # 4. Click 'BHD 40' button
        bhd_40 = driver.find_element(By.XPATH,
                                    "//android.widget.RadioButton[@text = 'BHD 40']")
        bhd_40.click()

        # 5. Does '40.000' contain '40.000'?
        _40_000 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/etAmount")
        step_output = _40_000.text
        assert step_output and ("40.000" in step_output)

        # 5. Does '40.000' contain '40.000'?
        # 6. Does 'BHD 40.000' contain 'BHD 40.000'?
        bhd_40_000 = driver.find_element(By.ID,
                                        "com.bfccirrus.bfcpayments.mobile:id/txtTotalAmt")
        step_output = bhd_40_000.text
        assert step_output and ("BHD 40.000" in step_output)

        # 7. Make a Swipe gesture from ('605','1482') to ('585','255')
        driver.swipe(start_x=605, start_y=1482, end_x=585, end_y=255, duration=300)

        # 8. Is 'Proceed1' is clickable?
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        assert proceed1.is_enabled()

        # 9. Click 'Proceed1'
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        proceed1.click()
        snackbarfound,snackbarmessage = check_snackbar(d)
        if snackbarfound:
            print("alert snackbar found with message: ",snackbarmessage)
        waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/imgArrow",)

        # 10. Click 'Benefit - Debit/ATM Card' link
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_3 = driver.find_element(By.ID,
                                                                                "com.bfccirrus.bfcpayments.mobile:id/imgArrow")
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_3.click()
        # wait_until(d,"//android.view.View[@text = 'Card Number']",)
        waitfor(d,"//android.view.View[@text = 'Card Number']","xpath")
        # 20. Click 'cardPin1'
        print("now starting to enter pin code '1111' from the UI ,because later xpath might change")
        # cardpin1 = driver.find_element(By.XPATH,
        #                             "//android.view.View[9]//android.widget.EditText")
        cardpinxpath2 = driver.find_element(By.XPATH,"//android.view.View[9]/android.view.View[2]/android.widget.EditText[1]")

        # print(cardpinxpath2.class)
        cardpinxpath2.click()
        
        clearfound = waitfor(d,"//android.widget.Button[@text = 'Clear']","xpath")
        # 21. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 22. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 23. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 24. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 25. Click 'Enter'
        enter = driver.find_element(By.XPATH,
                                    "//android.widget.Button[@text = 'Enter']")
        enter.click()
        # 11. Click 'debitCardNumber'
        debitcardnumber = driver.find_element(By.XPATH,
                                            "//android.view.View[6]/android.widget.EditText")
        debitcardnumber.click()

        # 12. Type '4600411234567890' in 'debitCardNumber'
        # debitcardnumber = driver.find_element(By.XPATH,
        #                                       "//android.view.View[6]/android.widget.EditText")
        debitcardnumber.send_keys(cardnumber)
        check_and_hide_keyboard(d)

        # 13. Click 'MM'
        mm = driver.find_element(By.XPATH,
                                "//android.widget.Spinner[@text = 'MM']")
        mm.click()
        sleep(2) #making sure the list is visible
        #TO_DO ::: write better code to select on date at random
        # 14. Make a Swipe gesture from ('510','1605') to ('508','177')
        driver.swipe(start_x=510, start_y=1605, end_x=508, end_y=177, duration=300)

        # 15. Click '121'
        _12m = driver.find_element(By.XPATH,
                                "//android.widget.CheckedTextView[@text = '12']")
        _12m.click()

        # 16. Click 'YYYY1'
        yyyy = driver.find_element(By.XPATH,
                                    "//android.widget.Spinner[@text = 'YYYY']")
        yyyy.click()
        waitfor(d,"//android.widget.ListView","xpath",sec = 5)
        # 17. Click '2026'
        _2026y = driver.find_element(By.XPATH,
                                    "//android.widget.CheckedTextView[@text = '2026']")
        _2026y.click()
        # if len(d.find_elements(By.XPATH,"//android.widget.ListView"))>0:
        #     android_widget_listview = driver.find_element(By.XPATH,
        #                                           "//android.widget.ListView")
        #     assert not android_widget_listview.is_displayed()
        # 18. Click 'debitCardholderName'
        waitfor(d,"//android.view.View[8]//android.widget.EditText","xpath",sec = 5)
        debitcardholdername = driver.find_element(By.XPATH,
                                                "//android.view.View[8]//android.widget.EditText")
        debitcardholdername.click()
        # 19. Type 'card name' in 'debitCardholderName'
        # debitcardholdername = driver.find_element(By.XPATH,
        #                                           "//android.view.View[8]//android.widget.EditText")
        debitcardholdername.send_keys(cardholdername)
        check_and_hide_keyboard(d)
        ##############################
        # pin enter function was here 
        ##############################
        # 26. Make a Swipe gesture from ('832','1484') to ('840','274')
        driver.swipe(start_x=832, start_y=1484, end_x=840, end_y=274, duration=300)

        # 27. Click 'Pay2'
        pay2 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = 'Pay']")
        pay2.click()

        # 28. Click 'Success!'
        waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/txtSuccessfullyTransferred")
        success_ = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/txtSuccessfullyTransferred")
        success_.click()

        # 29. Click 'Your transaction has been completed s...'
        txnresp = driver.find_element(By.ID,
                                                                    "com.bfccirrus.bfcpayments.mobile:id/txtMessage")
        txnresp.click()

        # 30. Make a Swipe gesture from ('754','1274') to ('745','380')
        driver.swipe(start_x=754, start_y=1274, end_x=745, end_y=380, duration=300)

        # 31. Click 'com.bfccirrus.bfcpayments.mobile:id/i...'
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_ = driver.find_element(By.ID,
                                                                                "com.bfccirrus.bfcpayments.mobile:id/imgMoneyTransfer")
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_.click()

        # 32. Is 'Proceed1' is clickable?
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        assert proceed1.is_enabled()

        # 33. Click 'Proceed1'
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        proceed1.click()
        sleep(2)
        #check for true status in here
        if checkassert(d,expected_balance,"==",go_and_check_dashboardbalance(d)):
            status = "PASS"
            message = "successfully added money"
            return True
        else:
            status = "FAIL"
            message = "successfully added money not updated in dashboard"
            return False
    # except AssertionError:
    #     print("ASSERT ERROR")
    #     message = traceback.format_exc()
    #     print("ERROR :: ",message)
        
    except:
        #
        ##except related cases.
        #<copy paste this except and finally block , add any if anything occurs>
        # self.fail("Encountered an unexpected exception.test failed in "+test_name)
        save_screenshot(d, test_name)
        status = "FAIL"
        # traceback.print_exc()
        message = traceback.format_exc()
        # print(error_message)
        return False
    finally:
        testcasereport(test_name,status,message)
        
#input amt     
def add_money_to_wallet_from_input(self,addamount = 100,**kwargs):
    '''
    adds money to wallet by specific flow:
    from debit card.
    default : adds 100 using text input.
    '''
    try:
        minimal = force
        #to capture details on what called this
        arg = True if int(kwargs.__len__()) != 0 else False
        d= driver =  self.driver
        test_name = 'add_money_to_wallet_from_input__amt='+str(addamount)
        status = "FAIL"
        print("current activity",d.current_activity)
        if not checkassert(d,"com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity", "==", d.current_activity ,"check activity is in AddMoneyWalletActivity"):
            back_to_dashboard(d)
        else:
            print("starting point is in Dashboard ")
        # if()
        # use force if want to start always
        #TO_DO:: randomise / config file for user input on data
        
        print("adding money to wallet ")
        
        # check if title is reached by checking if it contains  "Add Money" as text
        title = driver.find_element(By.ID,
                                "com.bfccirrus.bfcpayments.mobile:id/txtAppbarTitle").text
        assert title and ("Add Money" in title)
        checkassert(d,title,"==","Add Money","check title is Add Money")

        # 1. Check 'Available Balance text'
        available_balance_id = driver.find_element(By.ID,
                                                "com.bfccirrus.bfcpayments.mobile:id/txtWalletBal")
        
        assert available_balance_id

        # 3. C'
        # print("type:::",type(available_balance_id.text),"available_balance_id.text",available_balance_id.text)
        available_balance = float(available_balance_id.text)
        #TO_DO:: . make it dynamic
        expected_balance = available_balance + addamount
        ##############
        
        
        
        # 4. Click edit text
        amountaddtext = d.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/etAmount")
        amountaddtext.click()
        amountaddtext.send_keys(str(addamount)) #sends the amount to be added

        # 5. 5. Does '40.000' contain '40.000'?
        
        amounttextfield = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/etAmount")
        step_output = amounttextfield.text
        assert step_output and (str(addamount) in step_output)
        try:
            driver.press_keycode(66) #pressng enter for 
        finally:
            snackbarfound,snackbartext =  check_snackbar(d,2)
            if not snackbarfound: #if not found / if not False
                print('no snackbar found')
            else:
                print("snackbarfound :")
                raise failed('feeder' if arg else test_name ,snackbartext )
            check_and_hide_keyboard(d)
        
         # 
        # 6. Does 'BHD 40.000' contain 'BHD 40.000'?
        
        ##################################### addamount
        # 6. Does addamount contain addamount'?
        bhd_amt = driver.find_element(By.ID,
                                        "com.bfccirrus.bfcpayments.mobile:id/txtTotalAmt")
        step_output = bhd_amt.text
        assert step_output and ('BHD '+str(addamount) in step_output)

        # 7. Make a Swipe gesture from ('605','1482') to ('585','255')
        driver.swipe(start_x=605, start_y=1482, end_x=585, end_y=255, duration=300)

        # 8. Is 'Proceed1' is clickable?
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        assert proceed1.is_enabled()

        # 9. Click 'Proceed1'
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        proceed1.click()
        waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/imgArrow",)

        snackbarfound,snackbartext =  check_snackbar(d,2)
        if not snackbarfound: #if not found / if not False
            print('no snackbar found')
        else:
            print("snackbarfound :")
            raise failed('feeder' if arg else test_name ,snackbartext )
        check_and_waitforprogressbar(d)
        snackbarfound,snackbartext =  check_snackbar(d,2)
        if not snackbarfound: #if not found / if not False
            print('no snackbar found')
        else:
            print("snackbarfound :")
            raise failed('feeder' if arg else test_name ,snackbartext )
        # 10. Click 'Benefit - Debit/ATM Card' link
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_3 = driver.find_element(By.ID,
                                                                                "com.bfccirrus.bfcpayments.mobile:id/imgArrow")
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_3.click()
        # wait_until(d,"//android.view.View[@text = 'Card Number']",)
        waitfor(d,"//android.view.View[@text = 'Card Number']","xpath")
        # 20. Click 'cardPin1'
        print("now starting to enter pin code '1111' from the UI ,because later xpath might change")
        # cardpin1 = driver.find_element(By.XPATH,
        #                             "//android.view.View[9]//android.widget.EditText")
        cardpinxpath2 = driver.find_element(By.XPATH,"//android.view.View[9]/android.view.View[2]/android.widget.EditText[1]")

        # print(cardpinxpath2.class)
        cardpinxpath2.click()
        
        clearfound = waitfor(d,"//android.widget.Button[@text = 'Clear']","xpath")
        # default pin is '111111'
        # 21. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 22. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 23. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 24. Click '1'
        _1 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = '1']")
        _1.click()

        # 25. Click 'Enter'
        enter = driver.find_element(By.XPATH,
                                    "//android.widget.Button[@text = 'Enter']")
        enter.click()
        # 11. Click 'debitCardNumber'
        debitcardnumber = driver.find_element(By.XPATH,
                                            "//android.view.View[6]/android.widget.EditText")
        debitcardnumber.click()

        # 12. Type '4600411234567890' in 'debitCardNumber'
        # debitcardnumber = driver.find_element(By.XPATH,
        #                                       "//android.view.View[6]/android.widget.EditText")
        debitcardnumber.send_keys(cardnumber)
        check_and_hide_keyboard(d)

        # 13. Click 'MM'
        mm = driver.find_element(By.XPATH,
                                "//android.widget.Spinner[@text = 'MM']")
        mm.click()
        sleep(2) #making sure the list is visible
        #TO_DO ::: write better code to select on date at random
        # 14. Make a Swipe gesture from ('510','1605') to ('508','177')
        driver.swipe(start_x=510, start_y=1605, end_x=508, end_y=177, duration=300)

        # 15. Click '121'
        _12m = driver.find_element(By.XPATH,
                                "//android.widget.CheckedTextView[@text = '12']")
        _12m.click()

        # 16. Click 'YYYY1'
        yyyy = driver.find_element(By.XPATH,
                                    "//android.widget.Spinner[@text = 'YYYY']")
        yyyy.click()
        waitfor(d,"//android.widget.ListView","xpath",sec = 5)
        # 17. Click '2026'
        _2026y = driver.find_element(By.XPATH,
                                    "//android.widget.CheckedTextView[@text = '2026']")
        _2026y.click()
        # if len(d.find_elements(By.XPATH,"//android.widget.ListView"))>0:
        #     android_widget_listview = driver.find_element(By.XPATH,
        #                                           "//android.widget.ListView")
        #     assert not android_widget_listview.is_displayed()
        # 18. Click 'debitCardholderName'
        waitfor(d,"//android.view.View[8]//android.widget.EditText","xpath",sec = 5)
        debitcardholdername = driver.find_element(By.XPATH,
                                                "//android.view.View[8]//android.widget.EditText")
        debitcardholdername.click()
        # 19. Type 'card name' in 'debitCardholderName'
        # debitcardholdername = driver.find_element(By.XPATH,
        #                                           "//android.view.View[8]//android.widget.EditText")
        debitcardholdername.send_keys(cardholdername)
        check_and_hide_keyboard(d)
        ##############################
        # pin enter function was here 
        ##############################
        # 26. Make a Swipe gesture from ('832','1484') to ('840','274')
        driver.swipe(start_x=832, start_y=1484, end_x=840, end_y=274, duration=300)

        # 27. Click 'Pay2'
        pay2 = driver.find_element(By.XPATH,
                                "//android.widget.Button[@text = 'Pay']")
        pay2.click()

        # 28. Click 'Success!'
        waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/txtSuccessfullyTransferred")
        success_ = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/txtSuccessfullyTransferred")
        success_.click()
        
        print("payment process response received , checking for status is success or not ")
        # success
        print("\n\n\n\ncheck result with csv ,expected")
        # failed = contains faile = true and contains faile = true) true
        # failed = contains failed = false and contains faile = true) false
        #failed = contains failed = false and contains faile = false)  false
        
        #failed = 
        # 'Your transaction has been completed successfully'
        txnresp = driver.find_element(By.ID,"com.bfccirrus.bfcpayments.mobile:id/txtMessage")
        txnresp.click()
        
        failedcheckconditions =(checkassert(d,txnresp.text,'not contains','failed','checking for "payment failed" as text in payment response') and checkassert(d,success_.text,'not contains','Payment failed','checking for "payment failed" as text in payment response'))
        successcheckconditions = checkassert(d,txnresp.text,'contains','successfully','checking for "successfully" as text in payment response') and checkassert(d,(success_.text).casefold(),'contains','success','checking for "success" as text in payment response')
        if not expected and failedcheckconditions :
                print('The test is Expected to fail , and the condition have been failed')
        elif expected and successcheckconditions:
                print("there is code incompletion in this area")
        else:
            print('\033[5mONE OF THE CHECK HAS BEEN FAILED <SOME ERROR MUST BE OCCURED IN RESPONSE UI \033[0m')
                
            
            # if :
            #     print('payment process could not succeeded .error message shown :\n\t\t'+txnresp.text )
                
                
        # if checkassert(d,success_.text,'not contains','Payment failed','checking for "payment failed" as text in payment response'):
            
            

        # 29. Click 'Your transaction has been completed s...'

        
            
        

        # 30. Make a Swipe gesture from ('754','1274') to ('745','380')
        driver.swipe(start_x=754, start_y=1274, end_x=745, end_y=380, duration=300)

        # 31. Click 'com.bfccirrus.bfcpayments.mobile:id/i...'
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_ = driver.find_element(By.ID,
                                                                                "com.bfccirrus.bfcpayments.mobile:id/imgMoneyTransfer")
        com_bfccirrus_bfcpayments_mobile_colon_id_slash_i_.click()

        # 32. Is 'Proceed1' is clickable?
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        assert proceed1.is_enabled()

        # 33. Click 'Proceed1'
        proceed1 = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/btnProceed")
        proceed1.click()
        sleep(2)
        #check for true status in here
        if checkassert(d,expected_balance,"==",go_and_check_dashboardbalance(d)):
            status = "PASS"
            message = "successfully added money"
            return True
        else:
            status = "FAIL"
            message = "successfully added money not updated in dashboard"
            return False
    # except AssertionError:
    #     print("ASSERT ERROR")
    #     message = traceback.format_exc()
    #     print("ERROR :: ",message)
    except failed as e:
        print("(failed)alert message is : \n", e.message)
        status = "FAIL"
        message = e.message
        tr = False
        
    except Exception as e:
        #
        ##except related cases.
        #<copy paste this except and finally block , add any if anything occurs>
        # self.fail("Encountered an unexpected exception.test failed in "+test_name)
        save_screenshot(d, test_name)
        status = "FAIL"
        traceback.print_exc()
        message = e
        # print(error_message)
        return False
    finally:
        testcasereport(test_name,status,message)
        