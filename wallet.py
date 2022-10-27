from tkinter import E
from customclasses import failed, splashloadtooklong
from dashboard import go_and_check_dashboardbalance
from util import *
from time import sleep
import traceback
from selenium.webdriver.common.by import By



def add_money_to_wallet_from_card_by_BHD_20_button(self):
    '''
    adds money to wallet by specific flow:
    from debit card.
    utilises 20 bhd dedicated button.
    '''
    try:
        d= driver =  self.driver
        test_name = 'add_money_to_wallet_from_card_by_BHD_20_button'
        status = "FAIL"
        message = "unexpected error occured in "+test_name
        expected = True
        print("current activity",d.current_activity)
        assert "com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity" == d.current_activity,"it is not in view of add money wallet"
        checkassert(d,"com.bfc.bfcpayments.modules.wallet.view.AddMoneyWalletActivity","==",d.current_activity)
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

        available_balance = float(available_balance_id.text)
        #TO_DO::  hardcoding 20 here. make it dynamic
        expected_balance = available_balance +20

        # 4. Click 'BHD 20' button
        bhd_20 = driver.find_element(By.XPATH,
                                    "//android.widget.RadioButton[@text = 'BHD 20']")
        bhd_20.click()
        print("button 20 bhd clicked")
        

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
        print("proceed button found , clicking it")

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
        successtransferfound = waitfor(d,"com.bfccirrus.bfcpayments.mobile:id/txtSuccessfullyTransferred")
        success_ = driver.find_element(By.ID,
                                    "com.bfccirrus.bfcpayments.mobile:id/txtSuccessfullyTransferred")
        success_.click()
        checkassert(d,successtransferfound,'==',True,'successfully transferred screen found')

        # 29. Click 'Your transaction has been completed s...'
        txnresp = driver.find_element(By.ID,
                                                                    "com.bfccirrus.bfcpayments.mobile:id/txtMessage")
        print("transaction report : ",txnresp.text)
        txnresp.click()
        print("checking conditions")
        failedcheckconditions =(checkassert(d,txnresp.text,'not contains','failed','checking for "payment failed" as text in payment response') and checkassert(d,success_.text,'not contains','Payment failed','checking for "payment failed" as text in payment response'))
        successcheckconditions = checkassert(d,txnresp.text,'contains','successfully','checking for "successfully" as text in payment response') and checkassert(d,(success_.text).casefold(),'contains','success','checking for "success" as text in payment response')
        txnsuccess = checkassert(d,successtransferfound,'==',successcheckconditions, "checking if transaction resp text matches in UI")
        if not expected and failedcheckconditions :
                print('The test is Expected to fail , and the condition have been failed')
        elif expected and successcheckconditions:
                print("test case successfully completed as success, ")
                print("now checking for the balance ")
        else:
            print('\033[5mONE OF THE CHECK HAS BEEN FAILED <SOME ERROR MUST BE OCCURED IN RESPONSE UI \033[0m')

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

        proceed1.click()
        sleep(2)
        #check for true status in here
                # check =wait_until_activity(d,"com.bfc.bfcpayments.modules.pay.view.PayMainActivity","visible")
        # visibility	visible
        # true android.widget.ProgressBar
        currentbal = go_and_check_dashboardbalance(d)
        check_and_waitforprogressbar(d)
        if checkassert(d,expected_balance,"==",currentbal):
            status = "PASS"
            message = "successfully added money"
            tr = True
            # return True
            if not txnsuccess:
                status = "FAIL"
                message = "Transaction Failed but money is updated"
                tr = 'warn'

        else:
            if txnsuccess and currentbal == available_balance :
                status = "FAIL"
                message = "successfully added money not UPDATED in dashboard"
                tr = 'warn'
            elif txnsuccess and currentbal != expected_balance :
                status = "FAIL"
                message = "transaction successfully completed but money not UPDATED correctly in dashboard"
                tr = 'warn'
            elif not txnsuccess:
                status = "FAIL"
                message = "Transaction Failed and money not updated"
                tr = 'warn'

    # except AssertionError:
    #     print("ASSERT ERROR")
    #     message = traceback.format_exc()
    #     print("ERROR :: ",message)

    except Exception as e:
        save_screenshot(d, test_name)
        status = "FAIL"
        message = e
        tr = False
    except:
        save_screenshot(d, test_name)
        status = "FAIL"
        message = traceback.format_exc()
        # print(error_message)
        tr = False
    finally:
        testcasereport(test_name,status,message)
        return tr

