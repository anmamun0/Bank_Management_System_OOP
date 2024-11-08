from account import Account 
from user import Admin
class Bank:
    serial  = 123100000
    def __init__(self,name,location,invest) -> None:
        self.name = name
        self.location = location  
        self.balance = invest
        self.loan_available = True
        self.loan = 0 
        self.users = []
        self.request = []

    def account_generate(self):
        self.serial += 1
        return self.serial
    def access_admin(self,user_id,password):
        if user_id == 'admin' and password == '1234':
            return Admin()
        return None 
    
    def create_account(self,user):
        account = Account(self.account_generate())
        user.account = account 
        user.bank = self
        self.users.append(user)

    def remove_account(self,account_no):
        user = None
        for person in self.users:
            if person.account.account_no == account_no:
                user = person
                break 
        self.users.remove(user)
        return user
    
    def ban_account(self,account_no,clock):
        person = None 
        for user in self.users:
            if user.account.account_no == account_no:
                user.account.ban = clock
                person = user 
                break 
        return person
    def request_loan(self,user,amount):
        if user.account.ban == True or user.account.loan_times>=2 or self.balance-amount < 0:
            return False
        return True

    def view_users(self):
        print(f"Total Account is : {len(self.users)}")

        for user in self.users:
            print(f"Acc_No : {user.account.account_no} | Balance:  {user.account.balance} | User_Name: {user.name}")
         
    @property
    def is_loan(self):
        return self.loan_available 
    
    @is_loan.setter
    def is_loan(self,clock):
        self.loan_available = clock

    @property
    def bank_balance(self):
        return self.balance
 
     
    def track_withdraw(self,user,amount):
        if user.account.ban == True:
            return None 
        elif user.account.balance - amount <= 500:
            return False
        else :
            return True
         
        
    def transfer(self,user,other_account_no,amount):
        other = None 
        for person in self.users:
            if person.account.account_no == other_account_no:
                other = person
                break
        if other == None:
            print("This account is invalid..!")
            return None 
        if user.account.ban == True or other.account.ban == True:
            print("Bankrupt Account , Can't   Transfer")
            return False
        
        withdraw = user.withdraw(amount)
        if withdraw == True:
            other.deposit(amount)
        return True 

    def request_admin(self,user,password):
        admin = None

        if user == 'admin' and password =='1234':
            admin = Admin(self)
        return admin 

 