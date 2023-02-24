from sqlalchemy import create_engine

from api.models.tweets import Base as TweetBase
from api.models.users import Base as UserBase

DB_URL = "sqlite:///dev.db"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    UserBase.metadata.drop_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)

    TweetBase.metadata.drop_all(bind=engine)
    TweetBase.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
