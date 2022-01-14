CREATE DATABASE books;


CREATE TABLE books_eng (
  isbn13 BIGINT PRIMARY KEY,
  isbn10 TEXT,
  title TEXT ,
  subtitle TEXT,
  authors TEXT,
  categories TEXT ,
  thumbnail TEXT,
  description TEXT,
  published_year FLOAT,
  average_rating FLOAT,
  num_pages FLOAT,
  ratings_count FLOAT

);

CREATE TABLE books_spa(
  isbn13 BIGINT PRIMARY KEY,
  title TEXT
);

COPY books_eng(isbn13,isbn10,title,subtitle,authors,categories,thumbnail,description,published_year,average_rating,num_pages,ratings_count)
FROM '/home/isaac/PycharmProjects/recommender_system_nerds/data/books.csv'
DELIMITER  ','
CSV HEADER;
