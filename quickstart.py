# imports
import os
from tkinter import *
# import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# import dotenv
from dotenv import load_dotenv
load_dotenv('./constants.env')

# import functions/methods
from actions import *

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
SAMPLE_RANGE_NAME = "Turnos!A2:G20"

# initialize data values
values = [[]]


def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    global values
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    # print all rows
    # print_all(values)

    # print specific row
    # print_by_id(values, '3')

    # print_filtered_by_client(values, 'juan')

    # print_filtered_by_model(values, 'iPhone 15')

    # print_filtered_by_date(values, '2024-01-15')

    # print_filtered_by_date_last_ten(values)

    # edit specific row
    # update_by_id(values, 2)

    # add(values)
    
  except HttpError as err:
    print(err)

# interfaz grafica
root = Tk()
root.title("Archivos")
root.geometry("800x500")
btnFindById = Button(root, text="Find by id", width=20, command=lambda:printall(values)).grid(row=5, column=0)

def printall(values):
  for r in range(0, 3):
    for c in range(0, 7):
        cell = Entry(root, width=10)
        cell.grid(padx=5, pady=5, row=r, column=c)
        cell.insert(0, '{}'.format(values[r][c]))



if __name__ == "__main__":
  main()
  
root.mainloop()