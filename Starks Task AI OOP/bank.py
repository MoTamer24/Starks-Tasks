from bankAccount import BankAccount

class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self._next_account_id = 1000
    
    def _generate_account_number(self):
        acc_num = f"{self._next_account_id:06d}"
        self._next_account_id += 1
        return acc_num
    
    def create_account(self, password, owner, balance=0.0):
        account_number = self._generate_account_number()
        new_account = BankAccount(account_number, password, owner, balance)
        self.accounts[account_number] = new_account
        return account_number
    
    def get_account(self, account_number):
        return self.accounts.get(account_number)
    
    def authenticate(self, account_number, password):
        account = self.accounts.get(account_number)
        if account and account.verify_password(password):
            return account
        return None