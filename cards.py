from dashboard import click_cards
from util import *
from config import *
# from util import wait_until_activity
from time import sleep
import traceback
from selenium.webdriver.common.by import By

cardoccurance = 0

def agree_activation(self,minimal = False): #debit card
    '''
    just checks if the activation screen is present or not.
    put minimal as true , if just checking on a routine - it will not raise any issues\n
    
    '''
    # test_name = 'signout_and_reach_register_page'
    message = 'unexpected error occured when activation agreement'
    # status = "FAIL"
    d = driver = self.driver
    tr =False
    try:
        # id	@id/txtActivateYourBfcPayCard d.find_element(By.ID,'txtForgotPin').click()
#finding if activation is showed
        txtActivateYourBfcPayCards = d.find_elements(By.ID,'txtActivateYourBfcPayCard')   
#enter only if activation is shown
        if len(txtActivateYourBfcPayCards)>0:
            txtActivateYourBfcPayCard  =txtActivateYourBfcPayCards[0] 
            #  'Activate your BFC Pay Card'
            #check id	@id/txtWelcomeText contains logged name
            checkassert(d,txtActivateYourBfcPayCard.text,'==','Activate your BFC Pay Card','BFC PAY card activation loaded?')

            txtWelcomeText = d.find_element(By.ID,'txtWelcomeText')
            if checkassert(d,txtWelcomeText.text,'contains',loggedname,'check name is accurate in consent and preparation'):
                # id	@id/checkBoxTnc clcik
# if not clcicking this there will be a toast alert saying ' please alert terms and condition' no flow required
                d.find_element(By.ID,'checkBoxTnc').click()
                print("check box clicked")
                #id	@id/btnActivateNewCard  button click
                d.find_element(By.ID,'btnActivateNewCard').click()
                print("activate button clicked")
                ####################
                # next screen
                print('write screen check')
                ###########3
                tr= True
                message = 'card activation click successful'
            else:
                print("\tthe logged in user name -",loggedname," is not in consent text")
                tr= False 
                message ='logged in user welcome text could not found'
                
#if activation consent not shown , assume user has already gone through and accepted this before. check if next screen present
        else:
            print("activation consent may be already passed, checking the next screen presence")
            tr = 'warn'
            message = 'activation screen not seen'
    finally:
        return tr,message
        
    
def register_cards(self,minimal = False): #debit card
    '''
    just checks if the activation screen is present or not.
    put minimal as true , if just checking on a routine - it will not raise any issues\n
    
    '''
    test_name = 'register_cards'
    message = 'unexpected error occured in '+test_name
    status = "FAIL"
    d = driver = self.driver
    tr =False
    try:
        print("checking for the agreement")
        activation,message = agree_activation(self)
        print("agree activation test status response is ",activation,'with message ',message)
        test_name = 'signout_and_reach_register_page'
        message = 'unexpected error occured in '+test_name
        status = "FAIL"
        print("d.current_activity after agreement is ",d.current_activity)
        if d.current_activity == cardsactivity : #true case agrreement 
            print("it is in cards activity")
        else: #fail warn
            
            if force and cardoccurance == 0:
                cardoccurance = 1
                status = 'warn'
                message = 'register card failed in '+test_name
                
                click_cards(self)
                register_cards(self)
            else:
                test_name = 'register cards'
                message = 'register card failed in '+test_name
                status = "FAIL"

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
    
def check_MC_card_status(self):
    print("this is mc status first line")
    d = driver =  self.driver
    test_name = 'check_MC_card_status'
    status = "FAIL"
    message = "unexpected error occured in "+test_name
    # com.android.tools.idea.layoutinspector.tree.TreeViewNode@5edecaab
    try:

        # id	@id/btnApplyButtonTravelBuddy
        print("checking for the mc card status")
        wait_until(d,'btnApplyButtonTravelBuddy',visible)
        applybtntext = d.find_element(By.ID,'btnApplyButtonTravelBuddy').text
        print("checking for the mc button status",applybtntext)
        if applybtntext == 'Apply':
            print("\tcard isnt applied with this user. checking the steps")
            if expectedmcflow == [] or 'newuser' in expectedmcflow :
                if expectedmcflow == []:
                    print(YELLOW +" \texpected flow not defined the flow will continue please define the flow for more accurate result"+CRESET)
                else:
                    print("the user is expected to be new user")
            else:
                # if any flow keyword is to be excluded pass it here
                if force:
                    print("flow is not expected , but with force on trying to complete the flow")
                    
                else:
                    message = "Flow is not expected and force is not enabled , please recheck the flow and retry if it is not intended" 
                    status = "FAIL"
                    tr = False
                    print(message)
        elif applybtntext == 'Manage' or  applybtntext == 'manage':
            print("\n\n manage flow is incomplete")
        elif applybtntext == 'replace' or  applybtntext == 'Replace':
            print("\n\n replace flow is incomplete")
        else:
            print("applybtn text is",applybtntext)
            print("\nthis is not expected as an option , please update the testcase")
    
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
        
        
    
    
    