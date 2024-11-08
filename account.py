class Account:
    def __init__(self,account_no) -> None:
        self.account_no = account_no 
        self.balance = 0
        self.loan = 0
        self.loan_times = 0
        self.ban = False  
    