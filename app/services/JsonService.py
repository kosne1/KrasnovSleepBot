import json


class JsonService:
    def __init__(self):
        self.path = "app/configs/users.json"

    def read_users(self) -> list:
        with open(self.path, "r") as file:
            data = json.load(file)
        return data["users"]

    def write_users(self, data: list) -> None:
        with open(self.path, 'w') as file:
            json.dump({"users": data}, file)

    def update_is_finished_diary_to_false(self) -> None:
        data = self.read_users()
        for user in data:
            user['is_finished_diary_today'] = False
        self.write_users(data)
