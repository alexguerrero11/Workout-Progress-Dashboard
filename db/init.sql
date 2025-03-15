CREATE DATABASE workout_db;

USE workout_db;

CREATE TABLE workouts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    exercise VARCHAR(255) NOT NULL,
    sets INT NOT NULL,
    reps INT NOT NULL,
    weight FLOAT,
    notes TEXT
);