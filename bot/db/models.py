from datetime import date, datetime, time

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Sxema scraper/manba_yigish.py dagi SXEMA konstantasi bilan bir xil
# bo'lishi shart — ustun nomlari va turlari mos kelmasa scraper yozgan
# qatorlarni ORM o'qiy olmaydi.


class Base(DeclarativeBase):
    pass


class Shahar(Base):
    __tablename__ = "shaharlar"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String, unique=True)
    nom: Mapped[str] = mapped_column(String)
    viloyat: Mapped[str | None] = mapped_column(String, nullable=True)
    lat: Mapped[float | None] = mapped_column(nullable=True)
    lon: Mapped[float | None] = mapped_column(nullable=True)

    vaqtlar: Mapped[list["NamozVaqti"]] = relationship(back_populates="shahar")


class NamozVaqti(Base):
    __tablename__ = "namoz_vaqtlari"
    __table_args__ = (UniqueConstraint("shahar_id", "sana"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    shahar_id: Mapped[int] = mapped_column(ForeignKey("shaharlar.id", ondelete="CASCADE"))
    sana: Mapped[date] = mapped_column(Date)
    bomdod: Mapped[time] = mapped_column(Time)
    quyosh: Mapped[time] = mapped_column(Time)
    peshin: Mapped[time] = mapped_column(Time)
    asr: Mapped[time] = mapped_column(Time)
    shom: Mapped[time] = mapped_column(Time)
    xufton: Mapped[time] = mapped_column(Time)
    qamar_kuni: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    manba: Mapped[str] = mapped_column(String, default="namozvaqti.uz")
    olingan: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    shahar: Mapped[Shahar] = relationship(back_populates="vaqtlar")


class Foydalanuvchi(Base):
    __tablename__ = "foydalanuvchilar"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    shahar_id: Mapped[int | None] = mapped_column(ForeignKey("shaharlar.id"), nullable=True)
    maqsad: Mapped[str | None] = mapped_column(String, nullable=True)  # organish|vaqt_organish|vaqt|erkin
    daraja: Mapped[str] = mapped_column(String, default="boshlangich")  # boshlangich|orta|murakkab
    yaratilgan: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # 3-bosqich: bildirishnoma sozlamalari. Standart — kuniga 1 ta eslatma (Bomdod, 10 daqiqa oldin).
    eslatma_yoqilgan: Mapped[bool] = mapped_column(Boolean, default=True)
    eslatma_namozlar: Mapped[str] = mapped_column(String, default="bomdod")  # vergul bilan: "bomdod,peshin"
    eslatma_daqiqa: Mapped[int] = mapped_column(SmallInteger, default=10)

    # Vaqt tugashidan oldin ("qazo qilib qo'ymang") ogohlantirishi — standart o'chirilgan.
    eslatma_tugash_yoqilgan: Mapped[bool] = mapped_column(Boolean, default=False)
    eslatma_tugash_daqiqa: Mapped[int] = mapped_column(SmallInteger, default=15)

    shahar: Mapped[Shahar | None] = relationship()


class Sura(Base):
    __tablename__ = "suralar"

    raqam: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    nom_uz: Mapped[str] = mapped_column(String)
    nom_ar: Mapped[str] = mapped_column(String)
    oyat_soni: Mapped[int] = mapped_column(SmallInteger)
    daraja: Mapped[str] = mapped_column(String)  # boshlangich | orta | murakkab
    maqom: Mapped[str | None] = mapped_column(String, nullable=True)  # makka | madina
    matn: Mapped[list | None] = mapped_column(JSONB, nullable=True)  # [{oyat, arab, talaffuz}]
    manba: Mapped[str | None] = mapped_column(String, nullable=True)
    tasdiqlangan: Mapped[bool] = mapped_column(Boolean, default=False)
