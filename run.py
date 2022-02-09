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

def get_funds_data():
    """
    Get funds input from the user to correspond each player's contribution
    """
    while True: 
        print("Please enter contribution of each player.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 5, 10, 3, 20, 0, 8\n")

        contribution_str = input("Please enter your data here: ")
        
        funds_data = contribution_str.split(",")
        

        if validate_data(funds_data):
            print("Data is valid")
            break


def validate_data(values):
    """
    Converts all the string values into integers. 
    It will raise an error if the strings are not converted into integers,
    or if they are not exactly 6 values.
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"6 values required! you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


get_funds_data()
