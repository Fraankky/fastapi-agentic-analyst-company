from sqlmodel import Field, SQLModel


class ChatSession(SQLModel, table=True):
    # __tablename__ = "chatsession"
    id: int | None = Field(default=None, primary_key=True)
