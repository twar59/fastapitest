from database import Base, engine
from models import Item

print("Create database...")

Base.metadata.create_all(engine)
