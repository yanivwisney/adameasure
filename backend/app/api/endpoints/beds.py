from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.bed import Bed
from app.schemas.bed import BedCreate, BedUpdate, Bed as BedSchema

router = APIRouter()


@router.post("/", response_model=BedSchema, status_code=status.HTTP_201_CREATED)
def create_bed(bed: BedCreate, db: Session = Depends(get_db)):
    """Create a new bed"""
    # Calculate area if both length and width are provided
    area = None
    if bed.length and bed.width:
        area = bed.length * bed.width

    db_bed = Bed(
        name=bed.name,
        description=bed.description,
        farm_id=bed.farm_id,
        length=bed.length,
        width=bed.width,
        area=area,
        soil_type=bed.soil_type,
        is_active=bed.is_active,
    )
    db.add(db_bed)
    db.commit()
    db.refresh(db_bed)
    return db_bed


@router.get("/", response_model=List[BedSchema])
def get_beds(
    farm_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all beds with optional farm filter"""
    query = db.query(Bed)

    if farm_id:
        query = query.filter(Bed.farm_id == farm_id)

    beds = query.offset(skip).limit(limit).all()
    return beds


@router.get("/{bed_id}", response_model=BedSchema)
def get_bed(bed_id: int, db: Session = Depends(get_db)):
    """Get a specific bed by ID"""
    bed = db.query(Bed).filter(Bed.id == bed_id).first()
    if bed is None:
        raise HTTPException(status_code=404, detail="Bed not found")
    return bed


@router.put("/{bed_id}", response_model=BedSchema)
def update_bed(bed_id: int, bed: BedUpdate, db: Session = Depends(get_db)):
    """Update a bed"""
    db_bed = db.query(Bed).filter(Bed.id == bed_id).first()
    if db_bed is None:
        raise HTTPException(status_code=404, detail="Bed not found")

    update_data = bed.dict(exclude_unset=True)

    # Recalculate area if length or width is updated
    if "length" in update_data or "width" in update_data:
        new_length = update_data.get("length", db_bed.length)
        new_width = update_data.get("width", db_bed.width)
        update_data["area"] = new_length * new_width

    for field, value in update_data.items():
        setattr(db_bed, field, value)

    db.commit()
    db.refresh(db_bed)
    return db_bed


@router.delete("/{bed_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bed(bed_id: int, db: Session = Depends(get_db)):
    """Delete a bed"""
    db_bed = db.query(Bed).filter(Bed.id == bed_id).first()
    if db_bed is None:
        raise HTTPException(status_code=404, detail="Bed not found")

    db.delete(db_bed)
    db.commit()
    return None
