from src.database import Base
from src.tools import get_dt, get_uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Float


class WeatherData(Base):
    __tablename__ = "weather_data"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=get_uuid)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(True), default=get_dt, nullable=False
    )

    time: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    temperature_celsium: Mapped[float] = mapped_column(Float(1), nullable=False)
    wind_direction: Mapped[str] = mapped_column(String(2), nullable=False)
    wind_speed_mps: Mapped[float] = mapped_column(Float(1), nullable=False)
    air_pressure: Mapped[float] = mapped_column(Float(2), nullable=False)
    rain: Mapped[float] = mapped_column(Float(1), nullable=False)
    showers: Mapped[float] = mapped_column(Float(1), nullable=False)
    snowfall: Mapped[float] = mapped_column(Float(1), nullable=False)

    def dump(self) -> dict:
        return {
            "Время": self.time.replace(tzinfo=None).strftime("%d/%m/%Y, %H:%M:%S"),
            "Температура воздуха": round(self.temperature_celsium, 2),
            "Направление ветра": self.wind_direction,
            "Скорость ветра": round(self.wind_speed_mps, 2),
            "Давление": round(self.air_pressure, 2),
            "Осадки (дождь)": self.rain,
            "Осадки (ливни)": self.showers,
            "Осадки (снег)": self.snowfall,
        }
