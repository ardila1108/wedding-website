import io
import base64
from PIL import Image
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from src.config import env
from src.connectors.storage.experiences.base import ExperienceImageStorageConnector


class GoogleDriveImageStorageConnector(ExperienceImageStorageConnector):
    def __init__(self):
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
        self.service = build("drive", "v3", credentials=self.credentials)
        self.extensions = ["png", "jpeg", "jpg"]

    def get_image_bytes(self, image_name: str):
        file_id = self._get_image_file_id(image_name)
        if not file_id:
            file_id = ""
        img_bytes = self.service.files().get_media(fileId=file_id).execute()
        return img_bytes

    def _get_image_file_id(self, image_name: str):
        file_id = None
        for ext in self.extensions:
            file_list = self.service.files().list(q=f"name='{image_name}.{ext}'").execute()["files"]
            if file_list:
                file_id = file_list[0]["id"]
                break
        return file_id
