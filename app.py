import asyncio
from src.database import PostgreSQLController
from src.parser import Parser
from sqlalchemy import select, desc
from src.models import WeatherData
from sqlalchemy.ext.asyncio import AsyncSession
from src.exporter import Exporter
from src import config
import aioconsole


class Application:
    def __init__(self) -> None:
        self.tasks: list[asyncio.Task] = []

    async def api_requests(self):
        """
        Цикл с бесконечным запросом данных через таймаут.
        """
        print("Started api requests with timeout: ", config.PARSE_GAP_SECONDS)
        while True:
            parser = Parser()
            controller = PostgreSQLController()

            data = await parser.get_current_weather()

            async with controller() as session:
                session: AsyncSession
                session.add(data)
                await session.commit()
            print("Saved data")
            await asyncio.sleep(config.PARSE_GAP_SECONDS)

    async def _api_requests_batch(self):
        while True:
            parser = Parser()
            controller = PostgreSQLController()

            data = await parser.get_hourly_weather()

            async with controller() as session:
                session: AsyncSession
                session.add_all(data)
                await session.commit()
            print("Saved many data")
            await asyncio.sleep(config.PARSE_GAP_SECONDS)

    async def export_data(self):
        controller = PostgreSQLController()
        exporter = Exporter()

        async with controller() as session:
            session: AsyncSession

            results = list(
                (
                    await session.execute(
                        select(WeatherData).limit(10).order_by(desc(WeatherData.time))
                    )
                )
                .scalars()
                .all()
            )

        await exporter.export(results)

    async def handle_control(self):
        """
        Цикл для получения элементарных команд с консоли.
        """
        while True:
            key = await aioconsole.ainput()
            match key.lower():
                case "q":
                    for task in self.tasks:
                        task.cancel()
                case "e":
                    print("Exporting data")
                    await self.export_data()

    async def run(self):
        """
        Запускает выполнение скрипта.

        gather позволяет запускать задачи 'в фоне', таким образом они работают параллельно, не ожидая синхронного получения результата от каждой задачи.
        """
        self.tasks.append(asyncio.create_task(self.api_requests()))
        self.tasks.append(asyncio.create_task(self.handle_control()))

        try:
            await asyncio.gather(*self.tasks)
        except asyncio.CancelledError:
            pass

        print("Application closed")
        quit(0)

    @classmethod
    async def init():
        """Метод для первичной инициализации базы данных"""
        controller = PostgreSQLController()
        await controller.init_db()


if __name__ == "__main__":
    """
    По заданию функции должны работать асинхронно,
    что не дает полной параллельности в ее понимании на уровне операционной системы,
    но такой способ и не блокирует интерпретатор.
    """
    app = Application()
    asyncio.run(app.run())
