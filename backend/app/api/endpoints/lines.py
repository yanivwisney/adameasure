from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.line import Line
from app.models.bed import Bed
from app.schemas.line import (
    LineCreate,
    LineUpdate,
    Line as LineSchema,
)

router = APIRouter()


@router.get("/", response_model=List[LineSchema])
def get_lines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all lines"""
    lines = (
        db.query(Line).filter(Line.is_active == True).offset(skip).limit(limit).all()
    )
    return lines


@router.get("/bed/{bed_id}", response_model=List[LineSchema])
def get_lines_by_bed(bed_id: int, db: Session = Depends(get_db)):
    """Get all lines for a specific bed"""
    # Verify bed exists
    bed = db.query(Bed).filter(Bed.id == bed_id, Bed.is_active == True).first()
    if not bed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bed not found"
        )

    lines = (
        db.query(Line)
        .filter(Line.bed_id == bed_id, Line.is_active == True)
        .order_by(Line.position)
        .all()
    )
    return lines


@router.get("/{line_id}", response_model=LineSchema)
def get_line(line_id: int, db: Session = Depends(get_db)):
    """Get a specific line by ID"""
    line = db.query(Line).filter(Line.id == line_id, Line.is_active == True).first()
    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Line not found"
        )
    return line


@router.post("/", response_model=LineSchema)
def create_line(line: LineCreate, db: Session = Depends(get_db)):
    """Create a new line"""
    # Verify bed exists
    bed = db.query(Bed).filter(Bed.id == line.bed_id, Bed.is_active == True).first()
    if not bed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bed not found"
        )

    # Check if position is already taken in this bed
    existing_line = (
        db.query(Line)
        .filter(
            Line.bed_id == line.bed_id,
            Line.position == line.position,
            Line.is_active == True,
        )
        .first()
    )

    if existing_line:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Position already taken in this bed",
        )

    db_line = Line(**line.dict())
    db.add(db_line)
    db.commit()
    db.refresh(db_line)
    return db_line


@router.put("/{line_id}", response_model=LineSchema)
def update_line(line_id: int, line_update: LineUpdate, db: Session = Depends(get_db)):
    """Update a line"""
    db_line = db.query(Line).filter(Line.id == line_id, Line.is_active == True).first()
    if not db_line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Line not found"
        )

    # If position is being updated, check for conflicts
    if line_update.position is not None and line_update.position != db_line.position:
        existing_line = (
            db.query(Line)
            .filter(
                Line.bed_id == db_line.bed_id,
                Line.position == line_update.position,
                Line.id != line_id,
                Line.is_active == True,
            )
            .first()
        )

        if existing_line:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Position already taken in this bed",
            )

    update_data = line_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_line, field, value)

    db.commit()
    db.refresh(db_line)
    return db_line


@router.delete("/{line_id}")
def delete_line(line_id: int, db: Session = Depends(get_db)):
    """Delete a line (soft delete)"""
    db_line = db.query(Line).filter(Line.id == line_id, Line.is_active == True).first()
    if not db_line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Line not found"
        )

    db_line.is_active = False
    db.commit()

    return {"message": "Line deleted successfully"}
