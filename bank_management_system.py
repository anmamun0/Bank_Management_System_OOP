from datetime import datetime   
import textwrap 

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
        elif user.account.balance - amount < 0:
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
            print("Account does not exis..!")
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
            print(f"Withdrawal amount exceeded")
            print("Unsuccessfull Transaction..!\n")
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


class Transaction:
    def __init__(self,action,amount,date,current_balance,after_balance) -> None:
        self.action = action
        self.amount = amount 
        self.date = date 
        self.current_balance = current_balance
        self.after_balance = after_balance

class Account:
    def __init__(self,account_no) -> None:
        self.account_no = account_no 
        self.balance = 0
        self.loan = 0
        self.loan_times = 0
        self.ban = False  
    



# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------main.py

 
def user_pannel(bank,user):
    while True:
        print(f"{'-'*40}")
        print(' '*10,f"1. Deposit Money: ")
        print(' '*10,f"2. With Draw Money ")
        print(' '*10,f"3. Transfer Balance")
        print(' '*10,f"4. Take Loan ")
        print(' '*10,f"5. Check Balance")
        print(' '*10,f"6. Transaction History Print")
        print(' '*10,f"7. My Details ")
        print(' '*10,f"8. Exit")
        print(f"{'-'*20}",end='') 

        choice = int(input("Enter Your Choice: "))
        if choice == 1: 
            tk = int(input("Enter Your Money: "))
            user.deposit(tk)
            print()
        elif choice == 2: 
            tk = int(input("Enter Your Money: "))
            action = user.withdraw(tk)

            if action == True: 
                print(f"Successfully With Draw {tk} tk | Your current Balance: {user.check_balance}")
            print() 
        elif choice == 3:
            other = int(input("Enter Receiver account: "))
            amount = int(input("Enter amount: "))
            tran = user.transfer(other,amount)

            if tran == True:
                print(f"Successfull Transfer ! your current amount: {user.check_balance}")
            print()
        elif choice == 4:
            amount = int(input("Enter Your Loan amount: "))
            action = user.request_loan(amount)
            if action == True:
                print("Successl loan approved.. \n")

        elif choice == 5: 
            print(f"Your Current Balance: {user.check_balance}")
            print()
        elif choice == 6: 
            user.transaction_history()
            print()
        elif choice == 7:  
            details = user.details()
            print(textwrap.indent(details,' '*10))
        elif choice == 8:
            break 

def login(bank):
    ac = int(input("Enter Your account No: "))
    for user in bank.users:
        if user.account.account_no == ac:
            print(f" {'-'*10} Welcome Back - {user.name} ! {'-'*10}")
            if user.account.ban == True:
                print(f"Your Account is bankrupt, Your can login.. ")
                return
            return user_pannel(bank,user)
    print("----------Your are not member of this Bank!\n")

def signin(bank):
    name  = input(f"{' '*4}Enter Your Name : ")
    email  = input(f"{' '*4}Enter Your Email : ")
    address  = input(f"{' '*4}Enter Your Address : ")
    phone  = input(f"{' '*4}Enter Your phone : ")
    account_type  = input(f"{' '*4}Enter Your Account_type (savings/current) : ")
    user = User(name,email,address,phone,account_type)
    print(f" {'-'*10} Welcome Our New Member - {name} ! {'-'*10}")
    bank.create_account(user)
    user_pannel(bank,user)

def admin_pannel(bank,user_id,password):
    admin = bank.request_admin(user_id,password)
    if admin == None:
        print(f"Your are not admin .. please try again")
        return 
    
    while True:
        print(f" {'-'*15} Admin Pannel - ! {'-'*10}")
        print(' '*10,f"1. Create account ")
        print(' '*10,f"2. Remove_account ")
        print(' '*10,f"3. Ban Account ")
        print(' '*10,f"4. View All Users ")
        print(' '*10,f"5. Bank Current Balance ")
        print(' '*10,f"6. Set loan Activity (True/False) ")
        print(' '*10,f"7. Exit(admin Pannel) ")
        print(f"{'-'*20}",end='')
        choice = int(input("Enter Your Choice: "))

        if choice == 1:
            name  = input(f"{' '*4}Enter Your Name : ")
            email  = input(f"{' '*4}Enter Your Email : ")
            address  = input(f"{' '*4}Enter Your Address : ")
            phone  = input(f"{' '*4}Enter Your phone : ")
            account_type  = input(f"{' '*4}Enter Your Account_type (savings/current) : ")
            admin.create_account(name,email,address,phone,account_type)
            print("Creat Successfull...\n")

        elif choice == 2:
            account_no = int(input("Enter Account No: "))
            action = admin.remove_account(account_no)
            if action != None:
                print("Remove account successfull...\n")

        elif choice == 3:
            account_no = int(input("Enter account No: "))
            clock = input("if want to Ban(True) or UnBan(False)?  ")
            if clock == "True":
                admin.ban_account(account_no,True)
                print(f"{account_no} is Ban..\n")
            elif clock == "False":
                admin.ban_account(account_no,False) 
                print(f"{account_no} is free from Ban..,Congratulation\n")
            else:
                print("Type Error\n")

        elif choice == 4:
            admin.view_users()
            print()
        elif choice == 5:
            print(f"Bank current Balance: {admin.bank_balance()}\n")
            print() 
        elif choice == 6:
            clock = input("Enter True/False : ")
            if clock == 'True':
                admin.set_loan(True)
                print("Loan activated succesfull..\n")
            elif clock == "False":
                admin.set_loan(False)
                print("Loan inaction succesfull..\n")
            else:
                print("Type Error...\n")
        elif choice == 7:
            break 
         


AN = Bank("AN Coder" ,'Sylhet, Bangladesh',1000000)

while True:
    print(f"\nWelcome Our {AN.name} Bank..!")
    print("1. User: ")
    print("2. Admin: ")
    print("3. Exit : ")
    choice = int(input("Enter Your Choice: >> "))
    if choice == 1:
        clock = input("Login(L) or Signin(S) ? >> ").lower()
        if clock == 'l':
            login(AN)
        else:
            signin(AN)

    elif choice == 2:
        user_id = input("Enter User ID (admin) : ")
        password = input("Enter Password (1234): ")
        admin_pannel(AN,user_id,password)
        pass 
    elif choice == 3:
        break




    