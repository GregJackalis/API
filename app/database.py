from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQL_ALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL, pool_pre_ping=True)

Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#creates a session towrads our database on every request and then close it when we're done
def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password= 'Jackalis.SQL', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesful")
#         break
#     except Exception as error:
#         time.sleep(2)
#         print(f"Connecting to database failed! The error was: \n {error}")
