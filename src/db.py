from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


DB_URL = 'mysql+pymysql://'+os.getenv("MYSQL_USER")+':'+os.getenv("MYSQL_PASSWORD")+'@'+os.getenv("MYSQL_HOST")+':'+os.getenv("DB_PORT")+'/'+os.getenv("MYSQL_DB")

print(DB_URL)
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()