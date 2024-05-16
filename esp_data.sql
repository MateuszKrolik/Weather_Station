CREATE DATABASE IF NOT EXISTS esp_data;
--@block
USE esp_data;
DROP TABLE IF EXISTS sensor_data;
CREATE TABLE sensor_data (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sensor VARCHAR(30) NOT NULL,
    location VARCHAR(30) NOT NULL,
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    reading_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)