create database loginDB;
use loginDB;
create table users (
	id int auto_increment primary key,
    first_name varchar(50),
    last_name varchar(50),
    email varchar(255),
    password_hash varchar(255),
    created_at datetime,
    updated_at datetime
);

create table friendships (
	id int auto_increment primary key,
    friend_1_id int,
    friend_2_id int,
    created_at datetime,
    updated_at datetime
);

create table messages(
	id int auto_increment primary key,
    user_id int,
    user2_id int,
    content text,
    created_at datetime,
    updated_at datetime
);

