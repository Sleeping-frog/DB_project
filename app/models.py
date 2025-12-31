from sqlalchemy import Column, Integer, Text, Boolean, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import JSONB

class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)
    family = Column(Text, nullable=False)
    habitat = Column(Text, nullable=False)
    lifespan_years = Column(Integer, nullable=False)
    extra = Column(JSONB)

    placements = relationship("Placement", back_populates="species", cascade="all, delete")


class Enclosure(Base):
    __tablename__ = "enclosure"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(Integer, unique=True, nullable=False)
    complex_name = Column(Text, nullable=False)
    has_pond = Column(Boolean, nullable=False, default=False)
    area = Column(Numeric(10, 2), nullable=False)

    placements = relationship("Placement", back_populates="enclosure", cascade="all, delete")


class Placement(Base):
    __tablename__ = "placement"

    id = Column(Integer, primary_key=True, index=True)

    species_id = Column(Integer, ForeignKey("species.id", ondelete="CASCADE"), nullable=False)
    enclosure_id = Column(Integer, ForeignKey("enclosure.id", ondelete="CASCADE"), nullable=False)

    animals_count = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("species_id", "enclosure_id", name="unique_species_enclosure"),
    )

    species = relationship("Species", back_populates="placements")
    enclosure = relationship("Enclosure", back_populates="placements")
