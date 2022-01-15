from sqlalchemy import *
##from config import host, port, database, user, password
import pandas as pd

host = "secret.amazonaws.com"
port = "5432"
database = "da1c06fi82ev6c"
user = "tjhqznxnlxlreh"
password = "secret"


conn_str = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(conn_str)
connection = engine.connect()
metadata = MetaData()


first_tb = Table('books_eng', metadata,
   Column('isbn13', BIGINT, primary_key=True),
   Column('isbn10', TEXT, nullable=True),
   Column('title', TEXT, nullable=True),
   Column('subtitle', TEXT, nullable=True),
   Column('authors', TEXT, nullable=True),
   Column('categories', TEXT, nullable=True),
   Column('thumbnail', TEXT, nullable=True),
   Column('description', TEXT, nullable=True),
   Column('published_year', FLOAT, nullable=True),
   Column('average_rating', FLOAT, nullable=True),
   Column('num_pages', FLOAT, nullable=True),
   Column('ratings_count', FLOAT, nullable=True),
)


metadata.create_all(engine)
import os
path = os.getcwd()
data = pd.read_csv(path + "/data/books.csv")
values_list = data

data.to_sql(name="books_eng", con=connection, if_exists="replace", index=False)
engine.execute("SELECT * FROM books_eng").fetchall()
