CREATE DATABASE hospital_db;

USE hospital_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(10),
    address VARCHAR(255),
    department VARCHAR(255),
    date_time DATETIME,
    reason VARCHAR(255),
    comments VARCHAR(255)
);

select * from appointments;

select * from users;
