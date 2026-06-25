from sqlalchemy import create_engine, select, Column, Integer, String, DateTime, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///waypoint.db')

Base = declarative_base()

class Waypoint(Base):
  __tablename__ = "itineraries"

  id = Column(Integer, primary_key = True)
  username = Column(String, nullable = False)
  origin = Column(String)
  destination = Column(String)
  start_date = Column(Date)
  end_date = Column(Date)
  itinerary = Column(String)
  created_at = Column(DateTime, default = datetime.utcnow)

def make_db(DB_PATH = 'sqlite:///waypoint.db' ):
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

def get_itineraries(session, username):
  statement = select(
    Waypoint.id,
    Waypoint.origin,
    Waypoint.destination,
    Waypoint.start_date,
    Waypoint.end_date,
    Waypoint.created_at
  ).where(Waypoint.username == username)
  
  result = session.execute(statement)
  return result
  
def get_itinerary(session, username, itinerary_id):
  statement = select(
    Waypoint.origin,
    Waypoint.destination,
    Waypoint.start_date,
    Waypoint.end_date,
    Waypoint.itinerary
    ).where(
      Waypoint.id == itinerary_id,
      Waypoint.username == username)

  result = statement.execute(statement).one_or_none()
  return result
