import random

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/promo")
def create_promo(create_promo_query: schemas.PromoActionCreate,
                 db: Session = Depends(get_db)):
    """
    Creates new promo action.
    """
    promo_id = crud.create_promo(db, create_promo_query)
    return promo_id


@app.get("/promo", response_model=list[schemas.PromoActionSimple])
def get_promos(db: Session = Depends(get_db)):
    """
    Returns all existing promo actions without prizes and participants.
    """
    promos = crud.get_all_simple_promos(db)
    return promos


@app.get("/promo/{promo_id}", response_model=schemas.PromoAction)
def get_promo(promo_id: int, db: Session = Depends(get_db)):
    """
    Returns single promo action with all existing information about it.
    """
    promo = crud.get_promo(db, promo_id)
    if promo is None:
        raise HTTPException(
            status_code=404,
            detail=f"Promo with id {promo_id} doesn't exist"
        )
    return promo


@app.put("/promo/{promo_id}")
def edit_promo(promo_id: int, promo: schemas.PromoActionCreate,
               db: Session = Depends(get_db)):
    """
    Changes name and/or description of a promo action.
    """
    success = crud.edit_promo(db, promo_id, promo)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Promo with id {promo_id} doesn't exist"
        )


@app.delete("/promo/{promo_id}")
def delete_promo(promo_id: int, db: Session = Depends(get_db)):
    """
    Deletes promo action with all its prizes and participants.
    """
    success = crud.delete_promo(db, promo_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Promo with id {promo_id} doesn't exist"
        )


@app.post("/promo/{promo_id}/participant")
def create_participant(promo_id: int, participant: schemas.ParticipantCreate,
                       db: Session = Depends(get_db)):
    """
    Creates new participant for given promo action.
    """
    try:
        participant_id = crud.create_participant(db, promo_id, participant)
        return participant_id
    except RuntimeError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@app.delete("/promo/{promo_id}/participant/{participant_id}")
def delete_participant(promo_id: int, participant_id: int,
                       db: Session = Depends(get_db)):
    """
    Deletes existing participant.
    """
    try:
        crud.delete_participant(db, promo_id, participant_id)
    except RuntimeError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@app.post("/promo/{promo_id}/prize")
def create_prize(promo_id: int, prize: schemas.PrizeCreate,
                 db: Session = Depends(get_db)):
    """
    Creates new prize for given promo action.
    """
    try:
        prize_id = crud.create_prize(db, promo_id, prize)
        return prize_id
    except RuntimeError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@app.delete("/promo/{promo_id}/prize/{prize_id}")
def delete_prize(promo_id: int, prize_id: int,
                 db: Session = Depends(get_db)):
    """
    Deletes existing prize.
    """
    try:
        crud.delete_prize(db, promo_id, prize_id)
    except RuntimeError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@app.post("/promo/{promo_id}/raffle", response_model=list[schemas.RaffleResult])
def make_raffle(promo_id: int, db: Session = Depends(get_db)):
    """
    Raffles single promo action.
    """
    promo = crud.get_promo(db, promo_id)
    if promo is None:
        raise HTTPException(
            status_code=404,
            detail=f"Promo with id {promo_id} doesn't exist"
        )

    if len(promo.participants) != len(promo.prizes):
        raise HTTPException(
            status_code=409,
            detail="Length of prizes and participants should be equal"
        )

    if not promo.participants:
        raise HTTPException(
            status_code=409,
            detail="No one is registered for an action"
        )

    selected_prizes = random.sample(promo.prizes, k=len(promo.prizes))
    results = []
    for participant, prize in zip(promo.participants, selected_prizes):
        results.append(schemas.RaffleResult(winner=participant, prize=prize))
    return results
