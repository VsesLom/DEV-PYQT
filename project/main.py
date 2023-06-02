import os

import json

from PySide6 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__widgets = ("Календарь", "Список")

        self.initData()
        self.initUi()
        self.initSignals()

    def initData(self) -> None:
        """
        Инициализация данных
        :return: None
        """

        self.__catalog = {}
        self.__shedule = {}
        file_list = os.listdir()
        if 'catalog.json' in file_list:
            with open('catalog.json', 'r', encoding="utf-8") as f:
                self.__catalog = json.load(f)
        if 'shedule.json' in file_list:
            with open('shedule.json', 'r', encoding="utf-8") as f:
                self.__shedule = json.load(f)
            current_date = QtCore.QDate.currentDate()
            for date_str in self.__shedule.keys():
                date = QtCore.QDate().fromString(date_str, 'dd.MM.yyyy')
                if date < current_date:
                    if not self.__shedule[date_str].get('passed_date'):
                        for time in self.__shedule[date_str].keys():
                            for name in self.__shedule[date_str][time].keys():
                                self.__shedule[date_str][time][name]['color'] = '#707070'
                        self.__shedule[date_str].setdefault('passed_date', True)
                        with open('shedule.json', 'w', encoding="utf-8") as f:
                            json.dump(self.__shedule, f, ensure_ascii=False, indent=4)
                else:
                    break

    def initUi(self) -> None:
        """
        Инициализация Ui
        :return: None
        """

        # window -------------------------------------------------------------
        self.setWindowTitle("Менеджер лекарств")

        # treatmentCalendar --------------------------------------------------
        self.treatmentCalendar = TreatmentCalendar()
        self.treatmentCalendar.catalog = self.__catalog
        self.treatmentCalendar.shedule = self.__shedule
        self.treatmentCalendar.showDailyData(QtCore.QDate.currentDate())

        # treatmentList ------------------------------------------------------
        self.treatmentList = TreatmentList()
        self.treatmentList.catalog = self.__catalog
        self.treatmentList.shedule = self.__shedule
        self.treatmentList.showTreatmentList()

        # tabWidget ----------------------------------------------------------
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.addTab(self.treatmentCalendar, self.__widgets[0])
        self.tabWidget.addTab(self.treatmentList, self.__widgets[1])

        # layoutMain ---------------------------------------------------------
        layoutMain = QtWidgets.QHBoxLayout()
        layoutMain.addWidget(self.tabWidget)
        layoutMain.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layoutMain)

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """

        self.tabWidget.currentChanged.connect(self.currentTabIndexChanged)

    # slots --------------------------------------------------------------
    def currentTabIndexChanged(self, index: int) -> None:
        """
        Метод для обработки переключения вкладки в tabWidget
        :param index: индекс текущей вкладки
        :return: None
        """

        match self.__widgets[index]:
            case "Календарь":
                self.treatmentCalendar.showDailyData(self.treatmentCalendar.calendarWidget.selectedDate())
            case "Список":
                self.treatmentList.showTreatmentList(self.treatmentList.listWidget.currentRow())

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Событие закрытия основого окна приложения
        :param event: QtGui.QCloseEvent
        :return: None
        """

        answer = QtWidgets.QMessageBox.question(self, "Завершение работы",
                                                "Вы хотите сохранить внесенные изменения?")

        if answer == QtWidgets.QMessageBox.Yes:
            if self.treatmentCalendar.status or self.treatmentList.status:
                self.__catalog = dict(sorted(self.__catalog.items(), key=lambda x: x[0]))

            with open('catalog.json', 'w', encoding="utf-8") as f:
                json.dump(self.__catalog, f, ensure_ascii=False, indent=4)

            with open('shedule.json', 'w', encoding="utf-8") as f:
                json.dump(self.__shedule, f, ensure_ascii=False, indent=4)


class TreatmentCalendar(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__catalog = {}
        self.__shedule = {}
        self.__status = False

        self.initUi()
        self.initSignals()

    @property
    def status(self) -> bool:
        """
        Свойство-геттер для получения текущего статуса изменения данных
        :return: текущий статус изменения данных
        """
        return self.__status

    @property
    def catalog(self) -> dict:
        """
        Свойство-геттер для получения текущего словаря с перечнем лекарств
        :return: текущий словарь с перечнем лекарств
        """

        return self.__catalog

    @catalog.setter
    def catalog(self, value: dict) -> None:
        """
        Свойство-сеттер для изменения текущего словаря с перечнем лекарств
        :param value: новый словарь с перечнем лекарств
        :return: None
        """

        if not isinstance(value, dict):
            raise TypeError("Значение атрибута catalog должно быть типа dict!")
        self.__catalog = value

    @property
    def shedule(self) -> dict:
        """
        Свойство-геттер для получения текущего расписания приема лекарств
        :return: текущее расписание приема лекарств
        """

        return self.__shedule

    @shedule.setter
    def shedule(self, value: dict) -> None:
        """
        Свойство-сеттер для изменения текущего расписания приема лекарств
        :param value: новое расписание приема лекарств
        :return: None
        """

        if not isinstance(value, dict):
            raise TypeError("Значение атрибута shedule должно быть типа dict!")
        self.__shedule = value

    def initUi(self) -> None:
        """
        Инициализация Ui
        :return: None
        """

        # calendarWidget -----------------------------------------------------
        self.calendarWidget = QtWidgets.QCalendarWidget()
        self.calendarWidget.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

        # labelHeader --------------------------------------------------------
        self.labelHeader = QtWidgets.QLabel("Перечень лекарств на выбранную дату:")
        self.labelHeader.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # textEditData -------------------------------------------------------
        self.textEditData = QtWidgets.QTextEdit()
        self.textEditData.setReadOnly(True)

        # pushButtonAdd ------------------------------------------------------
        self.pushButtonAdd = QtWidgets.QPushButton("Добавить")

        # pushButtonClear ----------------------------------------------------
        self.pushButtonClear = QtWidgets.QPushButton("Очистить")

        # layoutButtons ------------------------------------------------------
        layoutButtons = QtWidgets.QHBoxLayout()
        layoutButtons.addWidget(self.pushButtonAdd)
        layoutButtons.addWidget(self.pushButtonClear)

        # layoutData ---------------------------------------------------------
        layoutData = QtWidgets.QVBoxLayout()
        layoutData.addWidget(self.labelHeader)
        layoutData.addWidget(self.textEditData)
        layoutData.addLayout(layoutButtons)

        # layoutMain ---------------------------------------------------------
        layoutMain = QtWidgets.QHBoxLayout()
        layoutMain.addWidget(self.calendarWidget)
        layoutMain.addLayout(layoutData)
        layoutMain.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layoutMain)

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """

        self.calendarWidget.activated.connect(self.activateDialog)
        self.calendarWidget.selectionChanged.connect(self.showDailyData)
        self.pushButtonAdd.clicked.connect(self.onPushButtonAddClicked)
        self.pushButtonClear.clicked.connect(self.onPushButtonClearClicked)

    # slots --------------------------------------------------------------
    def activateDialog(self, date: QtCore.QDate) -> None:
        """
        Метод для вызова диалогового окна с настройками записи при активации даты в calendarWidget
        :return: None
        """

        if date < QtCore.QDate.currentDate():
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Невозможно добавить лекарство на прошедшую дату!")
        else:
            self.calendarDialog = TreatmentDialog(date)
            self.calendarDialog.generated.connect(self.getData)
            self.calendarDialog.exec()

    def getData(self, data: tuple) -> None:
        """
        Метод для получения данных из диалоговго окна, вызванного активацией даты в calendarWidget
        :param data: набор данных из диалоговго окна
        :return: None
        """

        name_dose_unit = data[0] + ' ' + str(data[1]) + ' ' + data[2]
        if data[5]:
            date_stop = data[5].toString('dd.MM.yyyy')
        else:
            date_stop = data[5]
        d = {name_dose_unit: {'color': data[3], 'date_start': data[4].toString('dd.MM.yyyy'), 'date_stop': date_stop,
                              'interval': data[6], 'times': data[7]}}
        if not self.__catalog.get(name_dose_unit):
            self.__catalog.setdefault(name_dose_unit, d[name_dose_unit])
        else:
            self.__catalog[name_dose_unit] = d[name_dose_unit]  # перезаписывает существующий ключ!!!
        self.__status = True
        date = data[4]
        if not data[5] or data[5] > data[4].addDays(30):
            date_stop = data[4].addDays(30)
        else:
            date_stop = data[5]
        day = 0
        while not date > date_stop:
            date_str = date.toString('dd.MM.yyyy')
            for time in data[7]:
                d = {time: {name_dose_unit: {'color': data[3]}}}
                if not self.__shedule.get(date_str):
                    self.__shedule.setdefault(date_str, d)
                else:
                    if not self.__shedule[date_str].get(time):
                        self.__shedule[date_str].setdefault(time, d[time])
                    else:
                        self.__shedule[date_str][time].setdefault(name_dose_unit, d[time][name_dose_unit])
            day += 1 + data[6]
            date = data[4].addDays(day)
        for date in self.__shedule.keys():
            if not self.__shedule[date].get('passed_date'):
                d = dict(sorted(self.__shedule[date].items(), key=lambda x: x[0]))
                self.__shedule[date] = d
                for time in self.__shedule[date].keys():
                    d = dict(sorted(self.__shedule[date][time].items(), key=lambda x: x[0]))
                    self.__shedule[date][time] = d
        self.showDailyData(data[4])

    def showDailyData(self, date: QtCore.QDate = None) -> None:
        """
        Метод для вывода перечня лекарств на выбранную дату
        :return: None
        """

        self.textEditData.clear()
        if date:
            choosen_date = date.toString('dd.MM.yyyy')
        else:
            choosen_date = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        self.labelHeader.setText(f"Перечень лекарств на {choosen_date}:")
        if choosen_date in self.__shedule.keys():
            passed_date = self.__shedule[choosen_date].get('passed_date')
            for time in self.__shedule[choosen_date].keys():
                if time == 'passed_date':
                    continue
                for name in self.__shedule[choosen_date][time].keys():
                    self.textEditData.setTextBackgroundColor(self.__shedule[choosen_date][time][name]['color'])
                    if passed_date:
                        self.textEditData.setTextColor('#ffffff')
                    self.textEditData.append(f"В {time} - {name}")
        self.textEditData.setTextColor('#000000')
        self.textEditData.setTextBackgroundColor('#ffffff')

    def onPushButtonAddClicked(self) -> None:
        """
        Метод для вызова диалогового окна с настройками записи при нажатии кнопки pushButtonAdd
        :return: None
        """

        self.activateDialog(self.calendarWidget.selectedDate())

    def onPushButtonClearClicked(self) -> None:
        """
        Метод для удаления перечня лекарств на выбранную дату при нажатии кнопки pushButtonClear
        :return: None
        """

        answer = QtWidgets.QMessageBox.question(self, "Удаление данных",
                                                "Вы действительно хотите очистить\nвыбранную дату от перечня лекарств?")
        if answer == QtWidgets.QMessageBox.Yes:
            del_date = self.calendarWidget.selectedDate()
            if del_date < QtCore.QDate.currentDate():
                QtWidgets.QMessageBox.warning(self, "Предупреждение", "Редактирование прошедших дат невозможно!")
                return
            del_date = del_date.toString('dd.MM.yyyy')
            names_key = set()
            for time in self.__shedule[del_date].keys():
                names_key |= set(self.__shedule[del_date][time].keys())
            for name in names_key:
                if self.__catalog[name]['date_start'] == del_date:
                    new_date = QtCore.QDate().fromString(del_date, 'dd.MM.yyyy').addDays(1)
                    self.__catalog[name]['date_start'] = new_date.toString('dd.MM.yyyy')
                elif self.__catalog[name]['date_stop'] == del_date:
                    new_date = QtCore.QDate().fromString(del_date, 'dd.MM.yyyy').addDays(-1)
                    self.__catalog[name]['date_stop'] = new_date.toString('dd.MM.yyyy')
                if self.__catalog[name]['date_stop']:
                    if QtCore.QDate.fromString(self.__catalog[name]['date_start'],
                                               'dd.MM.yyyy') > QtCore.QDate.fromString(self.__catalog[name]['date_stop'],
                                                                                       'dd.MM.yyyy'):
                        self.__catalog.pop(name)
                        QtWidgets.QMessageBox.about(self, "Уведомление",
                                                    f"Лекарство {name} удалено\nиз списка принимаемых лекарств!")
                else:
                    if self.__catalog[name].get('excluded_dates'):
                        self.__catalog[name]['excluded_dates'].append(del_date)
                        self.__catalog[name]['excluded_dates'].sort()
                    else:
                        self.__catalog[name].setdefault('excluded_dates', [del_date])
            self.__shedule.pop(del_date)
            self.textEditData.clear()


class TreatmentList(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__catalog = {}
        self.__shedule = {}
        self.__status = False

        self.initUi()
        self.initSignals()

    @property
    def status(self) -> bool:
        """
        Свойство-геттер для получения текущего статуса изменения данных
        :return: текущий статус изменения данных
        """
        return self.__status

    @property
    def catalog(self) -> dict:
        """
        Свойство-геттер для получения текущего словаря с перечнем лекарств
        :return: текущий словарь с перечнем лекарств
        """

        return self.__catalog

    @catalog.setter
    def catalog(self, value: dict) -> None:
        """
        Свойство-сеттер для изменения текущего словаря с перечнем лекарств
        :param value: новый словарь с перечнем лекарств
        :return: None
        """

        if not isinstance(value, dict):
            raise TypeError("Значение атрибута catalog должно быть типа dict!")
        self.__catalog = value

    @property
    def shedule(self) -> dict:
        """
        Свойство-геттер для получения текущего расписания приема лекарств
        :return: текущее расписание приема лекарств
        """

        return self.__shedule

    @shedule.setter
    def shedule(self, value: dict) -> None:
        """
        Свойство-сеттер для изменения текущего расписания приема лекарств
        :param value: новое расписание приема лекарств
        :return: None
        """

        if not isinstance(value, dict):
            raise TypeError("Значение атрибута shedule должно быть типа dict!")
        self.__shedule = value

    def initUi(self) -> None:
        """
        Инициализация Ui
        :return: None
        """

        # labelList ----------------------------------------------------------
        labelList = QtWidgets.QLabel("Перечень принимаемых лекарств:")
        labelList.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # listWidget ---------------------------------------------------------
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setSortingEnabled(True)
        self.listWidget.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        # pushButtonAdd ------------------------------------------------------
        self.pushButtonAdd = QtWidgets.QPushButton("Добавить")

        # pushButtonDelete ---------------------------------------------------
        self.pushButtonDelete = QtWidgets.QPushButton("Удалить")

        # layoutButtons ------------------------------------------------------
        layoutButtons = QtWidgets.QHBoxLayout()
        layoutButtons.addWidget(self.pushButtonAdd)
        layoutButtons.addWidget(self.pushButtonDelete)

        # layoutList ---------------------------------------------------------
        layoutList = QtWidgets.QVBoxLayout()
        layoutList.addWidget(labelList)
        layoutList.addWidget(self.listWidget)
        layoutList.addLayout(layoutButtons)

        # labelData ----------------------------------------------------------
        labelData = QtWidgets.QLabel("Информация о лекарстве:")
        labelData.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # textEditData -------------------------------------------------------
        self.textEditData = QtWidgets.QTextEdit()
        self.textEditData.setEnabled(False)

        # layoutData ---------------------------------------------------------
        layoutData = QtWidgets.QVBoxLayout()
        layoutData.addWidget(labelData)
        layoutData.addWidget(self.textEditData)

        # layoutMain ---------------------------------------------------------
        layoutMain = QtWidgets.QHBoxLayout()
        layoutMain.addLayout(layoutList)
        layoutMain.addLayout(layoutData)
        layoutMain.setContentsMargins(2, 0, 0, 0)

        self.setLayout(layoutMain)

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """

        self.pushButtonAdd.clicked.connect(self.onPushButtonAddClicked)
        self.pushButtonDelete.clicked.connect(self.onPushButtonDeleteClicked)
        self.listWidget.currentRowChanged.connect(self.showDragData)

    # slots --------------------------------------------------------------
    def onPushButtonAddClicked(self) -> None:
        """
        Метод для вызова диалогового окна с настройками записи при нажатии кнопки pushButtonAdd
        :return: None
        """

        self.listDialog = TreatmentDialog()
        self.listDialog.generated.connect(self.getData)
        self.listDialog.exec()

    def onPushButtonDeleteClicked(self) -> None:
        """
        Метод для удаления лекарства из списка и расписания приема при нажатии кнопки pushButtonDelete
        :return: None
        """

        name = self.listWidget.currentItem().text()
        answer = QtWidgets.QMessageBox.question(
            self, "Удаление данных", f"Вы действительно хотите удалить {name}\nиз списка принимаемых лекарств?"
        )
        if answer == QtWidgets.QMessageBox.Yes:
            del_dict_time = {}
            for date in self.__shedule.keys():
                if not self.__shedule[date].get('passed_date'):
                    for time in self.__shedule[date].keys():
                        if self.__shedule[date][time].get(name):
                            self.__shedule[date][time].pop(name)
                            if not self.__shedule[date][time]:
                                if del_dict_time.get(date):
                                    del_dict_time[date].append(time)
                                else:
                                    del_dict_time.setdefault(date, [time])
            del_list_date = []
            for date in del_dict_time.keys():
                for time in del_dict_time[date]:
                    self.__shedule[date].pop(time)
                    if not self.__shedule[date]:
                        del_list_date.append(date)
            for date in del_list_date:
                self.__shedule.pop(date)
            self.__catalog.pop(name)
        self.showTreatmentList()

    def getData(self, data: tuple) -> None:
        """
        Метод для получения данных из диалоговго окна, вызванного нажатием на кнопки pushButtonAdd
        :param data: набор данных из диалоговго окна
        :return: None
        """

        name_dose_unit = data[0] + ' ' + str(data[1]) + ' ' + data[2]
        if data[5]:
            date_stop = data[5].toString('dd.MM.yyyy')
        else:
            date_stop = data[5]
        d = {name_dose_unit: {'color': data[3], 'date_start': data[4].toString('dd.MM.yyyy'), 'date_stop': date_stop,
                              'interval': data[6], 'times': data[7]}}
        if not self.__catalog.get(name_dose_unit):
            self.__catalog.setdefault(name_dose_unit, d[name_dose_unit])
        else:
            self.__catalog[name_dose_unit] = d[name_dose_unit]  # перезаписывает существующий ключ!!!
        self.__status = True
        date = data[4]
        if not data[5] or data[5] > data[4].addDays(30):
            date_stop = data[4].addDays(30)
        else:
            date_stop = data[5]
        day = 0
        while not date > date_stop:
            date_str = date.toString('dd.MM.yyyy')
            for time in data[7]:
                d = {time: {name_dose_unit: {'color': data[3]}}}
                if not self.__shedule.get(date_str):
                    self.__shedule.setdefault(date_str, d)
                else:
                    if not self.__shedule[date_str].get(time):
                        self.__shedule[date_str].setdefault(time, d[time])
                    else:
                        self.__shedule[date_str][time].setdefault(name_dose_unit, d[time][name_dose_unit])
            day += 1 + data[6]
            date = data[4].addDays(day)
        for date in self.__shedule.keys():
            if not self.__shedule[date].get('passed_date'):
                d = dict(sorted(self.__shedule[date].items(), key=lambda x: x[0]))
                self.__shedule[date] = d
                for time in self.__shedule[date].keys():
                    d = dict(sorted(self.__shedule[date][time].items(), key=lambda x: x[0]))
                    self.__shedule[date][time] = d
        self.showTreatmentList()

    def showTreatmentList(self, row: int = 0) -> None:
        """
        Метод для вывода списка принимаемых лекарств
        :return: None
        """

        self.listWidget.clear()
        self.listWidget.addItems(self.__catalog.keys())
        self.listWidget.setCurrentRow(row)

    def showDragData(self, row: int) -> None:
        """
        Метод для вывода информации о выбранном лекарстве
        :return: None
        """

        self.textEditData.clear()
        name = self.listWidget.item(row)
        if name:
            name = name.text()
            self.textEditData.append("Цвет маркера: ")
            self.textEditData.setTextColor(self.__catalog[name]['color'])
            self.textEditData.setTextBackgroundColor(self.__catalog[name]['color'])
            self.textEditData.insertPlainText('________')
            self.textEditData.setTextColor('#000000')
            self.textEditData.setTextBackgroundColor('#ffffff')
            self.textEditData.append(f"Начало курса: {self.__catalog[name]['date_start']}")
            if self.__catalog[name]['date_stop']:
                self.textEditData.append(f"Окончание курса: {self.__catalog[name]['date_stop']}")
            else:
                self.textEditData.append("Лекарство принимается на регулярной основе")
            if self.__catalog[name]['interval']:
                self.textEditData.append(f"Интервал между приемами (в днях): {self.__catalog[name]['interval']}")
            else:
                self.textEditData.append("Лекарство принимается ежедневно")
            self.textEditData.append("Время приема лекарства:")
            str_times = ''
            for time in self.__catalog[name]['times']:
                str_times += ' ' + time + ','
            self.textEditData.insertPlainText(str_times[:-1])
            if self.__catalog[name].get('excluded_dates'):
                self.textEditData.append("Даты перерывов в курсе приема лекарства:")
                str_dates = ''
                for date in self.__catalog[name]['excluded_dates']:
                    str_dates += ' ' + date + ','
                self.textEditData.insertPlainText(str_dates[:-1])


class TreatmentDialog(QtWidgets.QDialog):
    generated = QtCore.Signal(tuple)

    def __init__(self, date: QtCore.QDate = None, parent=None):
        super().__init__(parent)
        self.__names = (
            'Аспинат 300',
            'Аспирин Кардио',
            'Ацекардол',
            'Ацетилкардио-ЛекТ',
            'Ацетилсалициловая кислота Кардио',
            'Сановаск',
            'Таспир',
            'Тромбо АСС',
            'Тромбостен',
            'Эйфитол'
        )

        self.__color = QtGui.QColor('#000000')
        self.__date_start = date
        self.__date_stop = None
        self.__interval = 0
        self.__times = []

        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация Ui
        :return: None
        """

        # window -------------------------------------------------------------
        self.setWindowTitle("Добавление лекарства")

        # comboBoxDrugs ------------------------------------------------------
        self.comboBoxDrugs = QtWidgets.QComboBox()
        self.comboBoxDrugs.addItems(self.__names)
        self.comboBoxDrugs.setCurrentIndex(-1)
        self.comboBoxDrugs.setLineEdit(QtWidgets.QLineEdit())
        self.comboBoxDrugs.lineEdit().setPlaceholderText("Введите или выберите название")

        # dblSpinBoxDose -----------------------------------------------------
        labelDose = QtWidgets.QLabel("Дозировка")

        self.dblSpinBoxDose = QtWidgets.QDoubleSpinBox()
        self.dblSpinBoxDose.setDecimals(0)
        self.dblSpinBoxDose.setSuffix(' мг')

        # pushButtonColor ----------------------------------------------------
        labelColor = QtWidgets.QLabel("Цвет маркера:")

        self.pushButtonColor = QtWidgets.QPushButton()
        self.pushButtonColor.setStyleSheet(f"background-color: {self.__color.name()}")

        # layoutDoseColor ----------------------------------------------------
        layoutDoseColor = QtWidgets.QHBoxLayout()
        layoutDoseColor.addWidget(labelDose)
        layoutDoseColor.addWidget(self.dblSpinBoxDose)
        layoutDoseColor.addSpacerItem(QtWidgets.QSpacerItem(
            10, 5, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        )
        layoutDoseColor.addWidget(labelColor)
        layoutDoseColor.addWidget(self.pushButtonColor)

        # comboBoxPermanence -------------------------------------------------
        self.comboBoxPermanence = QtWidgets.QComboBox()
        self.comboBoxPermanence.addItems(('постоянно', 'курсом'))

        # comboBoxRegularity -------------------------------------------------
        self.comboBoxRegularity = QtWidgets.QComboBox()
        self.comboBoxRegularity.addItems(('ежедневно', 'через день', 'через интервал'))

        # spinBoxNumber ------------------------------------------------------
        self.spinBoxNumber = QtWidgets.QSpinBox()
        self.spinBoxNumber.setRange(1, 48)
        self.spinBoxNumber.setSuffix(" раз в день")

        # layoutPerRegNum ----------------------------------------------------
        layoutPerRegNum = QtWidgets.QHBoxLayout()
        layoutPerRegNum.addWidget(self.comboBoxPermanence)
        layoutPerRegNum.addWidget(self.comboBoxRegularity)
        layoutPerRegNum.addWidget(self.spinBoxNumber)

        # dateStart ----------------------------------------------------------
        labelDateStart = QtWidgets.QLabel("Начало")

        self.dateEditStart = QtWidgets.QDateEdit()
        if self.__date_start:
            self.dateEditStart.setDate(self.__date_start)
            self.dateEditStart.setEnabled(False)
            self.dateEditStart.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        else:
            self.dateEditStart.setMinimumDate(QtCore.QDate.currentDate())

        # layoutDateEdit -----------------------------------------------------
        self.layoutDateEdit = QtWidgets.QHBoxLayout()
        self.layoutDateEdit.addWidget(labelDateStart)
        self.layoutDateEdit.addWidget(self.dateEditStart)
        self.layoutDateEdit.addSpacerItem(QtWidgets.QSpacerItem(
            10, 5, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        )

        # layoutRegularityEdit -----------------------------------------------
        labelRegularity = QtWidgets.QLabel("Ежедневный прием лекарства")

        self.layoutRegularityEdit = QtWidgets.QHBoxLayout()
        self.layoutRegularityEdit.addWidget(labelRegularity)
        self.layoutRegularityEdit.addSpacerItem(QtWidgets.QSpacerItem(
            10, 5, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        )

        # timeEdit -----------------------------------------------------------
        labelTime_1 = QtWidgets.QLabel("В")

        timeEdit_1 = QtWidgets.QTimeEdit()
        timeEdit_1.setTime(QtCore.QTime(0, 0))

        # layoutTimeEdit -----------------------------------------------------
        self.layoutTimeEdit = QtWidgets.QGridLayout()
        self.layoutTimeEdit.addWidget(labelTime_1, 0, 0)
        self.layoutTimeEdit.addWidget(timeEdit_1, 0, 1)
        self.layoutTimeEdit.setColumnStretch(8, 5)

        # pushButtonAdd ------------------------------------------------------
        self.pushButtonAdd = QtWidgets.QPushButton("Добавить")

        # layoutMain ---------------------------------------------------------
        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addWidget(self.comboBoxDrugs)
        layoutMain.addLayout(layoutDoseColor)
        layoutMain.addLayout(layoutPerRegNum)
        layoutMain.addLayout(self.layoutDateEdit)
        layoutMain.addLayout(self.layoutRegularityEdit)
        layoutMain.addLayout(self.layoutTimeEdit)
        layoutMain.addWidget(self.pushButtonAdd)

        self.setLayout(layoutMain)

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """

        self.comboBoxDrugs.currentTextChanged.connect(self.findVariant)
        self.pushButtonColor.clicked.connect(self.chooseColor)
        self.comboBoxPermanence.currentIndexChanged.connect(self.changeDateLayout)
        self.comboBoxRegularity.currentIndexChanged.connect(self.changeRegularityLayout)
        self.spinBoxNumber.valueChanged.connect(self.changeTimeEditLayout)
        self.dateEditStart.dateChanged.connect(self.changeDateEditStop)
        self.pushButtonAdd.clicked.connect(self.onPushButtonAddClicked)

    # slots --------------------------------------------------------------
    def findVariant(self, text: str) -> None:
        """
        Метод для поиска варианта выбора из comboBoxDrugs по вводимой строке
        :param text: текст из строки ввода comboBoxDrugs
        :return: None
        """

        self.comboBoxDrugs.findText(text, QtCore.Qt.MatchFlag.MatchStartsWith)

    def chooseColor(self) -> None:
        """
        Метод для выбора цвета маркера при нажатии на кнопку pushButtonColor
        :return: None
        """

        self.__color = QtWidgets.QColorDialog.getColor(parent=self, title="Выбор цвета маркера")
        self.pushButtonColor.setStyleSheet(f"background-color: {self.__color.name()}")

    def changeDateLayout(self, index: int) -> None:
        """
        Метод для перезаполнения layoutDateEdit при изменении currentIndex в comboBoxPermanence
        :param index: значение текущего индекса из comboBoxPermanence
        :return:
        """

        q = self.layoutDateEdit.count()
        match index, q:
            case 0, 3:  # должно быть 3 виджета при индексе 0
                return
            case 0, 5:
                for _ in range(q - 3):
                    q -= 1
                    widget = self.layoutDateEdit.itemAt(q).widget()
                    widget.deleteLater()
            case 1, 3:
                dateEditStop = QtWidgets.QDateEdit()
                dateEditStop.setMinimumDate(self.dateEditStart.date().addDays(1))

                labelDateStop = QtWidgets.QLabel("Окончание")

                self.layoutDateEdit.addWidget(labelDateStop)
                self.layoutDateEdit.addWidget(dateEditStop)
            case 1, 5:  # должно быть 5 виджетов при индексе 1
                return

    def changeRegularityLayout(self, index: int) -> None:
        """
        Метод для перезаполнения layoutRegularityEdit при изменении currentIndex в comboBoxRegularity
        :param index: значение текущего индекса из comboBoxRegularity
        :return: None
        """

        def setEnding(value: int) -> None:
            val1, val2 = divmod(value, 10)
            if val1 > 1 and val2 == 1:
                labelDays.setText('день')
            elif (not val1 or val1 > 1) and 1 < val2 < 5:
                labelDays.setText('дня')
            else:
                labelDays.setText('дней')

        lastnumber = self.layoutRegularityEdit.count() - 1
        while not lastnumber < 0:
            widgetlink = self.layoutRegularityEdit.itemAt(lastnumber)
            if type(widgetlink) == QtWidgets.QSpacerItem:
                self.layoutRegularityEdit.removeItem(widgetlink)
            else:
                widgetlink = widgetlink.widget()
                widgetlink.deleteLater()
            lastnumber -= 1

        labelRegularity = QtWidgets.QLabel()
        self.layoutRegularityEdit.addWidget(labelRegularity)

        match index:
            case 0:
                labelRegularity.setText("Ежедневный прием лекарства")
                self.layoutRegularityEdit.addSpacerItem(QtWidgets.QSpacerItem(
                    10, 5, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
                )
            case 1:
                labelRegularity.setText("Прием лекарства через день")
                self.layoutRegularityEdit.addSpacerItem(QtWidgets.QSpacerItem(
                    10, 5, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
                )
            case 2:
                labelRegularity.setText("Прием лекарства через каждые")

                labelDays = QtWidgets.QLabel('дня')

                spinBoxRegularity = QtWidgets.QSpinBox()
                spinBoxRegularity.setRange(2, 365)
                spinBoxRegularity.valueChanged.connect(setEnding)

                self.layoutRegularityEdit.addWidget(spinBoxRegularity)
                self.layoutRegularityEdit.addWidget(labelDays)
                self.layoutRegularityEdit.addSpacerItem(QtWidgets.QSpacerItem(
                    10, 5, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
                )

    def changeTimeEditLayout(self, value: int) -> None:
        """
        Метод для перезаполнения layoutTimeEdit при изменении value в spinBoxNumber
        :param value: значение текущего значения из spinBoxNumber
        :return: None
        """

        q = self.layoutTimeEdit.count()
        for i in range(q):
            widgetlink = self.layoutTimeEdit.itemAt(i).widget()
            widgetlink.deleteLater()
        if value == 1:
            label = QtWidgets.QLabel("В")
            label.setObjectName(f"labelTime_{value}")
            timeEdit = QtWidgets.QTimeEdit()
            timeEdit.setObjectName(f"timeEdit_{value}")
            timeEdit.setTime(QtCore.QTime(0, 0))
            self.layoutTimeEdit.addWidget(label, 0, 0)
            self.layoutTimeEdit.addWidget(timeEdit, 0, 1)
        else:
            val = 86400 // value
            rows, columns = divmod(value, 4)
            n = 0
            for i in range(rows):
                v = 0
                for j in range(4):
                    n += 1
                    label = QtWidgets.QLabel(f"{n}-й")
                    label.setObjectName(f"labelTime_{n}")
                    timeEdit = QtWidgets.QTimeEdit()
                    timeEdit.setObjectName(f"timeEdit_{n}")
                    timeEdit.setTime(QtCore.QTime(0, 0).addSecs((n - 1) * val))
                    self.layoutTimeEdit.addWidget(label, i, j + v)
                    v += 1
                    self.layoutTimeEdit.addWidget(timeEdit, i, j + v)
            v = 0
            for j in range(columns):
                n += 1
                label = QtWidgets.QLabel(f"{n}-й")
                label.setObjectName(f"labelTime_{n}")
                timeEdit = QtWidgets.QTimeEdit()
                timeEdit.setObjectName(f"timeEdit_{n}")
                timeEdit.setTime(QtCore.QTime(0, 0).addSecs((n - 1) * val))
                self.layoutTimeEdit.addWidget(label, rows, j + v)
                v += 1
                self.layoutTimeEdit.addWidget(timeEdit, rows, j + v)

    def changeDateEditStop(self, date: QtCore.QDate) -> None:
        """
        Метод для изменения даты dateEditStop при изменении даты в dateEditStart
        :param date: текущая дата в dateEditStart
        :return: None
        """

        if self.layoutDateEdit.count() > 3:
            self.layoutDateEdit.itemAt(4).widget().setMinimumDate(date.addDays(1))

    def onPushButtonAddClicked(self) -> None:
        """
        Метод для передачи данных из диалогового окна и его закрытию по нажатию кнопки
        :return: None
        """

        if not self.comboBoxDrugs.currentText():
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Название лекарства не выбрано!")
            return

        if not self.dblSpinBoxDose.value():
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Доза лекарства не выбрана!")
            return

        if self.__color.name() == '#000000':
            QtWidgets.QMessageBox.warning(self, "Предупреждение",
                                          "Выберите цвет маркера: черный цвет маркера\nсделает информацию нечитаемой!")
            return

        self.__times = [
            self.layoutTimeEdit.itemAt(i).widget().time() for i in range(1, self.layoutTimeEdit.count(), 2)
        ]
        for i in range(len(self.__times) - 1):
            if self.__times[i] > self.__times[i + 1]:
                QtWidgets.QMessageBox.warning(self, "Предупреждение", f"Время {i + 1}-го приема больше {i + 2}-го!")
                return

        self.__times = [time.toString('HH:mm') for time in self.__times]

        if self.layoutDateEdit.count() > 3:
            self.__date_stop = self.layoutDateEdit.itemAt(4).widget().date()

        if self.layoutRegularityEdit.count() > 2:
            self.__interval = self.layoutRegularityEdit.itemAt(1).widget().value()
        else:
            if self.comboBoxRegularity.currentIndex():
                self.__interval = 1

        self.__date_start = self.dateEditStart.date()

        self.generated.emit(
            (self.comboBoxDrugs.currentText(), self.dblSpinBoxDose.value(), self.dblSpinBoxDose.suffix().lstrip(),
             self.__color.name(), self.__date_start, self.__date_stop, self.__interval, self.__times))

        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = MainWindow()
    window.show()

    app.exec()
