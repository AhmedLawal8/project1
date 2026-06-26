from sqlalchemy import create_engine, select, func, Column, Integer, String, Text, DateTime, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "waypoint.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

Base = declarative_base()

class Waypoint(Base):
  __tablename__ = "itineraries"

  id = Column(Integer, primary_key = True)
  username = Column(String, nullable = False)
  origin = Column(String)
  destination = Column(String)
  start_date = Column(Date)
  end_date = Column(Date)
  itinerary = Column(Text)
  created_at = Column(DateTime, default = datetime.utcnow)

def make_db():
  Base.metadata.create_all(engine)
  session_local = sessionmaker(bind = engine)
  return session_local()

def insert_itinerary(session, username, origin, destination, start_date, end_date, itinerary):

  new_itinerary = Waypoint(
    username = username,
    origin = origin,
    destination = destination,
    start_date = start_date,
    end_date = end_date,
    itinerary = itinerary
  )

  session.add(new_itinerary)
  session.commit()

def get_list_of_itineraries(session, username):
  statement = select(Waypoint).where(Waypoint.username == username)
  
  result = session.execute(statement).scalars().all()
  return result
  
def get_itinerary(session, username, itinerary_id):
  statement = select(Waypoint).where( Waypoint.id == itinerary_id, Waypoint.username == username)

  result = session.execute(statement).scalars().one_or_none()
  return result

def get_user(session, username):
  statement = select(Waypoint).where(Waypoint.username == username)
  return session.execute(statement).scalars().first()

def get_itineraries_count(session, username):
  statement = select(func.count()).where(Waypoint.username == username)
  return session.execute(statement).scalar()
