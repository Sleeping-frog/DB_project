from pydantic import BaseModel


# -------- Species --------

class SpeciesBase(BaseModel):
    name: str
    family: str
    habitat: str
    lifespan_years: int


class SpeciesCreate(SpeciesBase):
    pass


class SpeciesOut(SpeciesBase):
    id: int

    class Config:
        orm_mode = True


# -------- Enclosure --------

class EnclosureBase(BaseModel):
    room_number: int
    complex_name: str
    has_pond: bool
    area: float


class EnclosureCreate(EnclosureBase):
    pass


class EnclosureOut(EnclosureBase):
    id: int

    class Config:
        orm_mode = True


# -------- Placement --------

class PlacementBase(BaseModel):
    species_id: int
    enclosure_id: int
    animals_count: int


class PlacementCreate(PlacementBase):
    pass


class PlacementOut(PlacementBase):
    id: int

    class Config:
        orm_mode = True