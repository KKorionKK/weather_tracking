import aiohttp
import aiohttp.client_exceptions


from src.models import WeatherData
import datetime


class Parser:
    """
    Парсер данных. Имеет два публичных метода:
     - get_current_weather: возвращает модель текущей погоды
     - get_hourly_weather: возвращает модели почасового прогноза

    Запросы не обернуты в try, так как, скорее всего, проблема которая возникнет - будет с интернетом, и дальше программе работать нет смысла.
    """

    BASE_CURRENT = "https://api.open-meteo.com/v1/forecast?latitude=55.698520&longitude=37.359490&current=temperature_2m,rain,showers,snowfall,surface_pressure,wind_speed_10m,wind_direction_10m&wind_speed_unit=ms&timeformat=unixtime"
    BASE_HOURLY = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,rain,showers,snowfall,surface_pressure,wind_speed_10m,wind_direction_10m&wind_speed_unit=ms&timeformat=unixtime"

    async def get_current_weather(self) -> WeatherData:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_CURRENT) as response:
                if response.status != 200:
                    raise Exception(
                        f"The response status is: {response.status}. Check data provider."
                    )
                current_data = (await response.json()).get("current")

        model = await self.__get_variables(current_data)

        return model

    async def get_hourly_weather(self) -> list[WeatherData]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_HOURLY) as response:
                if response.status != 200:
                    raise Exception(
                        f"The response status is: {response.status}. Check data provider."
                    )
                data = (await response.json()).get("hourly")

        models = await self.__get_many_variables(data)

        return models

    async def __get_many_variables(self, data: dict) -> list[WeatherData]:
        """
        Парсит данные с JSON объекта во внутреннюю модель.
        """
        weather: list[WeatherData] = []
        for i in range(len(data["time"])):
            weather.append(
                WeatherData(
                    time=await self.__parse_time(data.get("time")[i]),
                    temperature_celsium=data.get("temperature_2m")[i],
                    wind_direction=await self.__get_wind_direction(
                        data.get("wind_direction_10m")[i]
                    ),
                    wind_speed_mps=data.get("wind_speed_10m")[i],
                    air_pressure=data.get("surface_pressure")[i],
                    rain=data.get("rain")[i],
                    showers=data.get("showers")[i],
                    snowfall=data.get("snowfall")[i],
                )
            )
        return weather

    async def __get_variables(self, current: dict) -> WeatherData:
        return WeatherData(
            time=await self.__parse_time(current.get("time")),
            temperature_celsium=current.get("temperature_2m"),
            wind_direction=await self.__get_wind_direction(
                current.get("wind_direction_10m")
            ),
            wind_speed_mps=current.get("wind_speed_10m"),
            air_pressure=current.get("surface_pressure"),
            rain=current.get("rain"),
            showers=current.get("showers"),
            snowfall=current.get("snowfall"),
        )

    async def __parse_time(self, time: int) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(float(time), datetime.timezone.utc)

    async def __get_wind_direction(self, deg: float) -> str:
        directions = ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]
        index = round(deg / (360.0 / len(directions))) % len(directions)
        return directions[index]
