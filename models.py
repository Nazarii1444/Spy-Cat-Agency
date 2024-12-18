from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, validates
from db import Base


class SpyCat(Base):
    __tablename__ = "spy_cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    years_of_experience = Column(Integer)
    breed = Column(String)
    salary = Column(Float)

    missions = relationship("Mission", back_populates="cat")


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("spy_cats.id"))
    completed = Column(Boolean, default=False)

    cat = relationship("SpyCat", back_populates="missions")
    targets = relationship("Target", back_populates="mission")

    @validates("targets")
    def validate_targets_count(self, key, targets):
        if len(targets) < 1 or len(targets) > 3:
            raise ValueError("A mission must have between 1 and 3 targets.")
        return targets


class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    mission = relationship("Mission", back_populates="targets")
