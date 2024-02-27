import base64
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from src.config import env
from src.connectors.database.base import DatabaseConnector


class SheetsDatabaseConnector(DatabaseConnector):
    def __init__(self, profile_sheet_name: str = None, group_sheet_name: str = None):
        self.credentials = Credentials.from_service_account_info(
            {
                "type": "service_account",
                "project_id": env("SHEETS_PROJECT_ID"),
                "private_key_id": env("SHEETS_PRIVATE_KEY_ID"),
                "private_key": base64.b64decode(env("SHEETS_PRIVATE_ENCRIPTED_KEY")).decode(),
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
        if profile_sheet_name is None:
            self.profile_sheet_name = env("SHEETS_PROFILE_SHEET_NAME")
        if group_sheet_name is None:
            self.group_sheet_name = env("SHEETS_GROUP_SHEET_NAME")

    def create(self, profile_dict: dict):
        full_data = self._read_whole_table("user")
        col_names = full_data[0]
        body = {
            "majorDimension": "ROWS",
            "values": [
                [profile_dict.get(col) for col in col_names]
            ]
        }
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=f"{self.profile_sheet_name}!A:Z",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

    def read_user(self, user_id) -> dict:
        profile_dict = self._get_user_profile(user_id)
        parsed_dict = self._parse_profile(profile_dict)
        return parsed_dict

    def read_group(self, group_id) -> dict:
        invite_list = self._get_group_members(group_id)
        group_info = {
            "name": self._get_group_name(group_id),
            "invitee_list": [self._parse_profile(inv) for inv in invite_list]
        }
        return group_info

    def update(self, user_id: str, changes_dict: dict):
        full_data = self._read_whole_table("user")
        user_idx = self._get_user_index(user_id, full_data)
        col_names = full_data[0]
        user_data = self.read_user(user_id)
        user_data.update(changes_dict)

        body = {
            "majorDimension": "ROWS",
            "values": [
                [user_data.get(col) for col in col_names]
            ]
        }

        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f"{self.profile_sheet_name}!A{user_idx+1}:Z{user_idx+1}",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

    def delete(self, user_id: str):
        full_data = self._read_whole_table("user")
        user_idx = self._get_user_index(user_id, full_data)
        body = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheet_id": 0,
                            "dimension": "ROWS",
                            "startIndex": user_idx,
                            "endIndex": user_idx + 1
                        }
                    }
                }
            ]
        }

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=body
        ).execute()

    @staticmethod
    def _get_user_index(user_id: str, full_data: list):
        for idx, user in enumerate(full_data):
            if user[0] == user_id:
                return idx

    def _get_user_profile(self, user_id):
        full_data = self._read_whole_table("user")
        col_names = full_data[0]
        found_user = full_data[self._get_user_index(user_id, full_data)]
        return {
            k: v for (k, v) in zip(col_names, found_user)
        }

    def _get_group_members(self, group_id: str):
        full_data = self._read_whole_table("user")
        col_names = full_data[0]
        group_idx = col_names.index("group_id")
        found_user_list = [user for user in full_data[1:] if user[group_idx] == group_id]
        return [{
            k: v for (k, v) in zip(col_names, found_user)
        } for found_user in found_user_list]

    def _get_group_name(self, group_id: str):
        full_data = self._read_whole_table("group")
        for user in full_data[1:]:
            if user[0] == group_id:
                return user[1]

    def _read_whole_table(self, level: str):
        if level == "user":
            sheet_id = self.profile_sheet_name
        elif level == "group":
            sheet_id = self.group_sheet_name
        else:
            raise NotImplementedError
        data = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=f"{sheet_id}!A:Z"
        ).execute()
        return data["values"]

    @staticmethod
    def _parse_field(field_value):
        bool_value_mapping = {
            "TRUE": True,
            "FALSE": False
        }
        return bool_value_mapping.get(field_value, field_value)

    def _parse_profile(self, profile_dict):
        parsed_dict = {
            field: self._parse_field(v) for field, v in profile_dict.items()
        }
        if parsed_dict.get("plus_one_id"):
            parsed_dict["plus_one"] = self.read_user(parsed_dict.get("plus_one_id"))
        else:
            parsed_dict["plus_one"] = None
        return parsed_dict
