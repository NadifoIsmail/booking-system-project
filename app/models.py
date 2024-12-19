from sqlalchemy import Column,Text,Integer,Boolean,DateTime,ForeignKey,create_engine
from sqlalchemy.orm import declarative_base,relationship

engine = create_engine("sqlite:///reservation.sqlite")

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id =Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email= Column(Text, unique=True,nullable=False)
    password= Column(Text,nullable=False)

    bookings = relationship("Bookings",back_populates="users")

class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer,primary_key= True)
    type = Column(Text,nullable=False)
    price = Column(Integer,nullable=False)
    availability = Column(Boolean,default=True)

    bookings = relationship("Bookings", back_populates="rooms")



class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer,ForeignKey('rooms.id'), nullable=False)
    check_in = Column(DateTime,nullable=False)
    check_out = Column(DateTime,nullable=False)

    users = relationship("Users", back_populates="bookings")
    rooms = relationship("Rooms", back_populates="bookings")

    

