class ATM:
    def __init__(self, bank):
        self.bank = bank
        self.current_account = None
    
    def login(self, account_number, password):
        self.current_account = self.bank.authenticate(account_number, password)
        return self.current_account is not None
    
    def logout(self):
        self.current_account = None
    
    def is_logged_in(self):
        return self.current_account is not None
    
    def deposit(self, amount):
        if not self.is_logged_in():
            return False
        return self.current_account.deposit(amount)
    
    def withdraw(self, amount):
        if not self.is_logged_in():
            return False
        return self.current_account.withdraw(amount)
    
    def transfer(self, target_account_number, amount):
        if not self.is_logged_in():
            return False
        target = self.bank.get_account(target_account_number)
        if target is None:
            return False
        if self.current_account.transfer_out(amount):
            target.transfer_in(amount)
            return True
        return False
    
    def check_balance(self):
        if not self.is_logged_in():
            return None
        return self.current_account.get_balance()
    
    def get_account_info(self):
        if not self.is_logged_in():
            return None
        return self.current_account.get_info()