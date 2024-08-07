# imports
import os

# tkinter
from tkinter import *
# ttkbootstrap
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

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

class MyMainPanel:
    def __init__(self, root, frame) -> None:
        self.root = root
        frame = frame

        # frame for the cells to be filled with the data
        self.widgets = []
        self.cells_frame = Frame(root)

        # search input
        searchEntry = ttk.Entry(root, width=10)
        searchEntry.grid(row=1, column=0)

        # list of texts for the labels
        label_texts = ["ID", "Cliente", "Modelo", "Fecha", "Problema", "Email", "Comentario"]
        # create and place labels
        for i, text in enumerate(label_texts):
            label = ttk.Label(root, text=text)
            label.grid(row=2, column=i, padx=10, pady=5)  # Arrange labels in a grid

        # action buttons
        # search by id
        ttk.Button(root,
                   text="Buscar por ID",
                   bootstyle=PRIMARY,
                   cursor="hand2",
                   command=lambda:self.show_by_id(root,
                                                  values,
                                                  searchEntry.get())
                    ).grid(row=0,
                        column=0,
                        padx=1, pady=1)
        # search by clientname
        ttk.Button(root,
                        text="Buscar por cliente",
                        bootstyle=PRIMARY,
                        cursor="hand2",
                        command=lambda:self.show_filtered_by_client(root,
                                                                values,
                                                                searchEntry.get())
                        ).grid(row=0,
                            column=1,
                            padx=1, pady=1)
        # search by model name
        ttk.Button(root,
                    text="Buscar por modelo",
                    bootstyle=PRIMARY,
                    cursor="hand2",
                    command=lambda:self.show_filtered_by_model(root,
                                                            values,
                                                            searchEntry.get())
                    ).grid(row=0,
                        column=2,
                        padx=1, pady=1)
        # search by date
        ttk.Button(root,
                    text="Buscar por fecha",
                    bootstyle=PRIMARY,
                    cursor="hand2",
                    command=lambda:self.show_filtered_by_date(root,
                                                            values,
                                                            searchEntry.get())
                    ).grid(row=0,
                        column=3,
                        padx=1, pady=1)
        # search last 10
        ttk.Button(root,
                    text="Buscar ultimos",
                    bootstyle=PRIMARY,
                    cursor="hand2",
                    command=lambda:self.show_filtered_by_date_last_ten(root,
                                                                    values)
                    ).grid(row=0,
                        column=4,
                        padx=1, pady=1)
        # retrieve all
        ttk.Button(root,
                    text="Ver todos",
                    bootstyle=PRIMARY,
                    cursor="hand2",
                    command=lambda:self.show_all(root,
                                                    values)
                    ).grid(row=0,
                            column=5,
                            padx=1, pady=1)
        # create new
        ttk.Button(root,
                    text="Crear",
                    bootstyle=SUCCESS,
                    cursor="hand2",
                    command=lambda:self.open_new_window()
                    ).grid(row=0,
                            column=6,
                                padx=1, pady=1)

    # actions
    # shows grid when given values, called by other filtering and sorting functions
    def show_grid(self, root, listValues):
        # clear existing grid
        self.clear_cells()
        
        # loop through the whole list
        for r in range(0, len(listValues)):
            row_id = listValues[r][0]
            id_label = ttk.Label(root, text=listValues[r][0])
            id_label.grid(row=r+3, column=0, padx=10, pady=5)
            self.widgets.append(id_label)

            # initialize entries
            entries = []
            # loop inside the row for every value
            for c in range(1, 7):
                cell = Entry(root, width=10)
                cell.grid(padx=5, pady=5, row=r+3, column=c)
                cell.insert(0, '{}'.format(listValues[r][c]))
                self.widgets.append(cell)
                entries.append(cell)
            
            # get entries and try to update_by_id()
            def get_updated_entries(entries, row_id):
                updated_values = [entry.get() for entry in entries]
                self.update_by_id(values, row_id, updated_values)
            
            # edit button
            edit_button = ttk.Button(root,
                text="Editar",
                bootstyle="primary",
                cursor="hand2",
                command=lambda entries=entries, row_id=row_id: get_updated_entries(entries, row_id)
                )
            edit_button.grid(row=r+3, column=8,
                        padx=1, pady=1)
            self.widgets.append(edit_button)
            # delete button
            delete_button = ttk.Button(root,
                text="Eliminar",
                bootstyle="danger",
                cursor="hand2",
                command=lambda row_id=row_id: self.delete_by_id(values, row_id))
            delete_button.grid(row=r+3, column=9)
            self.widgets.append(delete_button)

    def filterBy(self, values, searchValue, rowIndex):
        resultFilter = filter(lambda row: searchValue.lower() in row[rowIndex].lower(), values)
        resultList = list(resultFilter)
        return resultList

    def clear_cells(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []

    # show all rows
    def show_all(self, root, values):
        self.show_grid(root, values)

    # show row given its id
    def show_by_id(self, root, values, id):
        for row in values:
            if row[0] == id:
                self.show_grid(root, [row])

    # show all rows that match the client name
    def show_filtered_by_client(self, root, values, client_name):
        resultsList = self.filterBy(values, client_name, 1)
        self.show_grid(root, resultsList)

    # show all rows that match the model name
    def show_filtered_by_model(self, root, values, model_name):
        resultsList = self.filterBy(values, model_name, 2)
        self.show_grid(root, resultsList)

    # show all rows that match the date
    def show_filtered_by_date(self, root, values, date):
        resultsList = self.filterBy(values, date, 3)
        self.show_grid(root, resultsList)

    # show most recent 10 rows
    def show_filtered_by_date_last_ten(self, root, values):
        arrays_sorted = sorted(values, key=lambda x: x[3], reverse=True)
        resultsList = arrays_sorted[:3]
        self.show_grid(root, resultsList)

    # find the row index ("range") given an id
    def find_row_index(self, sheet_values, column_index, target_value):
        try: 
            for i, row in enumerate(sheet_values):
                if len(row) > column_index and row[column_index] == str(target_value):
                    return i + 2  # Sheets API uses 1-based indices
            return None
        except TypeError as err:
            print(err)

    # update row chosen by its id
    def update_by_id(self, sheet_values, target_id, updated_values):
        column_name = 'id'
        # Find the row index based on the 'id' column
        # column_index = sheet_values[0].index(column_name) if sheet_values and column_name in sheet_values[0] else None
        column_index = 0
        row_index = self.find_row_index(sheet_values, column_index, target_id)

        body = {
            'values': [updated_values]
        }

        if row_index is not None:
            try:
                service = build("sheets", "v4", credentials=creds)
                # Call the Sheets API
                sheet = service.spreadsheets()
                result = (
                    sheet.values()
                    .update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=f'Turnos!B{row_index}:G{row_index}',
                            valueInputOption='USER_ENTERED',
                            body=body)
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
    def add(self, sheet_values, entry_values):
            index_to_extract = 0
            ids_array = [int(sub_array[index_to_extract]) for sub_array in sheet_values] # get array of ids
            new_row_values = [max(ids_array) + 1] + entry_values
            
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

    def delete_by_id(self, sheet_values, target_id):
        # Find the row index based on the 'id' column
        column_index = 0
        row_index = self.find_row_index(sheet_values, column_index, target_id) - 1

        request_body = {
            'requests': [
                {
                    'deleteDimension': {
                        'range': {
                            'sheetId': 0,  # The sheet ID; default is the first sheet
                            'dimension': 'ROWS',
                            'startIndex': row_index, # Inclusive
                            'endIndex': row_index + 1 # Exclusive
                        }
                    }
                }
            ]
        }

        if row_index is not None:
            try:
                service = build("sheets", "v4", credentials=creds)
                # Call the Sheets API
                response = service.spreadsheets().batchUpdate(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID,
                    body=request_body
                ).execute()
                print(f"Row {row_index + 1} deleted.")
                
            except HttpError as err:
                print(err)
        else:
            print(f"Row with 'ID' = '{target_id}' not found.")
    
    # message dialog check if user is sure
    # if user selects OK
    def on_ok(self, values, entry_values):
        self.add(values, entry_values)
    # dialog
    def ask_ok_cancel(self, values, entry_values):
        response = Messagebox.okcancel("Se creará un nuevo expediente", "¿Quieres continuar?")
        if response == "OK":
            self.on_ok(values, entry_values)

    # new window to add new items to db
    def open_new_window(self):
        new_window = ttk.Toplevel(self.root)
        new_window.title("Crear un nuevo expediente")

        # inicializar entries
        entries = []

        # list of texts for the labels
        label_texts = ["Cliente", "Modelo", "Fecha", "Problema", "Email", "Comentario"]
        # create and place labels
        for i, text in enumerate(label_texts):
            label = ttk.Label(new_window, text=text)
            label.grid(row=0, column=i, padx=10, pady=5)  # Arrange labels in a grid

        # entry cells
        for c in range(0, 6):
            cell = Entry(new_window, width=10)
            cell.grid(padx=5, pady=5, row=1, column=c)
            entries.append(cell)
        # get entries and try to add()
        def get_new_window_entries():
            entry_values = [entry.get() for entry in entries]
            self.ask_ok_cancel(values, entry_values)

        # buttons to confirm or cancel
        ttk.Button(new_window,
                    text="Crear",
                    bootstyle=SUCCESS,
                    cursor="hand2",
                    command=lambda:get_new_window_entries()
                    ).grid(row=2,
                           column=4,
                           padx=10,
                           pady=10)
        
        ttk.Button(new_window,
                   text="Cerrar",
                   bootstyle="danger",
                   command=new_window.destroy
                   ).grid(row=2, column=5, padx=10, pady=10)

if __name__ == "__main__":
  main()