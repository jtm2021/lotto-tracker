import gspread, random
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
print("Please select from the menu using the corresponding number:\n")
print("""1 - Check Group Total Funds\n2 - Make a Bet\n3 - Input Lotto Win
4 - Check Last Numbers\n5 - Check Member Funds\n6 - Add Member Contribution
7 - Exit\n""")

def get_user_choice():
    """
    Get user choice from the welcome menu.
    """
    user_choice = int(input("Please enter your choice (from number 1-6): "))

    # make this a loop until the user inputs a correct choice
    if user_choice == 1:
        check_total_funds()
    elif user_choice == 2:
        get_random_number()
    elif user_choice == 3:
        calculate_winnings()
    elif user_choice == 4:
        check_last_numbers()
    elif user_choice == 5:
        pass
    elif user_choice == 6:
        get_contributions_data(),
        #update_contributions_worksheet(data)
    elif user_choice == 7:
        exit_program()
    else:
        print("Invalid Choice! Select a number from 1 to 7 only. Please try again.")


def calculate_winnings():
    """
    Get the value of winnings from the user and divide equally to all members
    """
    winning_value = int(input("Please enter the amount of winnings from the bet: "))
    member_share = winning_value // 8
    print(f"The group has won €{winning_value} and each member gets {member_share} each!")
    # print("Updating funds worksheet...")
    # add member_share to each individual and update funds sheet

def check_total_funds():
    """
    Check the total amount of money of all group members
    """    
    funds = SHEET.worksheet("funds").get_all_values()
    funds_last_row = funds[-1]
    print(int(funds_last_row))
    # can't get the sum of the last rows?


def check_member_funds():
    """
    Check each member's contributions and current total funds
    """
    #show total amount of contributions made
    #show current total funds in the game


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

 
def get_random_number():
    """
    Make a bet function using a quick pick random number generator
    """
    bet_numbers = random.sample(list(range(1,47)), 6)
    print(bet_numbers)
    numbers_worksheet = SHEET.worksheet("numbers")
    numbers_worksheet.append_row(bet_numbers)
    #only append this values when the user confirms usage of numbers
    #once, confirmation is made, print: numbers worksheet updated succesfully!


def check_last_numbers():
    """
    Checks the last numbers used in a bet by the group
    """
    numbers_used = SHEET.worksheet("numbers").get_all_values()
    numbers_last_row = numbers_used[-1]
    print(int(numbers_last_row))
    # should return list of ints not a list of str


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
            break

    return contributions_data


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


def update_contributions_worksheet(data):
    """
    Update the contributions worksheet, adding new row with the list data provided
    """
    print("Updating contributions worksheet...\n")
    contributions_worksheet = SHEET.worksheet("contributions")
    contributions_worksheet.append_row(data)
    print("Contributions worksheet updated succesfully.\nDo you want to make a bet for the next lotto draw?\n")


def exit_program():
    """
    Exits the whole program function
    """
    print("Thanks for checking in! Have a nice day! Goodbye...")

    
# data = get_contributions_data()
# contributions_data = [int(num) for num in data]
# update_contributions_worksheet(contributions_data)

get_user_choice()


