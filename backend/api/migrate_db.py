from sqlalchemy import create_engine

from api.models.likes import Base as LikeBase
from api.models.tweets import Base as TweetBase
from api.models.users import Base as UserBase

DB_URL = "postgresql://postgres:secret@localhost:5432/postgres"
engine = create_engine(DB_URL, echo=True, isolation_level="AUTOCOMMIT")


def reset_database():
    LikeBase.metadata.drop_all(bind=engine)
    LikeBase.metadata.create_all(bind=engine)

    TweetBase.metadata.drop_all(bind=engine)
    TweetBase.metadata.create_all(bind=engine)

    UserBase.metadata.drop_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
