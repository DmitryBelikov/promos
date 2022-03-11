from typing import Optional

from pydantic import BaseModel


class PrizeBase(BaseModel):
    name: str


class PrizeCreate(PrizeBase):
    class Config:
        orm_mode = True


class Prize(PrizeBase):
    id: int

    class Config:
        orm_mode = True


class ParticipantBase(BaseModel):
    name: str


class ParticipantCreate(ParticipantBase):
    class Config:
        orm_mode = True


class Participant(ParticipantBase):
    id: int

    class Config:
        orm_mode = True


class PromoActionBase(BaseModel):
    name: str
    description: Optional[str] = None


class PromoActionCreate(PromoActionBase):
    class Config:
        orm_mode = True


class PromoActionSimple(PromoActionBase):
    id: int

    class Config:
        orm_mode = True


class PromoAction(PromoActionSimple):
    participants: list[Participant] = []
    prizes: list[Prize] = []

    class Config:
        orm_mode = True


class RaffleResult(BaseModel):
    winner: Participant
    prize: Prize
