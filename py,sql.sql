DROP DATABASE IF EXISTS HOTEL;
CREATE DATABASE HOTEL;

USE HOTEL;

-- Create table for Guests
CREATE TABLE Guests (
    GuestID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(100),
    Address TEXT
);

-- Add guests
INSERT INTO Guests (FirstName, LastName, PhoneNumber, Email, Address)
VALUES 
('Alice', 'Smith', '2345678901', 'alice.smith@example.com', '456 Elm St'),
('Bob', 'Johnson', '3456789012', 'bob.johnson@example.com', '789 Oak St'),
('Carol', 'Williams', '4567890123', 'carol.williams@example.com', '321 Pine St'),
('David', 'Brown', '5678901234', 'david.brown@example.com', '654 Maple Ave'),
('Eve', 'Davis', '6789012345', 'eve.davis@example.com', '987 Birch Rd'),
('Frank', 'Miller', '7890123456', 'frank.miller@example.com', '321 Cedar Blvd');

select * from Guests;

-- Create table for Rooms
CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY AUTO_INCREMENT,
    RoomNumber VARCHAR(10) UNIQUE,
    RoomType VARCHAR(50),
    BedCount INT,
    PricePerNight DECIMAL(10, 2),
    IsAvailable BOOLEAN DEFAULT TRUE
);

-- Add rooms
INSERT INTO Rooms (RoomNumber, RoomType, BedCount, PricePerNight)
VALUES 
('102', 'Double', 2, 120.00),
('103', 'Suite', 3, 200.00),
('104', 'Single', 1, 75.00),
('105', 'Double', 2, 130.00),
('106', 'Double', 2, 150.00),
('107', 'Suite', 3, 250.00);

-- Create table for Bookings
CREATE TABLE Bookings (
    BookingID INT PRIMARY KEY AUTO_INCREMENT,
    GuestID INT,
    RoomID INT,
    CheckInDate DATE,
    CheckOutDate DATE,
    TotalAmount DECIMAL(10, 2),
    BookingDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (GuestID) REFERENCES Guests(GuestID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

-- Make bookings (RoomIDs are 1 to 6)
INSERT INTO Bookings (GuestID, RoomID, CheckInDate, CheckOutDate, TotalAmount)
VALUES 
(2, 1, '2025-04-21', '2025-04-25', 480.00),
(3, 2, '2025-04-22', '2025-04-24', 400.00),
(4, 3, '2025-04-23', '2025-04-26', 225.00),
(1, 4, '2025-04-24', '2025-04-27', 390.00),
(5, 5, '2025-04-25', '2025-04-28', 450.00),
(6, 6, '2025-04-26', '2025-04-28', 500.00);

-- Create table for Payments
CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    BookingID INT,
    PaymentDate DATE,
    AmountPaid DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID)
);

-- Record payments (BookingIDs will be 1 to 6)
INSERT INTO Payments (BookingID, PaymentDate, AmountPaid, PaymentMethod)
VALUES 
(1, '2025-04-19', 480.00, 'Cash'),
(2, '2025-04-20', 400.00, 'Online'),
(3, '2025-04-21', 225.00, 'Credit Card'),
(4, '2025-04-22', 390.00, 'Credit Card'),
(5, '2025-04-23', 450.00, 'Cash'),
(6, '2025-04-24', 500.00, 'Online');

-- Create table for Accounts
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(50) NOT NULL
);

-- Insert a sample account for testing
INSERT INTO Accounts (Username, Password)
VALUES ('manager', 'password');


select * from Guests;
select * from Rooms;
select * from Bookings;
select * from Payments;



