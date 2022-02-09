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

print("Welcome to Lotto Tracker Data Automation!\n")

def get_contributions_data():
    """
    Get contributions from each player for the lotto draw.
    """
    print("Please enter contributions data for each player!")
    print("Data should be eight numbers, separated by commas.")
    print("Example: 5,10,3,2,6,5,5,2\n")

    data_str = input("Enter your data here: ")

    contributions_data = data_str.split(",")
    validate_data(contributions_data)

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into integers,
    or if the input isn't exactly 8 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"8 values required! you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")

get_contributions_data()