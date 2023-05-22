"""
Модуль в котором содержаться потоки Qt
"""

import time

import psutil

import requests

from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)  # Создайте экземпляр класса Signal и передайте ему в конструктор тип данных передаваемого значения (в текущем случае list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__delay = None  # создайте атрибут класса self.delay = None, для управлением задержкой получения данных
        self.__status = None

    @property
    def status(self) -> bool:
        """
        Свойство-геттер для определения готовности потока для получения информации о системе
        :return: True или False
        """
        return self.__status

    @status.setter
    def status(self, value: bool) -> None:
        """
        Свойство-сеттер для изменения готовности потока для получения информации о системе
        :param value: True или False
        :return: None
        """
        if not isinstance(value, bool):
            raise TypeError("Значение status должно быть типа bool!")
        self.__status = value

    @property
    def delay(self) -> int:
        """
        Свойство-геттер для получения текущего времени задержки до получения информации о системе
        :return: текущее значение задержки в секундах
        """
        return self.__delay

    @delay.setter
    def delay(self, value: int) -> None:
        """
        Свойство-сеттер для установки времени задержки до получения информации о системе
        :param value: новое значение задержки в секундах
        :return: None
        """
        if not isinstance(value, int):
            raise TypeError("Значение delay должно быть типа int!")
        if value < 0:
            raise ValueError("Значение delay должно быть больше или равно 0!")
        self.__delay = value

    def run(self) -> None:  # переопределить метод run
        if self.__delay is None:  # Если задержка не передана в поток перед его запуском
            self.__delay = 1  # то устанавливайте значение 1

        while self.__status:  # Запустите бесконечный цикл получения информации о системе
            cpu_value = psutil.cpu_percent()  # с помощью вызова функции cpu_percent() в пакете psutil получите загрузку CPU
            ram_value = psutil.virtual_memory().percent  # с помощью вызова функции virtual_memory().percent в пакете psutil получите загрузку RAM
            self.systemInfoReceived.emit([cpu_value, ram_value])  # с помощью метода .emit передайте в виде списка данные о загрузке CPU и RAM
            time.sleep(self.__delay)  # с помощью функции .sleep() приостановите выполнение цикла на время self.delay


class WeatherHandler(QtCore.QThread):
    weatherResponsed = QtCore.Signal(dict)  # Пропишите сигналы, которые считаете нужными

    def __init__(self, lat: float, lon: float, parent=None):
        super().__init__(parent)

        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = 10
        self.__status = None

    @property
    def status(self) -> bool:
        """
        Свойство-геттер для определения готовности потока для подключения к сайту погоды
        :return: True или False
        """
        return self.__status

    @status.setter
    def status(self, value: bool) -> None:
        """
        Свойство-сеттер для изменения готовности потока для подключения к сайту погоды
        :param value: True или False
        :return: None
        """
        if not isinstance(value, bool):
            raise TypeError("Значение status должно быть типа bool!")
        self.__status = value

    @property
    def delay(self) -> int:
        """
        Свойство-геттер для получения текущего времени задержки до обновления сайта
        :return: текущее значение задержки в секундах
        """
        return self.__delay

    @delay.setter
    def delay(self, value: int) -> None:
        """
        Свойство-сеттер для установки времени задержки до обновления сайта
        :param value: новое значение задержки в секундах
        :return: None
        """
        if not isinstance(value, int):
            raise TypeError("Значение delay должно быть типа int!")
        if value < 1:
            raise ValueError("Значение delay должно быть больше или равно 1!")
        self.__delay = value

    def run(self) -> None:
        # настройте метод для корректной работы

        while self.__status:
            try:
                response = requests.get(self.__api_url)
            except requests.exceptions.ConnectionError:  # if response.status_code != 200:
                self.weatherResponsed.emit({'Ошибка': 'Проверьте наличие подключения к сети Интернет!'})
                time.sleep(1)
            else:
                data = response.json()
                self.weatherResponsed.emit(data)
                time.sleep(self.__delay)
