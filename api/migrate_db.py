from sqlalchemy import create_engine

from api.models.users import Base as user_base

DB_URL = "sqlite:///dev.db"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    user_base.metadata.drop_all(bind=engine)
    user_base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
