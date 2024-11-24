import streamlit as st
import mysql.connector
from datetime import date

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="hotel_booking"
    )

# User Authentication
def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Admin Page
def admin_dashboard():
    st.title("Admin Dashboard")
    menu = ["Add Room", "Manage Bookings", "Generate Reports"]
    choice = st.selectbox("Select Action", menu)

    if choice == "Add Room":
        add_room()
    elif choice == "Manage Bookings":
        manage_bookings()
    elif choice == "Generate Reports":
        generate_reports()
def add_booking():
    st.subheader("Book a Room")
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch available rooms
        query = "SELECT * FROM rooms WHERE availability = TRUE"
        cursor.execute(query)
        rooms = cursor.fetchall()

        if rooms:
            # Map room options for selection
            room_options = {f"Room {room['room_number']} ({room['room_type']}) - ${room['price_per_night']}": room['id'] for room in rooms}
            selected_room = st.selectbox("Select a Room", list(room_options.keys()))
            customer_name = st.text_input("Customer Name")
            check_in = st.date_input("Check-In Date", min_value=date.today())
            check_out = st.date_input("Check-Out Date", min_value=check_in)

            if st.button("Confirm Booking"):
                room_id = room_options[selected_room]
                
                # Insert booking details
                query = "INSERT INTO bookings (customer_name, room_id, check_in, check_out) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (customer_name, room_id, check_in, check_out))
                conn.commit()

                # Mark room as unavailable
                cursor.execute("UPDATE rooms SET availability = FALSE WHERE id = %s", (room_id,))
                conn.commit()

                st.success(f"Room {selected_room} successfully booked for {customer_name}!")
        else:
            st.write("No available rooms at the moment.")

        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

def view_rooms():
    st.subheader("Available Rooms")
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM rooms WHERE availability = TRUE"
        cursor.execute(query)
        rooms = cursor.fetchall()

        if rooms:
            for room in rooms:
                st.write(f"Room Number: {room['room_number']}")
                st.write(f"Type: {room['room_type']}")
                st.write(f"Price per Night: ${room['price_per_night']}")
                st.write("---")
        else:
            st.write("No rooms are currently available.")
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

# Add Room
def add_room():
    st.subheader("Add a New Room")
    room_number = st.text_input("Room Number")
    room_type = st.selectbox("Room Type", ["Single", "Double", "Suite"])
    price = st.number_input("Price per Night", min_value=0.0, step=0.01)
    if st.button("Add Room"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO rooms (room_number, room_type, price_per_night, availability) VALUES (%s, %s, %s, TRUE)"
            cursor.execute(query, (room_number, room_type, price))
            conn.commit()
            st.success("Room added successfully.")
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# Manage Bookings
def manage_bookings():
    st.subheader("Manage Bookings")
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bookings")
        bookings = cursor.fetchall()

        for booking in bookings:
            st.write(f"Booking ID: {booking['id']}, Customer: {booking['customer_name']}, Room ID: {booking['room_id']}, Check-In: {booking['check_in']}, Check-Out: {booking['check_out']}")
            if st.button(f"Cancel Booking {booking['id']}"):
                cancel_booking(booking['id'])
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

def cancel_booking(booking_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        conn.commit()
        st.success("Booking canceled successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

# Generate Reports
def generate_reports():
    st.subheader("Generate Reports")
    report_type = st.selectbox("Select Report Type", ["Daily", "Monthly", "Custom"])
    if report_type == "Daily":
        generate_daily_report()
    elif report_type == "Monthly":
        generate_monthly_report()
    elif report_type == "Custom":
        generate_custom_report()

def generate_daily_report():
    today = date.today()
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM bookings WHERE DATE(check_in) = %s OR DATE(check_out) = %s"
        cursor.execute(query, (today, today))
        bookings = cursor.fetchall()
        if bookings:
            st.write("Today's Bookings:")
            for booking in bookings:
                st.write(f"Booking ID: {booking['id']}, Customer: {booking['customer_name']}, Room: {booking['room_id']}, Check-In: {booking['check_in']}, Check-Out: {booking['check_out']}")
        else:
            st.write("No bookings for today.")
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error: {e}")

# Customer Page
def customer_dashboard():
    st.title("Customer Dashboard")
    menu = ["View Rooms", "Book Room", "View My Bookings"]
    choice = st.selectbox("Select Action", menu)

    if choice == "View Rooms":
        view_rooms()
    elif choice == "Book Room":
        add_booking()
    elif choice == "View My Bookings":
        view_customer_bookings()

# View Customer Bookings
def view_customer_bookings():
    st.subheader("Your Bookings")
    customer_name = st.text_input("Enter Your Name")
    if st.button("View"):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM bookings WHERE customer_name = %s"
            cursor.execute(query, (customer_name,))
            bookings = cursor.fetchall()
            for booking in bookings:
                st.write(f"Booking ID: {booking['id']}, Room ID: {booking['room_id']}, Check-In: {booking['check_in']}, Check-Out: {booking['check_out']}")
            cursor.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# Main Function
def main():
    st.sidebar.title("Navigation")
    role = st.sidebar.selectbox("Select Role", ["Customer", "Admin"])
    if role == "Customer":
        customer_dashboard()
    elif role == "Admin":
        admin_dashboard()

if __name__ == "__main__":
    main()
