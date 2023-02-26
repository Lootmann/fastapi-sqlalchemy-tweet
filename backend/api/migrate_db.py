from sqlalchemy import create_engine

from api.db import ASYNC_DB_URL
from api.models.likes import Base as LikeBase
from api.models.tweets import Base as TweetBase
from api.models.users import Base as UserBase

engine = create_engine(ASYNC_DB_URL, echo=True, isolation_level="AUTOCOMMIT")


def reset_database():
    LikeBase.metadata.drop_all(bind=engine)
    LikeBase.metadata.create_all(bind=engine)

    TweetBase.metadata.drop_all(bind=engine)
    TweetBase.metadata.create_all(bind=engine)

    UserBase.metadata.drop_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
