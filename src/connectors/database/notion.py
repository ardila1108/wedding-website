from notion_client import Client
from src.connectors.database.base import DatabaseConnector


class NotionDatabaseConnector(DatabaseConnector):
    def __init__(self, database_id: str = None):
        if database_id is None:
            self.database_id = "4c17f27b0c014405bd601bd644adc1dc"
        self.client = Client(auth="secret_MgiEJdX3dBTbnNcSIZoyKkaz0f4t6YSVylpgAY2J6Ci")

    def create(self, profile_dict: dict):
        self.client.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "user_id": {"title": [{"text": {"content": profile_dict.get("user_id")}}]},
                "name": {'rich_text': [{'type': 'text', 'text': {'content': profile_dict.get("name")}}]},
                "attending": {"checkbox": profile_dict.get("attending")},
                "restrictions": {'rich_text': [{'type': 'text', 'text': {'content': profile_dict.get("restrictions")}}]},
                "group_id": {'rich_text': [{'type': 'text', 'text': {'content': profile_dict.get("group_id")}}]},
            }
        )

    def read(self, user_id) -> dict:
        parsed_dict = self._parse_profile(user_id)

        if parsed_dict.get("plus_one_id"):
            parsed_dict["plus_one"] = self._get_plus_one(parsed_dict.get("plus_one_id"))
        else:
            parsed_dict["plus_one"] = None

        return parsed_dict

    def update(self, user_id: str, changes_dict: dict):
        page_id = self._get_profile_page(user_id)["id"]
        updated_dict = {}
        if "attending" in changes_dict:
            updated_dict.update({
                "attending": {"checkbox": changes_dict.get("attending")}
            })

        if "name" in changes_dict:
            updated_dict.update({
                "name": {'rich_text': [{'type': 'text', 'text': {'content': changes_dict.get("name")}}]}
            })

        if "restrictions" in changes_dict:
            updated_dict.update({
                "restrictions": {'rich_text': [{'type': 'text', 'text': {'content': changes_dict.get("restrictions")}}]}
            })

        if "plus_one" in changes_dict:
            if changes_dict.get("plus_one"):
                plus_one_id = changes_dict.get("plus_one").get("user_id")
            else:
                plus_one_id = ""
            updated_dict.update({
                "plus_one_id": {'rich_text': [{'type': 'text', 'text': {'content': plus_one_id}}]}
            })

        self.client.pages.update(
            page_id=page_id,
            properties=updated_dict
        )

    def delete(self, user_id: str):
        page_id = self._get_profile_page(user_id)["id"]
        self.client.pages.update(
            page_id=page_id,
            archived=True
        )

    def _get_profile_page(self, user_id):
        return self.client.databases.query(
            **{
                "database_id": self.database_id,
                "filter": {
                    "property": "user_id",
                    "rich_text": {
                        "equals": user_id,
                    },
                },
            }
        )["results"][0]

    def _get_plus_one(self, plus_one_id):
        return self._parse_profile(plus_one_id)

    @staticmethod
    def _parse_field(field_dict: dict):
        field_type = field_dict["type"]
        content = field_dict[field_type]
        if isinstance(content, list):
            if content:
                return field_dict[field_type][0]["text"]["content"]
            return None
        return content

    def _parse_profile(self, user_id: str):
        profile_dict = self._get_profile_page(user_id)["properties"]
        return {
            field: self._parse_field(profile_dict[field]) for field in profile_dict
        }
