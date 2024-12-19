from models import engine
from sqlalchemy.orm import sessionmaker
from models import Users,Rooms,Bookings
from datetime import datetime
import os

db = sessionmaker(bind=engine)
session = db()

#user management
def add_user():
    name = input("Enter User Name: ")
    email = input("Enter User Email: ")
    password = input("Enter your Password: ")
    user = Users(name=name, email=email, password = password)
    session.add(user)
    session.commit()
    print("User added successfully.")

def view_users():
    users = session.query(Users).all()
    for user in users:
        print(f"{user.id} - {user.name} - {user.email} - {user.password}")

def update_user():
    user_id = int(input("Enter User ID to update: "))
    user = session.query(Users).filter_by(id=user_id).first()
    if user:
        user.name = input(f"Enter new name (current: {user.name}): ")
        user.email = input(f"Enter new email (current: {user.email}): ")
        user.password =input(f"Enter new password (current):{user.password}):")
        session.commit()
        print("User updated successfully.")
    else:
        print("User not found.")

def delete_user():
    user_id = int(input("Enter User ID to delete: "))
    user = session.query(Users).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print("User deleted successfully.")
    else:
        print("User not found.")

#room management
def add_room():
    type = input("Enter Room Type (e.g., Single, Double): ").strip().lower()
    if type != "single" and type != "double":
        print("Invalid room type.Please enter Single or Double ")
        return
    price = float(input("Enter Room Price: "))
    availability = input("Enter Room Availability(Enter Yes/No): ").strip().lower()
    if availability == "yes":
        availability = True
    elif availability == "no":
        availability = False
    else:
        print("Invalid input for availability.Please enter Yes or No ")
        return
    room = Rooms(type=type, price=price, availability=availability)
    session.add(room)
    session.commit()
    print("Room added successfully.")

def view_rooms():
    rooms = session.query(Rooms).all()
    for room in rooms:
        print(f"{room.id} - Type: {room.type} - Price: {room.price} - Available: {room.availability}")

def update_room():
    room_id = int(input("Enter Room ID to update: "))
    room = session.query(Rooms).filter_by(id=room_id).first()
    if room:
        room.type = input(f"Enter new type (current: {room.type}): ")
        if room.type != "single" and room.type != "double":
            print("Invalid room type.Please enter Single or Double ")
            return
        room.price = float(input(f"Enter new price (current: {room.price}): "))
        room.availability = input(f"Enter new availability (Yes/No) (current: {room.availability}): ").strip().lower()
        if room.availability == "yes":
           room.availability = True
        elif room.availability == "no":
            room.availability = False
        else:
            print("Invalid input for availability.Please enter Yes or No ")
            return

        session.commit()
        print("Room updated successfully.")
    else:
        print("Room not found.")

def delete_room():
    room_id = int(input("Enter Room ID to delete: "))
    room = session.query(Rooms).filter_by(id=room_id).first()
    if room:
        session.delete(room)
        session.commit()
        print("Room deleted successfully.")
    else:
        print("Room not found.")

#booking management
def add_booking():
    user_id = int(input("Enter User ID: "))
    room_id = int(input("Enter Room ID: "))
    check_in = input("Enter Check-in Date (YYYY-MM-DD): ")
    check_out = input("Enter Check-out Date (YYYY-MM-DD): ")
    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    booking = Bookings(user_id=user_id, room_id=room_id, check_in=check_in_date, check_out=check_out_date)
    session.add(booking)
    session.commit()
    print("Booking added successfully.")

def update_booking():
    booking_id = int(input("Enter Booking ID to update: "))
    
    booking = session.query(Bookings).filter_by(id=booking_id).first()
    
    if booking is None:
        print("Booking not found!")
        return
    
    print(f"Current details: User ID: {booking.user_id}, Room ID: {booking.room_id}, Check-in: {booking.check_in}, Check-out: {booking.check_out}")
    
    user_id = int(input("Enter new User ID: "))
    room_id = int(input("Enter new Room ID: "))
    
    check_in_str = input("Enter new Check-in Date (YYYY-MM-DD): ")
    check_out_str = input("Enter new Check-out Date (YYYY-MM-DD): ")

    try:
        check_in_date = datetime(check_in_str, '%Y-%m-%d').date()
        check_out_date = datetime(check_out_str, '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    booking.user_id = user_id
    booking.room_id = room_id
    booking.check_in = check_in_date
    booking.check_out = check_out_date
    
    session.commit()
    print("Booking updated successfully.")


def view_bookings():
    bookings = session.query(Bookings).all()
    for booking in bookings:
        print(f"{booking.id} - User ID: {booking.user_id} - Room ID: {booking.room_id} - Check-in: {booking.check_in} - Check-out: {booking.check_out}")

def delete_booking():
    booking_id = int(input("Enter Booking ID to delete: "))
    booking = session.query(Bookings).filter_by(id=booking_id).first()
    if booking:
        session.delete(booking)
        session.commit()
        print("Booking deleted successfully.")
    else:
        print("Booking not found.")

#Menus
def main():
    while True:
        os.system("clear")
        print("=== Hotel Booking System ===")
        print("1. User Management")
        print("2. Room Management")
        print("3. Booking Management")
        print("4. Exit")
        main_menu_choice = input("Enter your Choice: ")

        if main_menu_choice == '1':
            while True:
                os.system("clear")
                print("=== User Management ===")
                print("1. Add User")
                print("2. View Users")
                print("3. Update User")
                print("4. Delete User")
                print("5. Back to Main Menu")
                user_menu_choice = input("Enter your Choice: ")
                if user_menu_choice == '1':
                    add_user()
                elif user_menu_choice == '2':
                    view_users()
                elif user_menu_choice == '3':
                    update_user()
                elif user_menu_choice == '4':
                    delete_user()
                elif user_menu_choice == '5':
                    break
                input("Press Enter to continue...")

        elif main_menu_choice == '2':
            while True:
                os.system("clear")
                print("=== Room Management ===")
                print("1. Add Room")
                print("2. View Rooms")
                print("3. Update Room")
                print("4. Delete Room")
                print("5. Back to Main Menu")
                room_menu_choice = input("Enter your Choice: ")
                if room_menu_choice == '1':
                    add_room()
                elif room_menu_choice == '2':
                    view_rooms()
                elif room_menu_choice == '3':
                    update_room()
                elif room_menu_choice == '4':
                    delete_room()
                elif room_menu_choice == '5':
                    break
                input("Press Enter to continue...")

        elif main_menu_choice == '3':
            while True:
                os.system("clear")
                print("=== Booking Management ===")
                print("1. Add Booking")
                print("2. View Bookings")
                print("3. Update Bookings")
                print("4. Delete Booking")
                print("5. Back to Main Menu")
                booking_menu_choice = input("Enter your Choice: ")
                if booking_menu_choice == '1':
                    add_booking()
                elif booking_menu_choice == '2':
                    view_bookings()
                elif booking_menu_choice == '3':
                    update_booking()
                elif booking_menu_choice == '4':
                    delete_booking()
                elif booking_menu_choice == '5':
                    break
                input("Press Enter to continue...")

        elif main_menu_choice == '4':
            print("Exiting the system")
            break
        else:
            print("Invalid choice! Please choose again.")
            input("Press Enter to continue...")

# Call the main function
main()