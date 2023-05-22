"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатие на кнопку
"""

from PySide6 import QtWidgets, QtGui

from a_threads import WeatherHandler


class WeatherInfoWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__hasСreatedThreadWH = False
        self.__cities = {
            'Амстердам': (52.37, 4.89),
            'Андорра-ла-Велья': (42.51, 1.52),
            'Анкара': (39.92, 32.85),
            'Афины': (37.98, 23.73),
            'Баку': (40.38, 49.89),
            'Белград': (44.80, 20.47),
            'Берлин': (52.52, 13.41),
            'Берн': (46.95, 7.45),
            'Братислава': (48.15, 17.11),
            'Брюссель': (50.85, 4.35),
            'Будапешт': (47.50, 19.04),
            'Бухарест': (44.43, 26.11),
            'Вадуц': (47.14, 9.52),
            'Валлетта': (35.90, 14.51),
            'Варшава': (52.23, 21.01),
            'Ватикан': (41.90, 12.45),
            'Вена': (48.21, 16.37),
            'Вильнюс': (54.69, 25.28),
            'Дублин': (53.33, -6.25),
            'Ереван': (40.18, 44.51),
            'Загреб': (45.81, 15.98),
            'Киев': (50.45, 30.52),
            'Кишинев': (47.01, 28.86),
            'Копенгаген': (55.68, 12.57),
            'Лиссабон': (38.72, -9.13),
            'Лондон': (51.51, -0.13),
            'Любляна': (46.05, 14.51),
            'Люксембург': (49.61, 6.13),
            'Мадрид': (40.42, -3.70),
            'Минск': (53.90, 27.57),
            'Монако': (43.73, 7.42),
            'Москва': (55.75, 37.62),
            'Никосия': (35.18, 33.36),
            'Осло': (59.91, 10.75),
            'Париж': (48.85, 2.35),
            'Подгорица': (42.44, 19.26),
            'Прага': (50.09, 14.42),
            'Рейкьявик': (64.14, -21.90),
            'Рига': (56.95, 24.11),
            'Рим': (41.89, 12.51),
            'Санкт-Петербург': (59.94, 30.31),
            'Сан-Марино': (43.94, 12.45),
            'Сараево': (43.85, 18.36),
            'Скопье': (42.00, 21.43),
            'София': (42.70, 23.32),
            'Стокгольм': (59.33, 18.06),
            'Таллинн': (59.44, 24.75),
            'Тбилиси': (41.69, 44.83),
            'Тирана': (41.33, 19.82),
            'Хельсинки': (60.17, 24.94)
        }

        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация интерфейса
        :return: None
        """

        # window -------------------------------------------------------------
        self.setWindowTitle("Погода")
        # self.setMinimumSize(320, 220)
        # self.setMaximumSize(320, 220)

        # comboBoxCities -----------------------------------------------------
        self.comboBoxCities = QtWidgets.QComboBox()
        self.comboBoxCities.addItems(self.__cities.keys())
        self.comboBoxCities.insertItem(0, "")
        self.comboBoxCities.setCurrentIndex(0)

        # dblSBoxLatitude ----------------------------------------------------
        labelDblSBoxLatitude = QtWidgets.QLabel("Широта:")
        labelDblSBoxLatitude.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred
        )
        # порядок политик в setSizePolicy: horizontalPolicy, verticalPolicy)

        self.dblSBoxLatitude = QtWidgets.QDoubleSpinBox()
        self.dblSBoxLatitude.setMinimumSize(70, 0)
        self.dblSBoxLatitude.setMinimum(-90.0)
        self.dblSBoxLatitude.setMaximum(90.0)
        self.dblSBoxLatitude.setSuffix(' °')

        # dblSBoxLongitude ---------------------------------------------------
        labelDblSBoxLongitude = QtWidgets.QLabel("Долгота:")
        labelDblSBoxLongitude.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred
        )

        self.dblSBoxLongitude = QtWidgets.QDoubleSpinBox()
        self.dblSBoxLongitude.setMinimumSize(70, 0)
        self.dblSBoxLongitude.setMinimum(-180.0)
        self.dblSBoxLongitude.setMaximum(180.0)
        self.dblSBoxLongitude.setSuffix(' °')

        # layoutDblSBoxLatLon ------------------------------------------------
        layoutDblSBoxLatLon = QtWidgets.QHBoxLayout()
        layoutDblSBoxLatLon.addWidget(labelDblSBoxLatitude)
        layoutDblSBoxLatLon.addWidget(self.dblSBoxLatitude)
        layoutDblSBoxLatLon.addWidget(labelDblSBoxLongitude)
        layoutDblSBoxLatLon.addWidget(self.dblSBoxLongitude)

        # spinBoxDelay -------------------------------------------------------
        labelSpinBoxDelay = QtWidgets.QLabel("Пауза после получения данных о погоде:")
        labelSpinBoxDelay.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred
        )
        self.spinBoxDelay = QtWidgets.QSpinBox()
        self.spinBoxDelay.setMinimumSize(60, 0)
        self.spinBoxDelay.setSuffix(' сек')
        self.spinBoxDelay.setMinimum(1)
        self.spinBoxDelay.setValue(5)

        # layuotSpinBoxDelay -------------------------------------------------
        layoutSpinBoxDelay = QtWidgets.QHBoxLayout()
        layoutSpinBoxDelay.addWidget(labelSpinBoxDelay)
        layoutSpinBoxDelay.addWidget(self.spinBoxDelay)

        # plainTEWeather -----------------------------------------------------
        self.plainTEWeather = QtWidgets.QPlainTextEdit()
        self.plainTEWeather.setReadOnly(True)

        # pushButtonThreadHandler --------------------------------------------------
        self.pushButtonThreadHandler = QtWidgets.QPushButton("Получать данные")
        self.pushButtonThreadHandler.setCheckable(True)

        # layoutMain ---------------------------------------------------------
        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addWidget(self.comboBoxCities)
        layoutMain.addLayout(layoutDblSBoxLatLon)
        layoutMain.addLayout(layoutSpinBoxDelay)
        layoutMain.addWidget(self.plainTEWeather)
        layoutMain.addWidget(self.pushButtonThreadHandler)

        self.setLayout(layoutMain)

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """

        self.comboBoxCities.currentTextChanged.connect(self.comboBoxCitiesChanged)
        self.pushButtonThreadHandler.clicked.connect(self.threadHandler)

    # slots --------------------------------------------------------------
    def comboBoxCitiesChanged(self, text) -> None:
        """
        Обработка сигнала выбора значения в comboBoxCities
        :param text: получаемый из comboBoxCities текст текущего варианта выбора
        :return: None
        """

        if text:
            self.dblSBoxLatitude.setEnabled(False)
            self.dblSBoxLongitude.setEnabled(False)
            self.dblSBoxLatitude.setValue(self.__cities[text][0])
            self.dblSBoxLongitude.setValue(self.__cities[text][1])
        else:
            self.dblSBoxLatitude.setEnabled(True)
            self.dblSBoxLongitude.setEnabled(True)
            self.dblSBoxLatitude.setValue(0.0)
            self.dblSBoxLongitude.setValue(0.0)

    def threadHandler(self, buttonStatus) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonThreadHandler
        :return: None
        """

        if buttonStatus:
            self.pushButtonThreadHandler.setText("Остановить получение")
            self.threadWH = WeatherHandler(self.dblSBoxLatitude.value(), self.dblSBoxLongitude.value())
            self.threadWH.delay = self.spinBoxDelay.value()
            self.threadWH.status = True
            self.threadWH.start()
            self.__hasСreatedThreadWH = True
            self.comboBoxCities.setEnabled(False)
            self.dblSBoxLatitude.setEnabled(False)
            self.dblSBoxLongitude.setEnabled(False)
            self.spinBoxDelay.setEnabled(False)
            self.threadWH.weatherResponsed.connect(self.reportWeatherInfo)
        else:
            self.threadWH.status = False
            self.threadWH.finished.connect(self.threadWH.deleteLater)
            self.__hasСreatedThreadWH = False
            self.comboBoxCities.setEnabled(True)
            if not self.comboBoxCities.currentText():
                self.dblSBoxLatitude.setEnabled(True)
                self.dblSBoxLongitude.setEnabled(True)
            self.spinBoxDelay.setEnabled(True)
            self.pushButtonThreadHandler.setText("Получать данные")

        # self.threadWH.started.connect(lambda: self.comboBoxCities.setEnabled(False))
        # self.threadWH.finished.connect(lambda: self.comboBoxCities.setEnabled(True))
        # блок с setEnabled группе виджетов через сигнал finished потока работает медленнее

    def reportWeatherInfo(self, data: dict):
        """
        Приём данных из потока и обработка их в основном цикле приложения
        :param data: информация о погоде в указанных координатах
        :return: None
        """

        if len(data) == 1:
            self.plainTEWeather.setStyleSheet('color: red')
            self.plainTEWeather.setPlainText(data['Ошибка'])
        else:
            self.plainTEWeather.clear()
            self.plainTEWeather.setStyleSheet('color: black')
            self.plainTEWeather.appendPlainText(f"Температура воздуха: {data['current_weather']['temperature']} °C")
            self.plainTEWeather.appendPlainText(f"Скорость ветра: {data['current_weather']['windspeed']} км/ч")
            self.plainTEWeather.appendPlainText(f"Направление ветра: {data['current_weather']['winddirection']} °")

            match data['current_weather']['weathercode']:
                case 0:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Безоблачно")
                case 1:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Преимущественно ясно")
                case 2:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Переменная облачность")
                case 3:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Пасмурно")
                case 45:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Туман")
                case 48:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Туман с инеем в ночные часы")
                case 51:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Морось слабой интенсивности")
                case 53:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Морось умеренной интенсивности")
                case 55:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Морось интенсивная")
                case 56:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Ледяная морось слабой интенсивности")
                case 57:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Ледяная морось интенсивная")
                case 61:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Дождь слабой интенсивности")
                case 63:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Дождь умеренной интенсивности")
                case 65:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Дождь интенсивный")
                case 66:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Ледяной дождь слабой интенсивности")
                case 67:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Ледяной дождь интенсивный")
                case 71:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Снег слабой интенсивности")
                case 73:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Снег умеренной интенсивности")
                case 75:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Снег интенсивный")
                case 77:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Снежные зерна")
                case 80:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Ливень слабой интенсивности")
                case 81:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Ливень умеренной интенсивности")
                case 82:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Ливень интенсивный")
                case 85:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Снегопад слабой интенсивности")
                case 86:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Снегопад интенсивный")
                case 95:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Гроза")
                case 96:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Гроза со слабым градом")
                case 99:
                    self.plainTEWeather.appendPlainText("Состояние погоды: Гроза с сильным градом")
                case _:
                    self.plainTEWeather.appendPlainText(f"Состояние погоды: {data['current_weather']['weathercode']}")

            if data['current_weather']['is_day']:
                self.plainTEWeather.appendPlainText("Время суток: дневное")
            else:
                self.plainTEWeather.appendPlainText("Время суток: ночное")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Событие закрытия окна
        :param event: QtGui.QCloseEvent
        :return: None
        """

        if self.__hasСreatedThreadWH:
            self.threadWH.status = False
            self.threadWH.wait(deadline=(self.threadWH.delay * 1000))
            self.threadWH.finished.connect(self.threadWH.deleteLater)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = WeatherInfoWidget()
    window.show()

    app.exec()