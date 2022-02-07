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
    Get funds input from the user which corresponds to each player's contribution
    """
    print("Please enter contributions data for each player.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 5, 10, 3, 20, 0, 8\n")

    contribution = input("Enter your data here please: ")
    print(f"The data provided is {contribution}")

get_funds_data()
