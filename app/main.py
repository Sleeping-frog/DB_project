from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app.models import Species, Enclosure, Placement
from app.schemas import (
    SpeciesCreate, SpeciesOut,
    EnclosureCreate, EnclosureOut,
    PlacementCreate, PlacementOut
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zoo REST API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- SPECIES ----------

@app.post("/species", response_model=SpeciesOut)
def create_species(data: SpeciesCreate, db: Session = Depends(get_db)):
    obj = Species(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/species", response_model=list[SpeciesOut])
def list_species(db: Session = Depends(get_db)):
    return db.query(Species).all()


@app.get("/species/{species_id}", response_model=SpeciesOut)
def get_species(species_id: int, db: Session = Depends(get_db)):
    obj = db.query(Species).get(species_id)
    if not obj:
        raise HTTPException(404)
    return obj


@app.put("/species/{species_id}", response_model=SpeciesOut)
def update_species(species_id: int, data: SpeciesCreate, db: Session = Depends(get_db)):
    obj = db.query(Species).get(species_id)
    if not obj:
        raise HTTPException(404)
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@app.delete("/species/{species_id}")
def delete_species(species_id: int, db: Session = Depends(get_db)):
    obj = db.query(Species).get(species_id)
    if not obj:
        raise HTTPException(404)
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}


# ---------- ENCLOSURES ----------

@app.post("/enclosures", response_model=EnclosureOut)
def create_enclosure(data: EnclosureCreate, db: Session = Depends(get_db)):
    obj = Enclosure(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/enclosures", response_model=list[EnclosureOut])
def list_enclosures(db: Session = Depends(get_db)):
    return db.query(Enclosure).all()


# ---------- PLACEMENTS ----------

@app.post("/placements", response_model=PlacementOut)
def create_placement(data: PlacementCreate, db: Session = Depends(get_db)):
    obj = Placement(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/placements", response_model=list[PlacementOut])
def list_placements(db: Session = Depends(get_db)):
    return db.query(Placement).all()