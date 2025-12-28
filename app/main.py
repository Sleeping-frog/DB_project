from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import Base, engine, SessionLocal
from app.models import Species, Enclosure, Placement
from app.schemas import (
    SpeciesCreate, SpeciesOut,
    EnclosureCreate, EnclosureOut,
    PlacementCreate, PlacementOut
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zoo REST API")

# -------------------
# Dependency
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- SPECIES CRUD ----------

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

@app.get("/species/filter", response_model=list[SpeciesOut])
def filter_species(family: str = Query(...), habitat: str = Query(...), db: Session = Depends(get_db)):
    return db.query(Species).filter(
        Species.family == family,
        Species.habitat == habitat
    ).all()

@app.get("/species/group_by_total")
def total_animals_per_species(db: Session = Depends(get_db)):
    results = db.query(
        Placement.species_id,
        func.sum(Placement.animals_count).label("total_animals")
    ).group_by(Placement.species_id).all()
    return [{"species_id": s_id, "total_animals": total} for s_id, total in results]

@app.get("/species/sorted", response_model=list[SpeciesOut])
def species_sorted(order: str = "asc", db: Session = Depends(get_db)):
    query = db.query(Species)
    if order.lower() == "desc":
        query = query.order_by(Species.lifespan_years.desc())
    else:
        query = query.order_by(Species.lifespan_years.asc())
    return query.all()

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


# ---------- ENCLOSURES CRUD ----------

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


# ---------- PLACEMENTS CRUD ----------

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

@app.get("/placements/join")
def placements_with_details(db: Session = Depends(get_db)):
    results = db.query(
        Placement,
        Species.name,
        Enclosure.room_number
    ).join(Species, Placement.species_id == Species.id)\
     .join(Enclosure, Placement.enclosure_id == Enclosure.id)\
     .all()

    return [
        {
            "placement_id": p.id,
            "species_name": name,
            "room_number": room_number,
            "animals_count": p.animals_count
        } for p, name, room_number in results
    ]

@app.put("/placements/increase_if_pond")
def increase_animals_if_pond(db: Session = Depends(get_db)):
    placements = db.query(Placement).join(Enclosure).filter(Enclosure.has_pond == True).all()
    for p in placements:
        p.animals_count += 1
    db.commit()
    return {"updated": len(placements)}