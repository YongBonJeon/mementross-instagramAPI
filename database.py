from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

# Create a connection to the database
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://admin:Mementross1!@capstone-rds-mysql.clqkkgwacwax.ap-northeast-2.rds.amazonaws.com:3306/capstoneDB"

# Create a session to use the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()