CREATE DATABASE IF NOT EXISTS cybergrouppr;

USE cybergrouppr;

CREATE USER 'flaskapp'@'%' IDENTIFIED BY 'pa$$123!';
GRANT ALL PRIVILEGES ON cybergrouppr.* TO 'flaskapp'@'%';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS Users(
    id int AUTO_INCREMENT PRIMARY KEY,
    username varchar(50) unique not null,
    pass varchar(128) not null,
    roleInApp enum('admin', 'uploader', 'viewer') not null  
);

INSERT INTO Users (username, pass, roleInApp) Values ('administrator', '@dmin123!', 'admin');
INSERT INTO Users (username, pass, roleInApp) Values ('uploader1', 'Upl0ader123!', 'uploader');
INSERT INTO Users (username, pass, roleInApp) Values ('viewer1', 'V1ewer123!', 'viewer');