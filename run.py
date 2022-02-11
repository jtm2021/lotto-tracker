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
7 - Exit\n""")
    try:
        user_choice = int(input("Please enter your choice (from number 1-7): "))
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
            exit_program()
    except ValueError:
            print("\nInvalid Choice! Select a number from 1 to 7 only. Please try again.")
            get_user_choice()


def check_total_funds():
    """
    Check the total amount of money of all group members
    """
    print("\nCalculating the group's total funds...\n")
    funds = SHEET.worksheet("funds").get_all_values()
    funds_first_row = funds[1]
    total_funds = sum([int(i) for i in funds_first_row])
    print(f"Total Funds: €{total_funds}")
    check_main_menu()


def get_lucky_numbers():
    """
    Get lucky numbers using a random number generator
    """
    lucky_numbers = random.sample(list(range(1, 47)), 6)
    print(f"\nHere's the lucky numbers for today: {lucky_numbers}")
    print("Feel free to copy these numbers, who knows? you might get the jackpot! :)\n")
    numbers_worksheet = SHEET.worksheet("numbers")
    numbers_worksheet.append_row(lucky_numbers)
    check_main_menu()


def calculate_winnings():
    """
    Get the value of winnings from the user and divide equally to all members
    """
    winning_value = int(input("\nPlease enter the amount of winnings again: "))
    member_share = winning_value // 8
    print(f"\nThe group has won €{winning_value}\n")
    print("Calculating dividends for each member...")
    print(f"Each member gets {member_share} each!\n")
    fundsheets = SHEET.worksheet("funds")
    fundsheets.append_row([member_share]*8)
    print("Updating funds worksheet...\n")
    print("Funds worksheet succesfully updated!\n")
    check_main_menu()


def input_win():
    """
    Ask user to input amount of winnings and verify if the user is sure of the amount
    """
    Winning_amount = input(f"Enter the amount of the winnings: \n")
    sure_answer = input("Enter yes if you are sure: ")
    if sure_answer.lower() == "yes":
        calculate_winnings()
    else:
        print(f"Try again!")
        input_win()


def check_last_numbers():
    """
    Check the last lucky numbers used in a bet by the group
    """
    numbers_used = SHEET.worksheet("numbers").get_all_values()
    numbers_last_row = numbers_used[-1]
    last_lucky_number = [int(i) for i in numbers_last_row]
    print(f"\nThe last lucky numbers are {last_lucky_number}:)\n")
    check_main_menu()


def show_member_funds():
    print("Here are the current funds of each member:")
    funds = SHEET.worksheet("funds").get_all_values()
    for i in range(len(funds[0])):
        print(f"{funds[0][i]}: €{funds[1][i]}")
    check_main_menu()


def calculate_total_funds():
    """
    Get the last row of funds data worksheet
    """
    contributions = SHEET.worksheet("contributions").get_all_values()
    contributions_last_row = contributions[-1]
    funds = SHEET.worksheet("winnings").get_all_values()
    funds_last_row = funds[-1]

    total_funds = []
    for contributions, funds in zip(contributions_last_row, funds_last_row):
        funds = int(contributions) + int(funds)
        total_funds.append(funds)
    fundsheets = SHEET.worksheet("funds")
    fundsheets.append_row(total_funds)
    overall_balance = sum(total_funds)
    print(f"The group has {overall_balance}euros in total!")


def check_main_menu():
    """
    Ask user to go back to main menu or exit
    """
    mx_choice = input(f"Enter yes to go back to main menu or no to exit program: \n")
    if mx_choice.lower() == "yes":
        get_user_choice()
    elif mx_choice.lower() == "no":
        exit_program()
    else:
        print(f"Invalid answer! Try again.")
        check_main_menu()
    # change name of variable


def get_contributions_data():
    """
    Get contributions from each player for the lotto draw.
    """
    while True:
        print("Please enter contributions data for each player!")
        print("Data should be eight numbers, separated by commas.")
        print("Example: 5,10,3,2,6,5,5,2\n")
    
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
        [int(value) for value in values]
        if len(values) != 8:
            raise ValueError(
                f"8 values required! you provided {len(values)}"
            )
    except ValueError:
        print(f"Invalid data! Please try again.\n")
        return False

    return True


def update_contributions_worksheet(my_list):#rename variable
    """
    Update the contributions worksheet, adding new row with the list data
    provided
    """
    print("Updating contributions worksheet...\n")
    contributions_worksheet = SHEET.worksheet("contributions")
    contributions_worksheet.append_row(my_list)#rename variable
    print("Contributions worksheet updated succesfully\n")
    check_main_menu()
    
    


def exit_program():
    """
    Exits the whole program function
    """
    print("Thanks for checking in! Have a nice day! Goodbye...")


get_user_choice()