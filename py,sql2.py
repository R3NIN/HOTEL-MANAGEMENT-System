import mysql.connector
from datetime import datetime

# Database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nitin123",
        database="HOTEL"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Error connecting to database: {err}")
    exit()

def display_start_menu():
    print("\n=== Hotel Management System ===")
    print("1. Login")
    print("2. Registration")
    print("Enter your choice: ", end="")

def display_management_menu():
    print("\n=== Hotel Management System ===")
    print("1. Add Guest")
    print("2. View Bookings")
    print("3. Delete Booking")
    print("4. Make Payment")
    print("5. Check Room Availability")
    print("6. Logout")
    print("7. Book Room")
    print("Enter your choice: ", end="")

def check_account_exists(username):
    query = "SELECT Password FROM Accounts WHERE Username = %s"
    cursor.execute(query, (username,))
    return cursor.fetchone()

def create_account():
    print("=== Registration ===")
    username = input("Enter new username: ")
    cursor.execute("SELECT Username FROM Accounts WHERE Username = %s", (username,))
    if cursor.fetchone():
        print("Username already exists! Please try again.")
        return False
    password = input("Enter new password: ")
    query = "INSERT INTO Accounts (Username, Password) VALUES (%s, %s)"
    try:
        cursor.execute(query, (username, password))
        db.commit()
        print(f"Account for {username} created successfully!")
        return True
    except mysql.connector.Error as err:
        print(f"Error creating account: {err}")
        return False

def login():
    print("=== Login ===")
    username = input("user_id = ")
    password = input("password = ")
    stored_password = check_account_exists(username)
    if stored_password is None:
        print("Account does not exist.")
        choice = input("Would you like to register? (yes/no): ").lower()
        if choice == "yes" and create_account():
            print("Please log in with your new account.")
            return login()
        return None
    elif stored_password[0] == password:
        print("Login successful!")
        return username   # Return the username on successful login
    else:
        print("Incorrect password!")
        return None

def add_guest(current_user):
    print("Enter guest details:")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    phone = input("Phone Number: ")
    email = input("Email: ")
    address = input("Address: ")

    query = """
    INSERT INTO Guests (FirstName, LastName, PhoneNumber, Email, Address, Username)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (first_name, last_name, phone, email, address, current_user)
    try:
        cursor.execute(query, values)
        db.commit()
        print(f"\n✅ Guest {first_name} {last_name} added successfully!")

        cursor.execute("SELECT * FROM Guests WHERE Email = %s", (email,))
        guest = cursor.fetchone()
        print("\n--- Guest Added ---")
        print(f"Guest ID   : {guest[0]}")
        print(f"First Name : {guest[1]}")
        print(f"Last Name  : {guest[2]}")
        print(f"Phone      : {guest[3]}")
        print(f"Email      : {guest[4]}")
        print(f"Address    : {guest[5]}")
        print(f"Username   : {guest[6]}")
        print("--------------------\n")
    except mysql.connector.Error as err:
        print(f"❌ Error adding guest: {err}")

def view_bookings(current_user):
    print("\n=== Your Bookings ===")
    query = """
    SELECT b.BookingID, g.FirstName, g.LastName, r.RoomNumber, b.CheckInDate, b.CheckOutDate, b.TotalAmount
    FROM Bookings b
    JOIN Guests g ON b.GuestID = g.GuestID
    JOIN Rooms r ON b.RoomID = r.RoomID
    WHERE g.Username = %s
    """
    try:
        cursor.execute(query, (current_user,))
        bookings = cursor.fetchall()
        if not bookings:
            print("No bookings found for your account!")
        else:
            for booking in bookings:
                print(f"Booking ID: {booking[0]} | Guest: {booking[1]} {booking[2]} | Room: {booking[3]} | "
                      f"Check-In: {booking[4]} | Check-Out: {booking[5]} | Total: ${booking[6]}")
    except mysql.connector.Error as err:
        print(f"Error viewing bookings: {err}")

def delete_booking(current_user):
    view_bookings(current_user)
    booking_id = input("Enter the Booking ID to delete: ")
    cursor.execute("SELECT RoomID FROM Bookings WHERE BookingID = %s", (booking_id,))
    room = cursor.fetchone()
    if not room:
        print("Booking not found!")
        return
    room_id = room[0]
    try:
        cursor.execute("DELETE FROM Bookings WHERE BookingID = %s", (booking_id,))
        cursor.execute("UPDATE Rooms SET IsAvailable = TRUE WHERE RoomID = %s", (room_id,))
        db.commit()
        print(f"Booking ID {booking_id} deleted and room set available!")
    except mysql.connector.Error as err:
        print(f"Error deleting booking: {err}")

def make_payment(current_user):
    view_bookings(current_user)
    booking_id = input("Enter the Booking ID to make payment for: ")

    # Check if payment already exists
    cursor.execute("SELECT * FROM Payments WHERE BookingID = %s", (booking_id,))
    if cursor.fetchone():
        print("Payment already made for this booking!")
        return

    amount = float(input("Enter amount to pay: "))
    method = input("Payment Method (Cash/Online/Credit Card): ")
    payment_date = datetime.now().strftime('%Y-%m-%d')

    query = """
    INSERT INTO Payments (BookingID, PaymentDate, AmountPaid, PaymentMethod)
    VALUES (%s, %s, %s, %s)
    """
    values = (booking_id, payment_date, amount, method)
    try:
        cursor.execute(query, values)
        db.commit()
        print(f"Payment of ${amount} for Booking ID {booking_id} recorded successfully!")
    except mysql.connector.Error as err:
        print(f"Error recording payment: {err}")

def check_room_availability():
    print("\n=== Room Availability ===")
    query = "SELECT RoomNumber, RoomType, IsAvailable FROM Rooms WHERE IsAvailable = TRUE"
    try:
        cursor.execute(query)
        rooms = cursor.fetchall()
        if not rooms:
            print("No available rooms found!")
        else:
            for room in rooms:
                print(f"Room: {room[0]} | Type: {room[1]} | Status: Available")
    except mysql.connector.Error as err:
        print(f"Error checking room availability: {err}")

def book_room(current_user):
    print("\n=== Available Guests ===")
    query = "SELECT GuestID, FirstName, LastName FROM Guests WHERE Username = %s"
    try:
        cursor.execute(query, (current_user,))
        guests = cursor.fetchall()
        if not guests:
            print("No guests found! Please add a guest first.")
            return
        for guest in guests:
            print(f"Guest ID: {guest[0]} | Name: {guest[1]} {guest[2]}")
    except mysql.connector.Error as err:
        print(f"Error fetching guests: {err}")
        return

    check_room_availability()
    guest_id = int(input("Enter Guest ID to book for: "))
    room_number = input("Enter Room Number to book: ")

    cursor.execute("SELECT RoomID, PricePerNight FROM Rooms WHERE RoomNumber = %s AND IsAvailable = TRUE", (room_number,))
    room = cursor.fetchone()
    if not room:
        print("Room not available or does not exist!")
        return
    room_id, price_per_night = room

    check_in = input("Enter Check-In Date (YYYY-MM-DD): ")
    check_out = input("Enter Check-Out Date (YYYY-MM-DD): ")
    check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
    check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
    nights = (check_out_date - check_in_date).days
    total_amount = nights * price_per_night

    query = """
    INSERT INTO Bookings (GuestID, RoomID, CheckInDate, CheckOutDate, TotalAmount)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (guest_id, room_id, check_in, check_out, total_amount)
    try:
        cursor.execute(query, values)
        cursor.execute("UPDATE Rooms SET IsAvailable = FALSE WHERE RoomID = %s", (room_id,))
        db.commit()
        print(f"Room {room_number} booked successfully for Guest ID {guest_id} with Total Amount ${total_amount}!")
    except mysql.connector.Error as err:
        print(f"Error booking room: {err}")

    view_bookings(current_user)

# Main Program
logged_in_user = None

while not logged_in_user:
    display_start_menu()
    choice = input()
    if choice == "1":
        user = login()
        if user:
            logged_in_user = user
            print("\n=== Debug Console ===\nTERMINAL\nPOSTMAN CONSOLE")
    elif choice == "2":
        if create_account():
            print("Please log in with your new account.")
        else:
            print("Registration failed. Please try again.")
    else:
        print("Invalid choice! Please try again.")

while logged_in_user:
    display_management_menu()
    choice = input()
    if choice == "1":
        add_guest(logged_in_user)
    elif choice == "2":
        view_bookings(logged_in_user)
    elif choice == "3":
        delete_booking(logged_in_user)
    elif choice == "4":
        make_payment(logged_in_user)
    elif choice == "5":
        check_room_availability()
    elif choice == "6":
        print("Logout")
        logged_in_user = None
    elif choice == "7":
        book_room(logged_in_user)
    else:
        print("Invalid choice! Please try again.")

print("=== End of Session ===")
cursor.close()
db.close()
