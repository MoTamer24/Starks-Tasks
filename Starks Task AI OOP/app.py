import os
from bank import Bank
from atm import ATM

# Minimalist ANSI color codes for terminal styling
class Style:
    HEADER = '\033[1;36m'  # Bold Cyan
    PROMPT = '\033[1;33m'  # Bold Yellow
    SUCCESS = '\033[92m'   # Green
    ERROR = '\033[91m'     # Red
    INFO = '\033[94m'      # Blue
    MUTED = '\033[90m'     # Gray
    RESET = '\033[0m'      # Reset to default
    BOLD = '\033[1m'       # Bold white

def clear_screen():
    """Clears the terminal for a cleaner UX."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_success(msg):
    print(f"{Style.SUCCESS}✔ {msg}{Style.RESET}")

def print_error(msg):
    print(f"{Style.ERROR}✖ {msg}{Style.RESET}")

def print_info(msg):
    print(f"{Style.INFO}ℹ {msg}{Style.RESET}")

def select_bank(banks):
    print(f"\n{Style.HEADER}=== Available Banks ==={Style.RESET}")
    for key, bank in banks.items():
        print(f"  {Style.BOLD}[{key}]{Style.RESET} {bank.name}")
    print(f"{Style.MUTED}-----------------------{Style.RESET}")
    
    choice = input(f"{Style.PROMPT}Select bank (1-{len(banks)}): {Style.RESET}").strip()
    return banks.get(choice)

def main():
    banks = {
        "1": Bank("National Bank"),
        "2": Bank("Cairo Bank"),
        "3": Bank("Bank Misr")
    }

    clear_screen()
    print(f"{Style.HEADER}Welcome to the Universal ATM System{Style.RESET}")

    while True:
        selected_bank = select_bank(banks)
        if not selected_bank:
            print_error("Invalid bank selection. Please try again.")
            continue

        atm = ATM(selected_bank)
        clear_screen()

        while True:
            # Check login state to render the menu dynamically
            logged_in = atm.is_logged_in()
            status = f"{Style.SUCCESS}Logged In{Style.RESET}" if logged_in else f"{Style.MUTED}Guest{Style.RESET}"
            
            print(f"\n{Style.HEADER}=== 🏦 {selected_bank.name} ATM ==={Style.RESET}")
            print(f"Status: {status}")
            print(f"{Style.MUTED}-----------------------{Style.RESET}")
            
            if not logged_in:
                print(f"  {Style.BOLD}[1]{Style.RESET} Login")
                print(f"  {Style.BOLD}[2]{Style.RESET} Create Account")
            else:
                print(f"  {Style.BOLD}[3]{Style.RESET} Deposit")
                print(f"  {Style.BOLD}[4]{Style.RESET} Withdraw")
                print(f"  {Style.BOLD}[5]{Style.RESET} Transfer")
                print(f"  {Style.BOLD}[6]{Style.RESET} Check Balance")
                print(f"  {Style.BOLD}[7]{Style.RESET} Account Info")
                print(f"  {Style.BOLD}[8]{Style.RESET} Logout")
            
            print(f"  {Style.BOLD}[9]{Style.RESET} Switch Bank")
            print(f"  {Style.BOLD}[10]{Style.RESET} Exit")
            print(f"{Style.MUTED}-----------------------{Style.RESET}")

            choice = input(f"{Style.PROMPT}Choice: {Style.RESET}").strip()
            print() # Add an empty line for breathing room

            match choice:
                case '1':
                    if logged_in:
                        print_info("Already logged in.")
                        continue
                    acc_num = input(f"{Style.PROMPT}Account number: {Style.RESET}").strip()
                    pwd = input(f"{Style.PROMPT}Password: {Style.RESET}").strip()
                    if atm.login(acc_num, pwd):
                        print_success("Login successful")
                    else:
                        print_error("Login failed. Check your credentials.")

                case '2':
                    if logged_in:
                        print_info("Please logout to create a new account.")
                        continue
                    owner = input(f"{Style.PROMPT}Owner name: {Style.RESET}").strip()
                    pwd = input(f"{Style.PROMPT}Password: {Style.RESET}").strip()
                    try:
                        balance_input = input(f"{Style.PROMPT}Initial balance (default 0): {Style.RESET}")
                        balance = float(balance_input) if balance_input else 0.0
                    except ValueError:
                        balance = 0.0
                    
                    acc_num = selected_bank.create_account(pwd, owner, balance)
                    print_success(f"Account created successfully! Your Account Number is: {Style.BOLD}{acc_num}{Style.RESET}")

                case '3':
                    if not logged_in:
                        print_error("Please login first")
                        continue
                    try:
                        amount = float(input(f"{Style.PROMPT}Amount to deposit: {Style.RESET}"))
                        if atm.deposit(amount):
                            print_success(f"Successfully deposited ${amount:,.2f}")
                        else:
                            print_error("Deposit failed")
                    except ValueError:
                        print_error("Invalid amount entered")

                case '4':
                    if not logged_in:
                        print_error("Please login first")
                        continue
                    try:
                        amount = float(input(f"{Style.PROMPT}Amount to withdraw: {Style.RESET}"))
                        if atm.withdraw(amount):
                            print_success(f"Successfully withdrew ${amount:,.2f}")
                        else:
                            print_error("Withdrawal failed. Insufficient funds or invalid amount.")
                    except ValueError:
                        print_error("Invalid amount entered")

                case '5':
                    if not logged_in:
                        print_error("Please login first")
                        continue
                    target = input(f"{Style.PROMPT}Target account number: {Style.RESET}").strip()
                    try:
                        amount = float(input(f"{Style.PROMPT}Amount to transfer: {Style.RESET}"))
                        if atm.transfer(target, amount):
                            print_success(f"Successfully transferred ${amount:,.2f} to {target}")
                        else:
                            print_error("Transfer failed. Check target account or balance.")
                    except ValueError:
                        print_error("Invalid amount entered")

                case '6':
                    if not logged_in:
                        print_error("Please login first")
                        continue
                    balance = atm.check_balance()
                    print_info(f"Current Balance: {Style.BOLD}${balance:,.2f}{Style.RESET}")

                case '7':
                    if not logged_in:
                        print_error("Please login first")
                        continue
                    info = atm.get_account_info()
                    print_info("Account Details:")
                    print(f"  • Account: {Style.BOLD}{info['account_number']}{Style.RESET}")
                    print(f"  • Owner:   {info['owner']}")
                    print(f"  • Balance: {Style.SUCCESS}${info['balance']:,.2f}{Style.RESET}")

                case '8':
                    if logged_in:
                        atm.logout()
                        print_success("Logged out successfully.")
                    else:
                        print_error("You are not logged in.")

                case '9':
                    clear_screen()
                    print_info("Switching banks...")
                    break

                case '10':
                    print_info("Thank you for using the Universal ATM System. Goodbye!")
                    return

                case _:
                    print_error("Invalid choice. Please select a number from the menu.")

if __name__ == "__main__":
    main()