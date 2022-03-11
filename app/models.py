from sqlalchemy import Column, ForeignKey, Integer, String, Identity
from sqlalchemy.orm import relationship

from .database import Base


class Prize(Base):
    __tablename__ = "prizes"

    id = Column(Integer, Identity(start=1), primary_key=True, index=True)
    name = Column(String)
    promo_id = Column(Integer, ForeignKey("promos.id", ondelete="CASCADE"))


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, Identity(start=1), primary_key=True, index=True)
    name = Column(String)
    promo_id = Column(Integer, ForeignKey("promos.id", ondelete="CASCADE"))


class PromoAction(Base):
    __tablename__ = "promos"

    id = Column(Integer, Identity(start=1), primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)

    participants = relationship("Participant", backref="promos")
    prizes = relationship("Prize", backref="promos")
