from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    query = Column(Text, nullable=False)
    source = Column(String(50), nullable=False)  # Google / YouTube
    title = Column(Text, nullable=False)
    link = Column(Text, nullable=False)
    snippet = Column(Text, nullable=False)  # Updated to match MySQL (was nullable=True)
    rank_score = Column(Float, nullable=True, default=0.0)  # Matches MySQL `DEFAULT 0`