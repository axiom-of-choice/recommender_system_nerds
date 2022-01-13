CREATE DATABASE IF NOT EXISTS books;
CREATE TABLE books.books_eng (
  isbn13 INT PRIMARY KEY,
  isbn10 INT,
  title TEXT ,
  subtitle TEXT,
  authors TEXT,
  categories TEXT ,
  thumbnail TEXT,
  description TEXT ,
  published_year INT,
  average_rating FLOAT
);

CREATE TABLE books.books_spa(
  isbn13 INT PRIMARY KEY,
  title TEXT
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/books.csv'
INTO TABLE books.books_eng
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' (isbn13,isbn10,title,subtitle,authors,categories,thumbnail,description,published_year,average_rating);