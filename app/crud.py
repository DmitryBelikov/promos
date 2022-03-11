from sqlalchemy.orm import Session

from . import models, schemas


def get_all_promos(db: Session):
    return db.query(models.PromoAction).all()


def get_promo(db: Session, promo_id: int):
    promos = get_all_promos(db)
    for promo in promos:
        if promo.id == promo_id:
            return promo
    return None


def get_all_simple_promos(db: Session):
    promos = get_all_promos(db)
    return [schemas.PromoActionSimple.from_orm(promo) for promo in promos]


def create_promo(db: Session,
                 create_promo_query: schemas.PromoActionCreate) -> int:
    promo = models.PromoAction(**create_promo_query.dict())
    db.add(promo)
    db.commit()
    return promo.id


def delete_promo(db: Session, promo_id: int):
    promo = get_promo(db, promo_id)
    if promo is None:
        return False
    db.query(models.PromoAction)\
      .filter(models.PromoAction.id == promo_id)\
      .delete()
    db.commit()
    return True


def edit_promo(db: Session, promo_id: int,
               promo_update: schemas.PromoActionCreate):
    promo = get_promo(db, promo_id)
    if promo is None:
        return False
    db.query(models.PromoAction)\
      .filter(models.PromoAction.id == promo_id)\
      .update(promo_update.dict())
    db.commit()
    return True


def create_participant(db: Session, promo_id: int,
                       create_participant_query: schemas.ParticipantCreate):
    promo = get_promo(db, promo_id)
    if promo is None:
        raise RuntimeError(f"Promo action with id {promo_id} doesn't exist")
    participant_data = create_participant_query.dict()
    participant_data['promo_id'] = promo_id
    participant = models.Participant(**participant_data)
    db.add(participant)
    db.commit()
    return participant.id


def delete_participant(db: Session, promo_id: int, participant_id: int):
    promo = get_promo(db, promo_id)
    if promo is None:
        raise RuntimeError(f"Promo action with id {promo_id} doesn't exist")
    for participant in promo.participants:
        if participant.id == participant_id:
            db.query(models.Participant)\
              .filter(models.Participant.id == participant_id)\
              .filter(models.Participant.promo_id == promo_id).delete()
            db.commit()
            return
    raise RuntimeError(
        f"Promo {promo_id} doesn't contain participant {participant_id}"
    )


def create_prize(db: Session, promo_id: int,
                 create_prize_query: schemas.PrizeCreate):
    promo = get_promo(db, promo_id)
    if promo is None:
        raise RuntimeError(f"Promo action with id {promo_id} doesn't exist")
    prize_data = create_prize_query.dict()
    prize_data['promo_id'] = promo_id
    prize = models.Prize(**prize_data)
    db.add(prize)
    db.commit()
    return prize.id


def delete_prize(db: Session, promo_id: int, prize_id: int):
    promo = get_promo(db, promo_id)
    if promo is None:
        raise RuntimeError(f"Promo action with id {prize_id} doesn't exist")
    for prize in promo.participants:
        if prize.id == prize_id:
            db.query(models.Prize)\
              .filter(models.Prize.promo_id == promo_id)\
              .filter(models.Prize.id == prize_id).delete()
            db.commit()
            return
    raise RuntimeError(
        f"Promo {promo_id} doesn't contain prize {prize_id}"
    )
