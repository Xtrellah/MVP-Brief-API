from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ChallengeData(Base):
    __tablename__ = 'challenges'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    skill = Column(JSONB, nullable=True)
    industry = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    scenario = Column(Text, nullable=True)
    challenge = Column(Text, nullable=True)
    task = Column(Text, nullable=True)
