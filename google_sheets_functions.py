from typing import List
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class Google_sheets_api():
 
    def __init__(
        self, path_to_json: str, api_name: str = "sheets", api_version: str = "v4",
        scopes: List[str] = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive'] 
        ) -> None:
    
        credentials = ServiceAccountCredentials.from_json_keyfile_name(path_to_json, scopes=scopes)
    
        # Build the service object.
        self._service = build(api_name, api_version, credentials=credentials)
    
    def get_value_from_google_sheets(self, spreadsheet_id: str, range_to_sheet: str)-> dict:
        return self._service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_to_sheet).execute()
        
    def append_to_google_sheets(self, spreadsheet_id: str, values: list, range_to_sheet: str ,format="ROWS")-> dict:
        return self._service.spreadsheets().values().append(spreadsheetId = spreadsheet_id,
        range = range_to_sheet,
        valueInputOption = "USER_ENTERED",
        body = {
            "majorDimension": format,     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
            "values": values}
        ).execute()