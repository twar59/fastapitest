from database import Base
from sqlalchemy import String, Boolean, Integer, Column, Text

class Item(Base):
    __tablename__="items"

    id=Column(Integer, primary_key=True)
    name=Column(String(255), nullable=False, unique=True)
    price=Column(Integer, nullable=False)
    description=Column(Text)
    on_offer=Column(Boolean, default=False)

    def __repr__(self):
          return f"<Item name={self.name} description={self.description}>"
