from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Create a file named 'school.db' in the current directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./school.db"

session = Session

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your database models (if you create tables later)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db  #jatibela chaiyo akko aai garxa
    finally:
        db.close()