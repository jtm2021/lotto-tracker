import gspread
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
print("1- Check Group Total Funds\n2- Make a Bet\n3- Input Lotto Win\n4- Check Last Numbers\n5- Check Member Funds\n6- Add Member Contribution\n")

def get_user_choice():
    """
    Get user choice from the welcome menu.
    """
    user_choice = input("Please enter your choice (from number 1-6): ")

    if user_choice == input(1):
        get_contributions_data()



def get_contributions_data():
    """
    Get contributions from each player for the lotto draw.
    """
    while True:
        print("Please enter contributions data for each player!")
        print("Data should be eight numbers, separated by commas.")
        print("Example: 5,10,3,2,6,5,5,2\n")
    
        data_str = input("Enter your data here: ")
    
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

    decision = input('Enter "yes" if you want to make the bet: ')

    get_funds_data()


def get_funds_data():
    """
    Get the last row of funds data worksheet
    """
    contributions = SHEET.worksheet("contributions").get_all_values()
    contributions_last_row = contributions[-1]
    funds = SHEET.worksheet("funds").get_all_values()
    funds_last_row = funds[-1]

    total_funds = []
    for contributions, funds in zip(contributions_last_row, funds_last_row):
        funds = int(contributions) + int(funds)
        total_funds.append(funds)

    return total_funds

# data = get_contributions_data()
# contributions_data = [int(num) for num in data]
# update_contributions_worksheet(contributions_data)

get_user_choice()