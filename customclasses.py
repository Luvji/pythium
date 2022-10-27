class Error(Exception):
    """Base class for other exceptions"""
    print()
    pass

class failed(Error):
    """Testcase failed"""
    def __init__(self, test_name = "Not Available", message="Custom Error not Provided"):
        self.test_name = test_name
        self.message = message
        print("in ",test_name)
        print(message)
        
        super().__init__(self.message)
        
class splashloadtooklong(Exception):
    def __init__(self,  message="splash took too long"):
        self.message = message
        print(message)
        super().__init__(self.message)
    pass

class noelement(Error):
    """Testcase check failed"""
    def __init__(self, test_name = "Not Available", message="Custom Error not Provided"):
        self.test_name = test_name
        self.message = message
    
        print(message)
        
        super().__init__(self.message)

