from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# For a quick out-of-the-box demo without configuring an external database server, we use SQLite.
# To use MySQL natively, change to: SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/event_management"
# To use Oracle natively, change to: SQLALCHEMY_DATABASE_URL = "oracle+oracledb://user:password@localhost:1521/?service_name=XEPDB1"
SQLALCHEMY_DATABASE_URL = "sqlite:///./event_management.db"

# Setting check_same_thread=False is needed for SQLite. With MySQL/Oracle, remove it.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI to get DB sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
