from app.schemas.UserSchema import User
from app.services import JsonService


class UserService:
    def __init__(self):
        self.json_service = JsonService()

    def get_users(self) -> list[User]:
        return [User.parse_obj(user) for user in self.json_service.read_users()]

    def get_user_by_id(self, id: int) -> User:
        users = self.get_users()
        return next((user for user in users if user.id == id), None)

    def upsert_user(self, user: User) -> None:
        data = self.json_service.read_users()
        users: list[User] = [User.parse_obj(user) for user in data]

        # Check if user is already in JSON file
        for temp_user in users:
            if temp_user.id == user.id:
                users.pop(users.index(temp_user))
                break

        # If user is not in JSON file, add them
        users.append(user)
        self.json_service.write_users([
            {
                "id": user.id,
                "fullname": user.fullname,
                "is_finished_diary_today": user.is_finished_diary_today,
                "chat_id": user.chat_id
            } for user in users])
