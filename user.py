from datetime import datetime  
from transaction import Transaction 

class Admin:
    def __init__(self,bank) -> None:
        self.user = 'admin'
        self.password = '1234'
        self.bank = bank 

    def create_account(self,name,email,address,phone,account_type):
        person = User(name,email,address,phone,account_type)
        self.bank.create_account(person)

    def remove_account(self,account_no):
        return self.bank.remove_account(account_no)
    
    def ban_account(self,account_no,clock):
        self.bank.ban_account(account_no,clock)
    
    
    def view_users(self):
        self.bank.view_users()

    def bank_balance(self):
        return self.bank.bank_balance  
    
    def is_loan(self):
        return self.bank.is_loan
    
    def set_loan(self,clock):
        self.bank.is_loan = clock

class User:
    def __init__(self,name,email,address,phone,account_type) -> None:
        self.name = name 
        self.email = email 
        self.address = address 
        self.phone = phone
        self.account_type = account_type
        self.bank = None 
        self.account = None 
        self.transection = []

    def deposit(self,amount):
        if self.account.ban == True:
            print("Your Bank is Bankrupt ...!")
            return 
        current_balance = self.account.balance
        self.account.balance += amount
        self.bank.balance += amount

        trans = Transaction('deposit',amount,datetime.now(),current_balance,self.account.balance)
        self.transection.append(trans)


    def withdraw(self,amount):
        check = self.bank.track_withdraw(self,amount)
        if check == None:
            print("Unsuccessfull Transaction, Your Account Backrupt !")
             
        elif check == False:
            print("Unsuccessfull Transaction..!")
            print("Your need to have 500 tk in your account.!") 
        else:
            current_balance = self.account.balance
            self.account.balance -= amount
            self.bank.balance -= amount

            trans = Transaction('withdrow',amount,datetime.now(),current_balance,current_balance-amount)
            self.transection.append(trans)

        return check
    def transfer(self,other,amount):
        action =  self.bank.transfer(self,other,amount)
        if action == True:
            trans = Transaction('transfer',amount,datetime.now(),self.account.balance,self.account.balance-amount)
            self.transection.append(trans)
        return action
    
    def request_loan(self,amount):
        action = self.bank.request_loan(self,amount)
        if action == True:
            self.account.balance += amount 
            self.account.loan_times += 1
            trans = Transaction('loan',amount,datetime.now(),self.account.balance,self.account.balance+amount)
            self.transection.append(trans)
        else :
            print("Request Faild..!")

        return action
    
    @property
    def check_balance(self):
        return self.account.balance
    
    def details(self):
        text =  (
        f"{'-'*10} My Profile{'-'*10}\n"
            f"Account No : {self.account.account_no }\n"
            f"Name : {self.name}\n"
            f"Email : {self.email}\n"
            f"Address : {self.address}\n"
            f"Address : {self.address}\n"
            f"Phone : {self.phone}\n"
            f"Current Balance : {self.account.balance}\n"
            f"Loan Balance : {self.account.loan}\n"
            f"Loan_timer : {self.account.loan_times}\n"
            f"Activeity : {self.account.ban}\n"
        f"{'-'*30}\n"
        ) 
        return text
    def transaction_history(self):
        for tran in self.transection:
            print(f"Action: '{tran.action}' | Amount: {tran.amount} | After Balance: {tran.after_balance} | Date: {tran.date.strftime('%I:%M:%S') }")


