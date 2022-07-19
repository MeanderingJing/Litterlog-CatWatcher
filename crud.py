# CRUD is an acronym for Create, Read, Update, and Delete

from sqlalchemy import create_engine
from .models.py import Base, CatData
import datetime

######################################################################
#  Creating a Table
######################################################################

# Engine gives SQLAlchemy the power to create tables
engine = create_engine(DATABASE_URI)
# The base class our models inherited has the definition of our Book model in its metadata
Base.metadata.create_all(engine)

# To destroy this table (and all tables) in the database, run drop_all method
Base.metadata.drop_all(engine)

# When testing different models and relationships you'll often create and destroy databases until it's all sorted out.
# For this we'll create a function to recreate the database
def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


######################################################################
#  Working with sessions to interact with the new table we created
######################################################################

from sqlalchemy.orm import sessionmaker

# Use the sessionmaker class with engine to return a session factory
Session = sessionmaker(bind=engine)
# Create individual sessions off of the global Session
s = Session()
# Always close the session when you are done using it to free connections and resources
s.close()

######################################################################
#  Inserting rows
######################################################################

# Put data in the model class cat_data
cat_data = CatData(
    Datatime="07-12-2022,Tue",  # These probably shouldn't be strings. Modification is needed for these values
    Entry=datetime("Jul 12 21:40:54 2022,Tue"),  # Modification
    Depart=datetime("Jul 12 21:43:44 2022"),
    Duration="00:02:49",
)

# Let's recreate the database (since we destroyed it) and recreate a session (since we closed it)
recreate_database()
s = Session()
# Now it's as simple as adding the object to the seesion and commiting
s.add(cat_data)
s.commit()  # Now the data shoud be populated into the table already

######################################################################
#  Inserting all data from csv
######################################################################

# Not done
# https://www.andrewvillazon.com/move-data-to-db-with-sqlalchemy/ for csv
# https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/ for yaml
import csv

with open(
    "/home/jetson-inference/CatWatcher/output/Atty20220711.csv",
    encoding="utf-8",
    newline="",
) as f:
    # The DictReader returns each row as a dictionary with key names from the header row
    # By using dictionaries, we'll also be able to use the dictionary unpacking operator when creating our objects.
    data = csv.DictReader(f, quotechar='"')
