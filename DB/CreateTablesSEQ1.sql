CREATE DATABASE IF NOT EXISTS SmartTransitApp;

USE SmartTransitApp;

-- Subway lines (Red, Orange, Blue, Green)
CREATE TABLE mbta_lines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(20),
    code VARCHAR(20),
    is_active BOOLEAN DEFAULT 1
);


-- All subway stations
CREATE TABLE stops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    stop_code VARCHAR(20),
    is_active BOOLEAN DEFAULT true
);

-- Which stops are served by which lines
CREATE TABLE line_stops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    line_id INT,
    stop_id INT,
    stop_sequence INT,
    is_terminal BOOLEAN DEFAULT false,
    FOREIGN KEY (line_id) REFERENCES mbta_lines(id),
    FOREIGN KEY (stop_id) REFERENCES stops(id),
    UNIQUE KEY unique_line_stop_direction (line_id, stop_id)
);

-- Simple fare structure - single price for all
CREATE TABLE fares (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fare_amount DECIMAL(4, 2) NOT NULL,
    fare_type ENUM('standard', 'reduced') NOT NULL,
    description TEXT
);

-- Table for storing transfer stations (stations where multiple lines intersect)
CREATE TABLE station_connections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT,
    line_ids VARCHAR(255),  -- Comma-separated list of line IDs that intersect at this station
    FOREIGN KEY (station_id) REFERENCES stops(id)
);

