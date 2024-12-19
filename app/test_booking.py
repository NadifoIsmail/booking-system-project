import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Users, Rooms, Bookings
from datetime import datetime

# Test setup
def setup_module(module):
    global engine, Session, session
    engine = create_engine("sqlite:///:memory:")  # In-memory database for testing
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

def teardown_module(module):
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def user():
    user = Users(name="Test User", email="test@example.com", password="test123")
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def room():
    room = Rooms(type="single", price=100.0, availability=True)
    session.add(room)
    session.commit()
    return room

@pytest.fixture
def booking(user, room):
    booking = Bookings(
        user_id=user.id,
        room_id=room.id,
        check_in=datetime(2024, 12, 25),
        check_out=datetime(2024, 12, 30)
    )
    session.add(booking)
    session.commit()
    return booking

# User management tests
def test_add_user():
    new_user = Users(name="Jane Doe", email="jane@example.com", password="securepass")
    session.add(new_user)
    session.commit()
    assert new_user in session.query(Users).all()

def test_view_users(user):
    users = session.query(Users).all()
    assert len(users) == 1
    assert users[0].name == "Test User"

def test_update_user(user):
    user.name = "Updated User"
    session.commit()
    updated_user = session.query(Users).filter_by(id=user.id).first()
    assert updated_user.name == "Updated User"

def test_delete_user(user):
    session.delete(user)
    session.commit()
    assert session.query(Users).filter_by(id=user.id).first() is None

# Room management tests
def test_add_room():
    new_room = Rooms(type="double", price=150.0, availability=True)
    session.add(new_room)
    session.commit()
    assert new_room in session.query(Rooms).all()

def test_view_rooms(room):
    rooms = session.query(Rooms).all()
    assert len(rooms) == 1
    assert rooms[0].type == "single"

def test_update_room(room):
    room.price = 120.0
    session.commit()
    updated_room = session.query(Rooms).filter_by(id=room.id).first()
    assert updated_room.price == 120.0

def test_delete_room(room):
    session.delete(room)
    session.commit()
    assert session.query(Rooms).filter_by(id=room.id).first() is None

# Booking management tests
def test_add_booking(user, room):
    new_booking = Bookings(
        user_id=user.id,
        room_id=room.id,
        check_in=datetime(2024, 12, 20),
        check_out=datetime(2024, 12, 25)
    )
    session.add(new_booking)
    session.commit()
    assert new_booking in session.query(Bookings).all()

def test_view_bookings(booking):
    bookings = session.query(Bookings).all()
    assert len(bookings) == 1
    assert bookings[0].user_id == booking.user_id

def test_update_booking(booking):
    booking.check_out = datetime(2024, 12, 31)
    session.commit()
    updated_booking = session.query(Bookings).filter_by(id=booking.id).first()
    assert updated_booking.check_out == datetime(2024, 12, 31)

def test_delete_booking(booking):
    session.delete(booking)
    session.commit()
    assert session.query(Bookings).filter_by(id=booking.id).first() is None
