# Import the base class our models inherit from
# Without this, SQLAlchemy wouldn't know anything about our models.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Float,
    Integer,
    Table,
    Date,
)

Base = declarative_base()

# Create CatData class with table name cat_data. This is the table name that will show up in Postges.
class CatData(Base):
    __tablename__ = "cat_data"
    # __table__args__ = {"schema":"cat_tech_database"}  I saw this line here: https://www.youtube.com/watch?v=oNky1SUC5Ak
    Id = Column(Integer, primary_key=True)
    Datetime = Column(Date)  # May change the column name to Date in the csv later
    Entry = Column(DateTime)
    Depart = Column(DateTime)
    Duration = Column(Float)
