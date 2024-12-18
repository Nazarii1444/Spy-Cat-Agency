from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from db import get_db
from models import Mission, Target, SpyCat

router = APIRouter(prefix="/missions", tags=["Missions"])


class UpdateTarget(BaseModel):
    notes: str
    completed: bool


class TargetCreate(BaseModel):
    id: int
    name: str
    country: str
    notes: str = None


class MissionCreate(BaseModel):
    cat_id: int
    targets: list[TargetCreate]


# Ability to create a mission in the system along with targets in one single request
@router.post("/")
def create_mission(payload: MissionCreate, db: Session = Depends(get_db)):
    cat = db.query(SpyCat).filter(SpyCat.id == payload.cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")

    active_mission = db.query(Mission).filter(Mission.cat_id == payload.cat_id, Mission.completed == False).first()
    if active_mission:
        raise HTTPException(status_code=400, detail="Cat already has an active mission")

    if not (1 <= len(payload.targets) <= 3):
        raise HTTPException(status_code=400, detail="A mission must have between 1 and 3 targets")

    mission = Mission(cat_id=payload.cat_id)
    db.add(mission)
    db.commit()
    db.refresh(mission)

    for target_data in payload.targets:
        target = Target(
            id=target_data.id,
            mission_id=mission.id,
            name=target_data.name,
            country=target_data.country,
            notes=target_data.notes,
        )
        db.add(target)

    db.commit()
    db.refresh(mission)
    return {"message": "Mission created successfully", "mission_id": mission.id}


# Ability to list missions
@router.get("/")
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).all()


# Ability to get a single mission
@router.get("/{mission_id}")
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = (
        db.query(Mission)
        .options(joinedload(Mission.targets))
        .filter(Mission.id == mission_id)
        .first()
    )

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    return mission


# Ability to update mission targets
# Ability to mark mission as completed
@router.put("/{mission_id}/targets/{target_id}")
def update_target(mission_id: int, target_id: int, payload: UpdateTarget, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.completed:
        raise HTTPException(status_code=400, detail="Mission is already completed")

    target = db.query(Target).filter(Target.id == target_id, Target.mission_id == mission_id).first()

    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    if target.completed:
        raise HTTPException(status_code=400, detail="Target is already completed")

    # Ability to update Notes and Completed state
    target.notes = payload.notes
    target.completed = payload.completed

    db.commit()
    db.refresh(target)

    return target


# Ability to delete a mission
@router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.cat_id is not None:
        # A mission cannot be deleted if it is already assigned to a cat
        raise HTTPException(status_code=400, detail="Cannot delete a mission assigned to a cat")

    db.delete(mission)
    db.commit()

    return {"message": "Mission deleted"}
