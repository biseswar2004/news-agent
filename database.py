# database.py
# Creates and manages our SQLite database
# SQLite = one simple file on your computer, no server needed

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Creates news_agent.db file in your project folder
engine = create_engine("sqlite:///news_agent.db", echo=False)
Base = declarative_base()

# TABLE 1 - stores each morning briefing
class Briefing(Base):
    __tablename__ = "briefings"
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    script = Column(Text, nullable=False)
    audio_path = Column(String, nullable=True)
    topics_used = Column(String, nullable=True)
    articles_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

# TABLE 2 - stores every article fetched
class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    source = Column(String, nullable=True)
    link = Column(String, nullable=True)

# TABLE 3 - stores logs of every run
class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

# Create all tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# SAVE a new briefing
def save_briefing(date, script, audio_path, topics, count):
    session = Session()
    b = Briefing(date=date, script=script, audio_path=audio_path,
                 topics_used=topics, articles_count=count)
    session.add(b)
    session.commit()
    session.close()
    print(f"✓ Briefing saved for {date}")

# GET all briefings newest first
def get_all_briefings():
    session = Session()
    result = session.query(Briefing).order_by(Briefing.id.desc()).all()
    session.close()
    return result

# GET one briefing by date
def get_briefing_by_date(date):
    session = Session()
    result = session.query(Briefing).filter_by(date=date).first()
    session.close()
    return result

# SAVE articles
def save_articles(date, articles):
    session = Session()
    for a in articles:
        article = Article(
            date=date,
            title=a.get("title", ""),
            summary=a.get("summary", ""),
            source=a.get("source", ""),
            link=a.get("link", "")
        )
        session.add(article)
    session.commit()
    session.close()
    print(f"✓ {len(articles)} articles saved")

# SAVE a log entry
def save_log(date, status, message, duration=None):
    session = Session()
    log = Log(date=date, status=status,
              message=message, duration_seconds=duration)
    session.add(log)
    session.commit()
    session.close()

# GET all logs
def get_all_logs():
    session = Session()
    result = session.query(Log).order_by(Log.id.desc()).limit(50).all()
    session.close()
    return result

# TEST - run: python database.py
if __name__ == "__main__":
    print("Testing database...")
    save_briefing("2026-05-01", "Good morning! Test briefing.",
                  "audio/test.mp3", "AI, cricket", 10)
    all_b = get_all_briefings()
    print(f"Total briefings: {len(all_b)}")
    print("✓ Database working!")