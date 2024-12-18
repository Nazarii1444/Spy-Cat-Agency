import requests
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import get_db
from models import SpyCat

router = APIRouter(prefix="/spy_cats", tags=["Spy Cats"])


class SpyCatCreate(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float


# Breed must be validated, see General
def validate_cat_breed(breed: str):
    response = requests.get("https://api.thecatapi.com/v1/breeds")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error validating breed")

    breeds = [b["name"] for b in response.json()]
    if breed not in breeds:
        raise HTTPException(status_code=400, detail="Invalid breed")


# Ability to create a spy cat in the system
@router.post("/")
def create_spy_cat(cat: SpyCatCreate, db: Session = Depends(get_db)):
    # A cat is described as Name, Years of Experience, Breed, and Salary.
    validate_cat_breed(cat.breed)

    new_cat = SpyCat(
        name=cat.name,
        years_of_experience=cat.years_of_experience,
        breed=cat.breed,
        salary=cat.salary,
    )

    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)

    return new_cat


# Ability to list spy cats
@router.get("/")
def list_spy_cats(db: Session = Depends(get_db)):
    return db.query(SpyCat).all()


# Ability to get a single spy cat
@router.get("/{cat_id}")
def get_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()

    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    return cat


class UpdateSalary(BaseModel):
    salary: float


# Ability to update spy cats’ information (Salary)
@router.put("/{cat_id}")
def update_spy_cat(cat_id: int, payload: UpdateSalary, db: Session = Depends(get_db)):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()

    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")

    cat.salary = payload.salary

    db.commit()
    db.refresh(cat)

    return cat


# Ability to remove spy cats from the system
@router.delete("/{cat_id}")
def delete_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()

    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")

    db.delete(cat)
    db.commit()

    return {"status": status.HTTP_200_OK, "message": "Spy cat deleted"}
