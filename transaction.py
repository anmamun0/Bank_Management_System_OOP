class Transaction:
    def __init__(self,action,amount,date,current_balance,after_balance) -> None:
        self.action = action
        self.amount = amount 
        self.date = date 
        self.current_balance = current_balance
        self.after_balance = after_balance

