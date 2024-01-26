import os

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
SAMPLE_RANGE_NAME = "Turnos!A1:G10"

creds = None

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


# actions
def print_all(values):
    for row in values:
        print(row)

def print_by_id(values, id):
    for row in values:
        if row[0] == id:
            print(row)

def print_filtered_by_client(values, client_name):
    result = filter(lambda row: client_name.lower() in row[1].lower(), values)
    print(list(result))

def print_filtered_by_model(values, model_name):
    result = filter(lambda row: model_name.lower() in row[3].lower(), values)
    print(list(result))

def print_filtered_by_date(values, date):
    result = filter(lambda row: date in row[5], values)
    print(list(result))

def print_filtered_by_date_last_ten(values):
    values.sort(key = lambda row: row[5], reverse=True)
    print(list(values[0:10]))

def find_row_index(sheet_values, column_index, target_value):
    for i, row in enumerate(sheet_values):
        if len(row) > column_index and row[column_index] == str(target_value):
            return i + 1  # Sheets API uses 1-based indices
    return None

def update_by_id(sheet_values, target_id):

    column_name = 'id'
    new_value = 'New Value'

    # Find the row index based on the 'id' column
    column_index = sheet_values[0].index(column_name) if sheet_values and column_name in sheet_values[0] else None
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