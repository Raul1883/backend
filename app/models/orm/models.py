from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    Text,
    UniqueConstraint,
    JSON,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_pwd: Mapped[str] = mapped_column(String)
    contact_info: Mapped[str | None] = mapped_column(String, nullable=True)
    roles: Mapped[str] = mapped_column(String)
    # example: "player,master"

    characters: Mapped[list["Character"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    mastered_sessions: Mapped[list["Session"]] = relationship(
        back_populates="master",
    )

    applications: Mapped[list["Application"]] = relationship(
        back_populates="user",
    )


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="company",
    )

    characters: Mapped[list["Character"]] = relationship(
        back_populates="company",
    )


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, unique=True)

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="genre",
    )


class System(Base):
    __tablename__ = "systems"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, unique=True)

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="system",
    )


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    scheduled_at: Mapped[str] = mapped_column(String, nullable=True)

    master_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    system_id: Mapped[int] = mapped_column(ForeignKey("systems.id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))

    company_id: Mapped[int | None] = mapped_column(
        ForeignKey("companies.id"),
        nullable=True,  # oneshot
    )

    master: Mapped["User"] = relationship(
        back_populates="mastered_sessions",
    )

    company: Mapped["Company | None"] = relationship(
        back_populates="sessions",
    )

    system: Mapped["System"] = relationship(
        foreign_keys=[system_id],
        back_populates="sessions",
    )

    genre: Mapped["Genre"] = relationship(
        foreign_keys=[genre_id],
        back_populates="sessions",
    )

    applications: Mapped[list["Application"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("user_id", "session_id", name="uq_user_session"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))

    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String)
    # pending / approved / rejected

    user: Mapped["User"] = relationship(
        back_populates="applications",
    )

    session: Mapped["Session"] = relationship(
        back_populates="applications",
    )

    character: Mapped["Character"] = relationship()


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    company_id: Mapped[int | None] = mapped_column(
        ForeignKey("companies.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    data_fields: Mapped[dict] = mapped_column(JSON)

    owner: Mapped["User"] = relationship(
        back_populates="characters",
    )

    company: Mapped["Company | None"] = relationship(
        back_populates="characters",
    )
