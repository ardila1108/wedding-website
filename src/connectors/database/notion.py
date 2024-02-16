from notion_client import Client
from src.config import env
from src.connectors.database.base import DatabaseConnector


class NotionDatabaseConnector(DatabaseConnector):
    def __init__(self, profile_db_id: str = None, group_db_id: str = None):
        if profile_db_id is None:
            self.profile_db_id = env("NOTION_INVITE_LIST_DB")
        if group_db_id is None:
            self.group_db_id = env("NOTION_GROUP_LIST_DB")
        self.client = Client(auth=env("NOTION_API_SECRET_KEY"))

    def create(self, profile_dict: dict):
        self.client.pages.create(
            parent={"database_id": self.profile_db_id},
            properties={
                "user_id": {"title": [{"text": {"content": profile_dict.get("user_id")}}]},
                "name": {'rich_text': [{'type': 'text', 'text': {'content': profile_dict.get("name")}}]},
                "attending": {"checkbox": profile_dict.get("attending")},
                "restrictions": {'rich_text': [{'type': 'text', 'text': {'content': profile_dict.get("restrictions")}}]},
                "group_id": {'rich_text': [{'type': 'text', 'text': {'content': profile_dict.get("group_id")}}]},
            }
        )

    def read_user(self, user_id) -> dict:
        profile_dict = self._get_profile_page(user_id)["properties"]
        parsed_dict = self._parse_profile(profile_dict)

        return parsed_dict

    def read_group(self, group_id) -> dict:
        invite_list = self._get_group_members(group_id)
        group_info = {
            "name": self._get_group_name(group_id),
            "invitee_list": [self._parse_profile(inv["properties"]) for inv in invite_list]
        }
        return group_info

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
                "database_id": self.profile_db_id,
                "filter": {
                    "property": "user_id",
                    "rich_text": {
                        "equals": user_id,
                    },
                },
            }
        )["results"][0]

    def _get_group_members(self, group_id: str):
        return self.client.databases.query(
            **{
                "database_id": self.profile_db_id,
                "filter": {
                    "property": "group_id",
                    "rich_text": {
                        "equals": group_id,
                    },
                },
            }
        )["results"]

    def _get_group_name(self, group_id: str):
        return self.client.databases.query(
            **{
                "database_id": self.group_db_id,
                "filter": {
                    "property": "group_id",
                    "rich_text": {
                        "equals": group_id,
                    },
                },
            }
        )["results"][0]["properties"]["name"]["rich_text"][0]["text"]["content"]

    @staticmethod
    def _parse_field(field_dict: dict):
        field_type = field_dict["type"]
        content = field_dict[field_type]
        if isinstance(content, list):
            if content:
                return field_dict[field_type][0]["text"]["content"]
            return None
        return content

    def _parse_profile(self, profile_dict):
        parsed_dict = {
            field: self._parse_field(profile_dict[field]) for field in profile_dict
        }
        if parsed_dict.get("plus_one_id"):
            parsed_dict["plus_one"] = self.read_user(parsed_dict.get("plus_one_id"))
        else:
            parsed_dict["plus_one"] = None
        return parsed_dict
