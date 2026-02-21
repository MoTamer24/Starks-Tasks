class BankAccount:
    def __init__(self, account_number, password, owner, balance=0.0):
        self.account_number = account_number
        self.__password = password
        self.owner = owner
        self.__balance = balance
    
    def verify_password(self, password):
        return self.__password == password
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True
    
    def transfer_out(self, amount):
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True
    
    def transfer_in(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def get_balance(self):
        return self.__balance
    
    def get_info(self):
        return {
            'account_number': self.account_number,
            'owner': self.owner,
            'balance': self.__balance
        }