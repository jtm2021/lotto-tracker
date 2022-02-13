import gspread
import random
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('lotto_tracker')

print("Welcome to Lotto Tracker Data Automation!")


def get_user_choice():
    """
    Get user choice from the welcome menu.
    """
    print("\nPlease select from the menu using the corresponding number:\n")
    print("""1 - Check Group Total Funds\n2 - Lucky Numbers\n3 - Input Lotto Win
4 - Check Last Numbers\n5 - Check Member Funds\n6 - Add Member Contribution
7 - Withdraw Money for A Member\n8 - Exit\n""")
    try:
        user_choice = int(input("Please enter your choice (from no. 1-8):\n"))
        if user_choice == 1:
            check_total_funds()
        elif user_choice == 2:
            get_lucky_numbers()
        elif user_choice == 3:
            input_win()
        elif user_choice == 4:
            check_last_numbers()
        elif user_choice == 5:
            show_member_funds()
        elif user_choice == 6:
            get_contributions_data()
        elif user_choice == 7:
            who_wants_withdrawal()
        elif user_choice == 8:
            exit_program()
        elif user_choice < 1 or user_choice > 8:
            print("\nInvalid Choice! Please try again.")
            get_user_choice()
    except ValueError:
        print("\nInvalid Choice! Please try again.")
        get_user_choice()


def check_total_funds():
    """
    Check the total amount of money of all group members
    """
    print("\nCalculating the group's total funds...\n")
    funds = SHEET.worksheet("funds").get_all_values()
    funds_first_row = funds[1]
    total_funds = sum([float(i) for i in funds_first_row])
    total_funds_float = "{:.2f}".format(total_funds)
    print(f"Total Funds: €{total_funds_float}")
    check_main_menu()


def get_lucky_numbers():
    """
    Get lucky numbers using a random number generator
    """
    lucky_numbers = random.sample(list(range(1, 47)), 6)
    print(f"\nHere's the lucky numbers for you today: {lucky_numbers}")
    print("Feel free to copy these numbers, you might win the jackpot! :)")
    numbers_worksheet = SHEET.worksheet("numbers")
    numbers_worksheet.append_row(lucky_numbers)
    check_main_menu()


def calculate_winnings():
    """
    Get the value of winnings from the user and divide equally to all members
    """
    winning_value = float(input("\nRe-enter amount to confirm: \n"))
    total_win = "{:.2f}".format(winning_value)
    member_share = float(winning_value / 8)
    member_share_float = "{:.2f}".format(member_share)
    print(f"\nCongratulations! Your group has won €{total_win}\n")
    print("Calculating dividends for each member...")
    print(f"Each member gets €{member_share_float} each!\n")
    fundsheets = SHEET.worksheet("funds")
    fundsheets.append_row([member_share]*8)
    print("Updating funds worksheet...\n")
    print("Funds worksheet successfully updated!\n")
    check_main_menu()


def input_win():
    """
    Ask user to input amount of winnings and verify if the
    user is sure of the amount.
    """
    while True:
        try:
            float(input("Enter the amount of the winnings: \n"))
            calculate_winnings()
            break
        except ValueError:
            print("That's not a valid option!")


def check_last_numbers():
    """
    Check the last lucky numbers used in a bet by the group
    """
    numbers_used = SHEET.worksheet("numbers").get_all_values()
    numbers_last_row = numbers_used[-1]
    last_lucky_number = [int(i) for i in numbers_last_row]
    print(f"\nThe last lucky numbers are {last_lucky_number}\n")
    check_main_menu()


def show_member_funds():
    """
    Retrieve data for each member's available funds
    """
    print("\nHere are the current funds of each member:")
    funds = SHEET.worksheet("funds").get_all_values()
    for i in range(len(funds[0])):
        print(f"{funds[0][i]}: €{funds[1][i]}")
    check_main_menu()


def get_contributions_data():
    """
    Get contributions from each player for the lotto draw.
    """
    while True:
        print("\nPlease enter contributions data for each player!")
        print("Data should be eight numbers, separated by commas.")
        print("Contributions must be added in alphabetical order.")
        print("Example: Ann, Ben, Carl, Dean, Emma, Fiona, Greg, Harry")
        print("Example: 5,10,0,2,6,5,5,2\n")
        data_str = input("Enter your data here:\n")
        contributions_data = data_str.split(",")
        if validate_data(contributions_data):
            print("Data is valid!")
            update_contributions_worksheet(contributions_data)
            break


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into integers,
    or if the input isn't exactly 8 values.
    """
    try:
        values = [int(value) for value in values]
        if len(values) != 8:
            raise ValueError(
                f"8 values required! you provided {len(values)}"
            )
    except ValueError:
        print("\nInvalid data! Please try again.\n")
        return False

    return True


def update_contributions_worksheet(new_contribution):
    """
    Update the contributions worksheet, adding new row with the list data
    provided
    """
    print("Updating contributions worksheet...\n")
    contributions_worksheet = SHEET.worksheet("contributions")
    contributions_worksheet.append_row(new_contribution)
    funds_worksheet = SHEET.worksheet("funds")
    funds_worksheet.append_row(new_contribution)
    print("Contributions and Funds worksheet updated successfully.\n")
    check_main_menu()


def who_wants_withdrawal():
    """
    Ask the user who wants to withdraw money
    """
    global user_withdraw_choice
    SHEET.worksheet("funds").get_all_values()
    print("\nWho wants to withdraw money?")
    print("""1 - Ann\n2 - Ben\n3 - Carl\n4 - Dean\n5 - Emma\n6 - Fiona
7 - Greg\n8 - Harry""")
    try:
        user_withdraw_choice = int(input("""\nSelect from the corresponding
numbers above:\n"""))
        if user_withdraw_choice == 1:
            print("\nWithdraw money for Ann?\n")
            confirm_withdraw_choice()
        elif user_withdraw_choice == 2:
            print("\nWithdraw money for Ben?\n")
            confirm_withdraw_choice()
        elif user_withdraw_choice == 3:
            print("\nWithdraw money for Carl?\n")
            confirm_withdraw_choice()
        elif user_withdraw_choice == 4:
            print("\nWithdraw money for Dean?\n")
            confirm_withdraw_choice()
        elif user_withdraw_choice == 5:
            print("\nWithdraw money for Emma?\n")
            confirm_withdraw_choice()
        elif user_withdraw_choice == 6:
            print("\nWithdraw money for Fiona?\n")
            confirm_withdraw_choice()
        elif user_withdraw_choice == 7:
            print("\nWithdraw money for Greg?\n")
            confirm_withdraw_choice()
        elif user_withdraw_choice == 8:
            print("Withdraw money for Harry?\n")
            confirm_withdraw_choice()
        elif user_withdraw_choice < 1 or user_withdraw_choice > 8:
            print("\nInvalid Choice! Please try again.")
            who_wants_withdrawal()
    except ValueError:
        print("\nInvalid Choice! Please try again.")
        who_wants_withdrawal()


def confirm_withdraw_choice():
    """
    Ask user to confirm withdrawal for a certain member
    """
    withdraw_choice = input("Confirm to proceed! (yes/no): \n")
    if withdraw_choice.lower() == "yes":
        withdraw_money(user_withdraw_choice)
    elif withdraw_choice.lower() == "no":
        check_main_menu()
    else:
        print("\nInvalid answer! Try again.")
        confirm_withdraw_choice()


def withdraw_money(user_withdraw_choice):
    """
    Withdraw money for a group member
    """
    fnd_sheet = SHEET.worksheet("funds")
    withdraw = float(input("\nEnter amount of money to withdraw: "))
    if user_withdraw_choice == 1:
        if withdraw <= float(fnd_sheet.cell(col=1, row=2).value):
            withdraw_list = [-withdraw] + [0] * 7
            fnd_sheet.append_row(withdraw_list)
        else:
            print("Sorry! You exceeded the available funds for withdrawal!")
            print(f"Limit: €{float(fnd_sheet.cell(col=1, row=2).value)}")
            withdraw_money(user_withdraw_choice)
    elif user_withdraw_choice == 2:
        if withdraw <= float(fnd_sheet.cell(col=2, row=2).value):
            withdraw_list = [0] + [-withdraw] + [0] * 6
            fnd_sheet.append_row(withdraw_list)
        else:
            print("Sorry! You exceeded the available funds for withdrawal!")
            print(f"Limit: €{float(fnd_sheet.cell(col=2, row=2).value)}")
            withdraw_money(user_withdraw_choice)
    elif user_withdraw_choice == 3:
        if withdraw <= float(fnd_sheet.cell(col=3, row=2).value):
            withdraw_list = [0] * 2 + [-withdraw] + [0] * 5
            fnd_sheet.append_row(withdraw_list)
        else:
            print("Sorry! You exceeded the available funds for withdrawal!")
            print(f"Limit: €{float(fnd_sheet.cell(col=3, row=2).value)}")
            withdraw_money(user_withdraw_choice)
    elif user_withdraw_choice == 4:
        if withdraw <= float(fnd_sheet.cell(col=4, row=2).value):
            withdraw_list = [0] * 3 + [-withdraw] + [0] * 4
            fnd_sheet.append_row(withdraw_list)
        else:
            print("Sorry! You exceeded the available funds for withdrawal!")
            print(f"Limit: €{float(fnd_sheet.cell(col=4, row=2).value)}")
            withdraw_money(user_withdraw_choice)
    elif user_withdraw_choice == 5:
        if withdraw <= float(fnd_sheet.cell(col=5, row=2).value):
            withdraw_list = [0] * 4 + [-withdraw] + [0] * 3
            fnd_sheet.append_row(withdraw_list)
        else:
            print("Sorry! You exceeded the available funds for withdrawal!")
            print(f"Limit: €{float(fnd_sheet.cell(col=5, row=2).value)}")
            withdraw_money(user_withdraw_choice)
    elif user_withdraw_choice == 6:
        if withdraw <= float(fnd_sheet.cell(col=6, row=2).value):
            withdraw_list = [0] * 5 + [-withdraw] + [0] * 2
            fnd_sheet.append_row(withdraw_list)
        else:
            print("Sorry! You exceeded the available funds for withdrawal!")
            print(f"Limit: €{float(fnd_sheet.cell(col=6, row=2).value)}")
            withdraw_money(user_withdraw_choice)
    elif user_withdraw_choice == 7:
        if withdraw <= float(fnd_sheet.cell(col=7, row=2).value):
            withdraw_list = [0] * 6 + [-withdraw] + [0]
            fnd_sheet.append_row(withdraw_list)
        else:
            print("Sorry! You exceeded the available funds for withdrawal!")
            print(f"Limit: €{float(fnd_sheet.cell(col=7, row=2).value)}")
            withdraw_money(user_withdraw_choice)
    elif user_withdraw_choice == 8:
        if withdraw <= float(fnd_sheet.cell(col=8, row=2).value):
            withdraw_list = [0] * 7 + [-withdraw]
            fnd_sheet.append_row(withdraw_list)
        else:
            print("Sorry! You exceeded the available funds for withdrawal!")
            print(f"Limit: €{float(fnd_sheet.cell(col=8, row=2).value)}")
            withdraw_money(user_withdraw_choice)
    print("\nWithdrawal done! Updating funds worksheet...\n")
    print("Current funds are up-to-date!.\n")
    check_main_menu()


def check_main_menu():
    """
    Ask user to go back to main menu or exit
    """
    menu_exit_choice = input("\nDo you need anything else? (yes/no): \n")
    if menu_exit_choice.lower() == "yes":
        get_user_choice()
    elif menu_exit_choice.lower() == "no":
        exit_program()
    else:
        print("Invalid answer! Try again.")
        check_main_menu()


def exit_program():
    """
    Exits the whole program function
    """
    print("Thanks for checking in! Have a nice day! Goodbye...")


user_withdraw_choice = 0
get_user_choice()
