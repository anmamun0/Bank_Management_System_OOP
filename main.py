from bank_management import Bank
from user import User 
import textwrap
 
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
