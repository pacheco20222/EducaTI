use EducaTI;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    second_name VARCHAR(100),
    lastname VARCHAR(100) NOT NULL,
    second_lastname VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,  -- Store hashed passwords
    email VARCHAR(50) NOT NULL UNIQUE,    -- Ensure unique emails
    birthdate DATE NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Track user creation time
);