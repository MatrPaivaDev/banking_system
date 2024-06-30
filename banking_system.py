import os

# Menu options displayed to the user
menu = """
[1] Deposit
[2] Withdraw
[3] Statement
[4] New User
[5] New Account
[6] List accounts
[7] EXIT
"""

# Global variables for managing account operations
total_balance = 0
withdrawals_made = 0
WITHDRAW_LIMIT = 1000.00
final_value = ''
users = []
BRANCH = '0001'
account_number = 0
accounts = []

# Function to validate CPF (Brazilian ID number)
def cpf_validator(cpf):
    entry_is_sequential = cpf == cpf[0] * len(cpf)

    if entry_is_sequential:
        return ('You sent sequential data.')

    nine_digits = cpf[:9]
    reverse_counter_1 = 10

    digit_1_result = 0
    for digit in nine_digits:
        digit_1_result += int(digit) * reverse_counter_1
        reverse_counter_1 -= 1
    digit_1 = (digit_1_result * 10) % 11
    digit_1 = digit_1 if digit_1 <= 9 else 0

    ten_digits = nine_digits + str(digit_1)
    reverse_counter_2 = 11

    digit_2_result = 0
    for digit in ten_digits:
        digit_2_result += int(digit) * reverse_counter_2
        reverse_counter_2 -= 1
    digit_2 = (digit_2_result * 10) % 11
    digit_2 = digit_2 if digit_2 <= 9 else 0

    calculated_cpf = f'{nine_digits}{digit_1}{digit_2}'

    if cpf == calculated_cpf:
        return True
    else:
        return None

# Function to withdraw money from an account
def withdraw(*, balance, value, statement, limit, withdrawals):
    global total_balance
    global final_value
    global withdrawals_made
    try:
        value_float = float(value)
    except ValueError:
        return 'Please provide a valid value!'
    if value_float > balance:
        withdrawals_made -= 1
        return ('Insufficient funds!\n'
                f'Your balance is R$ {balance:.2f}')
    elif value_float > limit:
        withdrawals_made -= 1
        return f'Your maximum withdrawal limit is R$ {limit:.2f}'
    elif withdrawals > 3:
        return (f'This is your {withdrawals}th withdrawal.\n'
                'You can only make 3 withdrawals per day!')
    total_balance = balance - value_float
    statement += f'Withdrawal (-): R$ {value_float:.2f}\n'
    final_value = statement
    return (f'You withdrew R$ {value_float:.2f}\n')

# Function to deposit money into an account
def deposit(balance, value, statement):
    global total_balance
    global final_value
    try:
        deposited_value = float(value)
    except ValueError:
        return 'Please provide a valid value!'
    total_balance = balance + deposited_value
    statement += f'Deposit (+): R$ {deposited_value:.2f}\n'
    final_value = statement
    return (f'You deposited R$ {deposited_value:.2f}\n')

# Function to display the final statement and balance
def end(balance, /, *, statement):
    global final_value
    global total_balance
    total_balance = balance
    final_value = statement
    os.system('clear')  # Clear the console screen
    return (f'####### Your statement: #######\n'
                     f'{statement}\n'
          f'Your final balance is: R${balance:.2f}\n'
           '############################')

# Function to create a new user
def create_user(user):
    cpf = input('Enter your CPF: ').replace('.', '').replace('-', '')
    if cpf_validator(cpf) is not True:
        return ('Invalid CPF!')
    user = filter_user(cpf, users)

    if user:
        return ("\n⚠️⚠️⚠️ There is already a user with this CPF! ⚠️⚠️⚠️")
        
    name = input('Enter your name: ')
    birth_date = input('Enter your date of birth (dd-mm-yyyy): ')
    address = input('Enter your address ' \
                     '(street, number - neighborhood - city/state code): ')
    
    users.append({"name": name, "birth_date": birth_date, \
                    "cpf": cpf, "address": address})
    return ('✅ User created successfully! ✅')

# Function to filter a user by CPF
def filter_user(cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None

# Function to create a new account associated with an existing user
def create_account(branch, account_number, user):
    cpf = input('Enter your CPF: ').replace('.', '').replace('-', '')
    user = filter_user(cpf, users)

    if user:
        print("🆕 Account created successfully! 🆕")
        return{'branch': branch, 'account_number': account_number, "user": user}
    return 'User not found!'
    
# Function to list all created accounts
def list_accounts(accounts):
    for account in accounts:
        line = (f'Branch: {account["branch"]}\n'
            f'A/C: {account["account_number"]}\n'
            f'Holder: {account["user"]["name"]}\n'
            '#######################################\n')
        print(line)

# Main program loop
while True:
    # Display the menu options and prompt user to choose an option
    option = input(f'{menu}\n'
                  'Choose one of the options: ')
    print()

    if option == '1':
        # Deposit operation selected
        deposited_value = input('Enter the amount you want to deposit: ')
        print(deposit(total_balance, deposited_value, final_value))

    elif option == '2':
        # Withdraw operation selected
        withdrawals_made += 1
        withdrawn_value = input('Enter the amount to withdraw: ')
        print(withdraw(balance=total_balance, value=withdrawn_value, statement=final_value,
                    limit=WITHDRAW_LIMIT, withdrawals=withdrawals_made))

    elif option == '3':
        # Statement operation selected
        os.system('clear')
        print(end(total_balance, statement=final_value))

    elif option == '4':
        # New user creation selected
        print(create_user(users))

    elif option == '5':
        # New account creation selected
        account_number += 1
        account = create_account(BRANCH, account_number, users)
        if account:
                accounts.append(account)

    elif option == '6':
        # List accounts selected
        if len(accounts) == 0 :
            print('There are no accounts to be listed')
            continue
        print(list_accounts(accounts))

    elif option == '7':
        # Exit the program
        break

    else:
        # Invalid option selected
        print('You did not choose any of the options!\n'
              'Please try again!')
