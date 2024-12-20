import pytest
from models import engine, Base, Users, Rooms, Bookings
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Setup session
Session = sessionmaker(bind=engine)
session = Session()

# Fixtures for setting up and tearing down the database
@pytest.fixture(autouse=True)
def clean_database():
    # Drop and recreate tables before each test
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    session.rollback()

@pytest.fixture
def sample_user():
    user = Users(name="Test User", email="testuser@example.com", password="password123")
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def sample_room():
    room = Rooms(type="single", price=100.0, availability=True)
    session.add(room)
    session.commit()
    return room

@pytest.fixture
def sample_booking(sample_user, sample_room):
    booking = Bookings(
        user_id=sample_user.id,
        room_id=sample_room.id,
        check_in=datetime(2024, 12, 20, 0, 0),  
        check_out=datetime(2024, 12, 25, 0, 0)
    )
    session.add(booking)
    session.commit()
    return booking

# Tests for User Management
def test_add_user():
    user = Users(name="New User", email="newuser@example.com", password="newpassword")
    session.add(user)
    session.commit()
    assert user in session.query(Users).all()

def test_view_users(sample_user):
    users = session.query(Users).all()
    assert len(users) == 1
    assert users[0].name == "Test User"

def test_update_user(sample_user):
    sample_user.name = "Updated User"
    session.commit()
    updated_user = session.query(Users).filter_by(id=sample_user.id).first()
    assert updated_user.name == "Updated User"

def test_delete_user(sample_user):
    session.delete(sample_user)
    session.commit()
    users = session.query(Users).all()
    assert len(users) == 0

# Tests for Room Management
def test_add_room():
    room = Rooms(type="double", price=150.0, availability=True)
    session.add(room)
    session.commit()
    assert room in session.query(Rooms).all()

def test_view_rooms(sample_room):
    rooms = session.query(Rooms).all()
    assert len(rooms) == 1
    assert rooms[0].type == "single"

def test_update_room(sample_room):
    sample_room.price = 120.0
    session.commit()
    updated_room = session.query(Rooms).filter_by(id=sample_room.id).first()
    assert updated_room.price == 120.0

def test_delete_room(sample_room):
    session.delete(sample_room)
    session.commit()
    rooms = session.query(Rooms).all()
    assert len(rooms) == 0

# Tests for Booking Management
def test_add_booking(sample_user, sample_room):
    booking = Bookings(
        user_id=sample_user.id,
        room_id=sample_room.id,
        check_in=datetime(2024, 12, 20),
        check_out=datetime(2024, 12, 25)
    )
    session.add(booking)
    session.commit()
    assert booking in session.query(Bookings).all()

from datetime import datetime

def test_view_bookings(sample_booking):
    bookings = session.query(Bookings).all()
    assert len(bookings) == 1
    
    assert bookings[0].check_in == datetime(2024, 12, 20, 0, 0)
    assert bookings[0].check_out == datetime(2024, 12, 25, 0, 0)

def test_update_booking(sample_booking):
    sample_booking.check_out = datetime(2024, 12, 30, 0, 0)  
    session.commit()
    updated_booking = session.query(Bookings).filter_by(id=sample_booking.id).first()
    assert updated_booking.check_out == datetime(2024, 12, 30, 0, 0)



def test_delete_booking(sample_booking):
    session.delete(sample_booking)
    session.commit()
    bookings = session.query(Bookings).all()
    assert len(bookings) == 0
