CREATE DATABASE matcha IF NOT EXISTS;

\c matcha;

CREATE TABLE IF NOT EXISTS todo (
    todo_id SERIAL PRIMARY KEY,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    gender VARCHAR(50),
    sexual_preferences VARCHAR(50),
    biography TEXT,
    fame_rating INTEGER DEFAULT 0,
    profile_picture_url TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_activated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);