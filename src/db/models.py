from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, JSON, Text, Float, Table, Column, Date, ForeignKey, func, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from typing import Optional
import uuid
from datetime import date, datetime
from src.db.base import Base
import enum


class User(Base):

    __tablename__ = 'users'


    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    surname: Mapped[str] = mapped_column(String(255))

    email: Mapped[str] = mapped_column(String, unique=True)
    #потом изменить
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    tel_number: Mapped[str] = mapped_column(String)

    password_hash: Mapped[str] = mapped_column(String)
    wallet_address: Mapped[str] = mapped_column(String, nullable=False)

    additional_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    talent_profile: Mapped[Optional['Talent']] = relationship(
                                                        back_populates='user',
                                                        uselist=False,
                                                        cascade='all, delete-orphan') 
    

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    

class Talent(Base):

    __tablename__ = 'talents'

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), index=True,
                                               primary_key=True)
    
    nickname: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=False)

    portfolio_links: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
    project_price: Mapped[float] = mapped_column(Float, nullable=False)
    
    role: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped["User"] = relationship(back_populates="talent_profile")

    managed_team_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey('teams.id'), nullable=True)
    managed_team: Mapped[Optional["Team"]] = relationship(
        "Team",
        back_populates='manager',
        foreign_keys=[managed_team_id]  
    )

    current_team_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey('teams.id'), nullable=True)
    current_team: Mapped[Optional["Team"]] = relationship(
        "Team",
        back_populates='current_members',
        foreign_keys=[current_team_id]
    )





#ENUMS

class League(str, enum.Enum):
    STARTER = 'Starter League'
    FIRST = 'First Division'
    PREMIER = 'Premier League'

class TeamStatus(str, enum.Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

class MembershipRole(str, enum.Enum):
    MANAGER = 'Manager'
    MEMBER = 'Member'

class MembershipStatus(str, enum.Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'


class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    speed: Mapped[int] = mapped_column(Integer, default=50)
    creativity: Mapped[int] = mapped_column(Integer, default=50)
    reliability: Mapped[int] = mapped_column(Integer, default=50)
    chemistry: Mapped[int] = mapped_column(Integer, default=0)

    manager: Mapped["Talent"] = relationship(
        "Talent",
        back_populates="managed_team",
        foreign_keys=[Talent.managed_team_id]
    )

    league: Mapped[League] = mapped_column(Enum(League, native_enum=False), nullable=False, default=League.STARTER)
    status: Mapped[TeamStatus] = mapped_column(Enum(TeamStatus, native_enum=False), nullable=False, default=TeamStatus.ACTIVE)

    current_members: Mapped[list["Talent"]] = relationship(
        "Talent",
        back_populates="current_team",
        foreign_keys=[Talent.current_team_id]
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

 