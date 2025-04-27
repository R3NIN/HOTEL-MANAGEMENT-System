-- Drop and create the database
DROP DATABASE IF EXISTS HOTEL;

CREATE DATABASE HOTEL;

USE HOTEL;

-- Table: Guests
CREATE TABLE Guests (
    GuestID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    PhoneNumber VARCHAR(20),
    Email VARCHAR(100),
    Address TEXT,
    Username VARCHAR(50) -- Add this column for linking with Accounts
);

-- Sample Guests with Username
INSERT INTO Guests (FirstName, LastName, PhoneNumber, Email, Address, Username)
VALUES 
('Alice', 'Smith', '2345678901', 'alice.smith@example.com', '456 Elm St', 'alice');

-- Table: Rooms
CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY AUTO_INCREMENT,
    RoomNumber VARCHAR(10) UNIQUE NOT NULL,
    RoomType VARCHAR(50),
    BedCount INT,
    PricePerNight DECIMAL(10, 2),
    IsAvailable BOOLEAN DEFAULT TRUE
);

-- Sample Rooms
INSERT INTO Rooms (RoomNumber, RoomType, BedCount, PricePerNight)
VALUES 
('101', 'Double', 2, 120.00),
('102', 'Single', 1, 80.00),
('103', 'Suite', 3, 250.00),
('104', 'Double', 2, 130.00),
('105', 'Single', 1, 85.00),
('201', 'Suite', 2, 300.00),
('202', 'Double', 2, 140.00),
('203', 'Single', 1, 75.00),
('204', 'Double', 2, 125.00),
('205', 'Suite', 3, 270.00),
('301', 'Penthouse', 4, 500.00),
('302', 'Double', 2, 150.00),
('303', 'Single', 1, 90.00),
('304', 'Suite', 3, 280.00),
('305', 'Single', 1, 95.00);

-- Table: Bookings
CREATE TABLE Bookings (
    BookingID INT PRIMARY KEY AUTO_INCREMENT,
    GuestID INT,
    RoomID INT,
    CheckInDate DATE,
    CheckOutDate DATE,
    TotalAmount DECIMAL(10, 2),
    BookingDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (GuestID) REFERENCES Guests(GuestID) ON DELETE CASCADE,
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE CASCADE
);

-- Sample Bookings
INSERT INTO Bookings (GuestID, RoomID, CheckInDate, CheckOutDate, TotalAmount)
VALUES 
(1, 1, '2025-04-21', '2025-04-25', 480.00);

-- Table: Payments
CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    BookingID INT,
    PaymentDate DATE,
    AmountPaid DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID) ON DELETE CASCADE
);

-- Sample Payments (Now BookingID 1 exists)
INSERT INTO Payments (BookingID, PaymentDate, AmountPaid, PaymentMethod)
VALUES 
(1, '2025-04-19', 480.00, 'Cash');

-- Table: Accounts
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(50) NOT NULL
);

-- Sample Account
INSERT INTO Accounts (Username, Password)
VALUES ('manager', 'password');


select * from Guests;

select * from Rooms;

select * from Bookings;

select * from Payments;

select * from Accounts;




