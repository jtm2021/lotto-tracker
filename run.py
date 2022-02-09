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
    print("Data should be eight numbers, separated by commas")
    print("Example: 5,10,3,2,6,5,5,2\n")

    data_str = input("Enter your data here: ")

get_contributions_data()