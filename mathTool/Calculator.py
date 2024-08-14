import math
from database.DataOps import DataOps

class Calculator:
    #addition, subtraction, multiplication, division, square_root, random_string'
    user = ''

    def __init__(self, user):
        self.user = user 
        
    def RegisterOperation(
        self,
        amount,
        operation_response, operation
    ):
        
        try:
            da = DataOps()          
            da.SaveOperationRecord(operation, self.user, amount, 100, operation_response)
            
            
        except Exception as e:
            raise Exception('There is an error that states '+ str(e))

    
    def SquareRoot(self, num : float, operation):    
        try:
            
            if(num==0):
                return 0
             
            if(num<0):
                raise Exception('The square root of a negative number is undefined in the context of real numbers.')
            number = math.sqrt(num)
            self.RegisterOperation(num,number, operation)
            return number
        except Exception as e:
            raise e
    
    def Addition(self, a: float, b: float,operation):
        try:
            number = a + b
            self.RegisterOperation(number,number, operation)
            return number
        except Exception as e:
            raise e
    
    def Subtraction(self, a: float, b: float, operation):
        try:
            number = a - b             
            self.RegisterOperation(number, number, operation)
            return number
        except Exception as e:
            raise e
    
    def Multiplication(self, a: float, b: float,operation):
        try:
            number = a * b
            self.RegisterOperation(number,number,operation)
            return number
        except Exception as e:
            raise e
    
    def Division(self, a: float, b: float,operation):
        try:
            if(b == 0):
                raise ZeroDivisionError('B must be a value different than Zero! You can not divide by Zero!')
            number = a / b
            self.RegisterOperation(number,number,operation)
            return number
        except Exception as e:
            raise e
    
