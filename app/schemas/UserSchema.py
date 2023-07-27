from pydantic import BaseModel


class User(BaseModel):
    id: int
    chat_id: int
    fullname: str
    is_finished_diary_today: bool = False
