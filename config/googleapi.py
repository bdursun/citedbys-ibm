from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os


class GoogleAPIClient:
    def __init__(self, credentials_file="config/credentials.json", token_file="token.json"):
        self.scopes = ["https://www.googleapis.com/auth/drive"]
        self.credentials_file = credentials_file
        self.token_file = token_file

    def authenticate(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(
                self.token_file, self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())
        return creds


class GoogleServices:
    def __init__(self, creds):
        self.drive_service = build('drive', 'v3', credentials=creds)
        self.sheets_service = build('sheets', 'v4', credentials=creds)

    def create_sheet_copy(self, tempname, newname, email):
        response = self.drive_service.files().list(q=f"name='{tempname}'").execute()
        template_file_id = response.get('files', [])[0].get('id')
        folder_client = self.drive_service.files().list(q="name='ClientData'").execute().get('files', [])
        folder_metadata = {
            'name': newname,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents':  [folder_client[0]['id']]
        }
        new_folder = self.drive_service.files().create(body=folder_metadata, fields='id').execute()
        new_folder_id = new_folder.get('id')
        copy_metadata = {'name': newname,
                         'parents': [new_folder_id]}
        copy_response = self.drive_service.files().copy(fileId=template_file_id, body=copy_metadata).execute()
        copy_file_id = copy_response.get('id')
        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': email
        }
        # use fileId=new_folder_id for giving permission to parent folder
        self.drive_service.permissions().create(
            fileId=copy_file_id,
            body=permission,
            fields='id'
        ).execute()
        link = self.drive_service.files().get(fileId=copy_file_id, fields='webViewLink').execute()
        print("link: ", link)
        return link

        # Rename the copied file
        # self.sheets_service.spreadsheets().batchUpdate(spreadsheetId=copy_file_id, body={'requests': [
        #     {'updateSpreadsheetProperties': {'properties': {'title': newname}, 'fields': 'title'}}]}).execute()
