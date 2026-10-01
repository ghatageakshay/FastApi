from sqlalchemy import String
from sqlalchemy.orm import mapped_column,Mapped

from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    middle_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))

    age:Mapped[int]
    email: Mapped[str] = mapped_column(String(150),unique=True)

    weight:Mapped[float]
    height:Mapped[float]

    