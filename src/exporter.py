import xlsxwriter
from xlsxwriter.workbook import Worksheet, Workbook
from src.models import WeatherData
import datetime


class Exporter:
    """
    Класс для экспорта данных.
    """

    async def export(self, data: list[WeatherData]):
        """
        Экспорт данных в формат xlsx. Тут следует убедиться, что у пользователя есть права на создание файлов.
        """
        worksheet, workbook = await self.__create_file_n_worksheet()
        weather = [item.dump() for item in data]
        worksheet = await self.__make_headers(worksheet, list(weather[0].keys()))
        row = 2
        for item in weather:
            col = 0
            for value in list(item.values()):
                worksheet.write(row, col, value)
                col += 1
            row += 1
        workbook.close()

    async def __make_headers(self, worksheet: Worksheet, keys: list[str]) -> Worksheet:
        for i in range(len(keys)):
            worksheet.write_string(1, i, keys[i])

        return worksheet

    async def __create_file_n_worksheet(self) -> tuple[Worksheet, Workbook]:
        filename = (
            "./"
            + datetime.datetime.now(datetime.timezone.utc).strftime(
                "%d-%m-%Y, %H:%M:%S"
            )
            + " - Database dump.xlsx"
        )
        with open(filename, "w+") as f:
            f.close()
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet("Данные о погоде")
        return worksheet, workbook
