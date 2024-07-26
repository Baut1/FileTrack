# imports
import os

# tkinter
from tkinter import *

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# import dotenv
from dotenv import load_dotenv
load_dotenv('./constants.env')

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
SAMPLE_RANGE_NAME = os.environ.get('RANGE_NAME')

# intitialize data values
values = [[]]

creds = None

# connection to the API
def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  global creds
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
    
  except HttpError as err:
    print(err)


# actions
# show all rows
def show_all(root, values):
    for r in range(0, len(values)):
            for c in range(0, 7):
                cell = Entry(root, width=10)
                cell.grid(padx=5, pady=5, row=r+1, column=c)
                cell.insert(0, '{}'.format(values[r][c]))

# print row given its id
def print_by_id(values, id):
    for row in values:
        if row[0] == id:
            print(row)

# print all rows that match the client name
def print_filtered_by_client(values, client_name):
    result = filter(lambda row: client_name.lower() in row[1].lower(), values)
    print(list(result))

# print all rows that match the model name
def print_filtered_by_model(values, model_name):
    result = filter(lambda row: model_name.lower() in row[3].lower(), values)
    print(list(result))

# print all rows that match the date
def print_filtered_by_date(values, date):
    result = filter(lambda row: date in row[5], values)
    print(list(result))

# print most recent 10 rows
def print_filtered_by_date_last_ten(values):
    values.sort(key = lambda row: row[5], reverse=True)
    print(list(values[0:10]))

# find the row index ("range") given an id
def find_row_index(sheet_values, column_index, target_value):
    try: 
        for i, row in enumerate(sheet_values):
            print(row[column_index])
            if len(row) > column_index and row[column_index] == str(target_value):
                return i + 2  # Sheets API uses 1-based indices
        return None
    except TypeError as err:
        print(err)

# update row chosen by its id
def update_by_id(sheet_values, target_id):
    column_name = 'id'
    new_value = 'New Value'
    # Find the row index based on the 'id' column
    # column_index = sheet_values[0].index(column_name) if sheet_values and column_name in sheet_values[0] else None
    column_index = 0
    row_index = find_row_index(sheet_values, column_index, target_id)

    if row_index is not None:
        try:
            service = build("sheets", "v4", credentials=creds)
            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                        range=f'Turnos!G{row_index}',
                        valueInputOption='RAW',
                        body={'values': [[new_value]]})
            )
            # Execute the request
            response = result.execute()
            # Print the updated range and values
            print(f"Updated range: {response['updatedRange']}")
            
        except HttpError as err:
            print(err)
    else:
        print(f"Row with '{column_name}' = '{target_id}' not found.")

# add new row to the table
def add(sheet_values):
    index_to_extract = 0
    ids_array = [int(sub_array[index_to_extract]) for sub_array in sheet_values] # get array of ids
    new_row_values = [max(ids_array) + 1, 'Ana', 'agonzalez@gmail.com', 'Samsung S23', 'Boton roto', '2024-02-01', 'asd']
    
    try:
            service = build("sheets", "v4", credentials=creds)
            # Call the Sheets API
            sheet = service.spreadsheets()
            append_request = (
                sheet.values()
                .append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                        range=f'Turnos!A1',
                        valueInputOption='USER_ENTERED',
                        body={'values': [new_row_values]})
            )
            # Execute the request
            response = append_request.execute()
            # Print the updated range and values
            print(f"Appended range: {response['updates']['updatedRange']}")
            
    except HttpError as err:
        print(err)

class MyMainPanel:
    def __init__(self, root, frame) -> None:
        root = root
        frame = frame

        # btnFindById = Button(root, text="Ver todos", command=lambda:show_all(root, values)).grid(row=9, column=0)
        btnFindById = Button(root, text="Ver todos", command=lambda:update_by_id(values, 3)).grid(row=9, column=0)
        Label(root, text="ID").grid(row=0, column=0)
        Label(root, text="Nombre").grid(row=0, column=1)
        Label(root, text="email").grid(row=0, column=2)
        Label(root, text="articulo").grid(row=0, column=3)
        Label(root, text="detalle").grid(row=0, column=4)
        Label(root, text="fecha").grid(row=0, column=5)
        Label(root, text="comentario").grid(row=0, column=6)

if __name__ == "__main__":
  main()