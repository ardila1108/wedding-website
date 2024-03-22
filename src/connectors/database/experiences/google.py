import base64
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from src.config import env
from src.connectors.database.experiences.base import ExperienceDatabaseConnector


class SheetsGiftDatabaseConnector(ExperienceDatabaseConnector):
    def __init__(self, gift_sheet_name: str = None, gift_contribution_sheet_name: str = None):
        self.credentials = Credentials.from_service_account_info(
            {
                "type": "service_account",
                "project_id": env("SHEETS_PROJECT_ID"),
                "private_key_id": env("SHEETS_PRIVATE_KEY_ID"),
                "private_key": base64.b64decode(env("SHEETS_PRIVATE_ENCRYPTED_KEY")).decode(),
                "client_email": env("SHEETS_CLIENT_EMAIL"),
                "client_id": env("SHEETS_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cb-wedding%40centering-line-303022.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }
        )
        self.service = build("sheets", "v4", credentials=self.credentials)
        self.spreadsheet_id = env("SHEETS_SPREADSHEET_ID")
        if gift_sheet_name is None:
            self.gift_sheet_name = env("SHEETS_GIFT_SHEET_NAME")
        if gift_contribution_sheet_name is None:
            self.gift_contribution_sheet_name = env("SHEETS_CONTRIBUTION_SHEET_NAME")

    def read_gift(self, gift_id: str):
        full_data = self._read_whole_table("gift")
        col_names = full_data[0]
        found_gift = full_data[self._get_user_index(gift_id, full_data)]
        return {
            k: v for (k, v) in zip(col_names, found_gift)
        }

    def add_contribution(self, gift_contribution: dict):
        pass

    @staticmethod
    def _get_user_index(gift_id: str, full_data: list):
        for idx, gift in enumerate(full_data):
            if gift[0] == gift_id:
                return idx

    def _read_whole_table(self, level: str):
        if level == "gift":
            sheet_id = self.gift_sheet_name
        elif level == "contribution":
            sheet_id = self.gift_contribution_sheet_name
        else:
            raise NotImplementedError
        data = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=f"{sheet_id}!A:Z"
        ).execute()
        return data["values"]

#dr_cl = build("drive", "v3", credentials=db.credentials)
#dr_cl.files().list(q="name='X001.jpeg'").execute()["files"][0]["id"]
#dr_cl.files().get_media(fileId="1oJiD8XsbGwUw6SKUiDZ1K_PX9oyzou-H").execute()