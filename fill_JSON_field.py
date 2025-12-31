from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Species
from app.database import Base

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/zoo_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

notes_examples = [
    "Dangerous preditor",
    "Rare specie",
    "Friendly animal",
    "Night lifestyle",
    "Needs a big encousure"
]

species_list = session.query(Species).all()

for i, sp in enumerate(species_list):
    sp.extra = {
        "notes": notes_examples[i % len(notes_examples)],
        "origin": "zoo import",
        "feed_times": [9, 15, 20]
    }

session.commit()
session.close()

print("JSON-field successfully filled")