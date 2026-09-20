import os

from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///cinema_review.db")
ECHO_SQL = os.getenv("ECHO_SQL", "false").lower() == "true"
engine = create_engine(DATABASE_URL, echo=ECHO_SQL)
# echo shows sql query directly in the terminal when ECHO_SQL=true
def create_tables():
    """Create all tables defined in the Sqlmodel class"""
    #     if the table exist it will be created if not it does nothing
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency that provides database session per request"""
    with Session(engine) as session:
        yield session
