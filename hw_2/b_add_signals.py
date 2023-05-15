import random

from PySide6 import QtWidgets, QtCore


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация интерфейса
        :return: None
        """

        # comboBox -----------------------------------------------------------
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItem("Элемент 1")
        self.comboBox.addItem("Элемент 2")
        self.comboBox.addItems(["Элемент 3", "Элемент 4", "Элемент 5"])
        self.comboBox.insertItem(0, "")

        self.pushButtonComboBox = QtWidgets.QPushButton("Получить данные")

        layoutComboBox = QtWidgets.QHBoxLayout()
        layoutComboBox.addWidget(self.comboBox)
        layoutComboBox.addWidget(self.pushButtonComboBox)

        # lineEdit -----------------------------------------------------------
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("Введите текст")

        self.pushButtonLineEdit = QtWidgets.QPushButton("Получить данные")

        layoutLineEdit = QtWidgets.QHBoxLayout()
        layoutLineEdit.addWidget(self.lineEdit)
        layoutLineEdit.addWidget(self.pushButtonLineEdit)

        # textEdit -----------------------------------------------------------
        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setPlaceholderText("Введите текст")

        self.pushButtonTextEdit = QtWidgets.QPushButton("Получить данные")

        layoutTextEdit = QtWidgets.QHBoxLayout()
        layoutTextEdit.addWidget(self.textEdit)
        layoutTextEdit.addWidget(self.pushButtonTextEdit)

        # plainTextEdit ------------------------------------------------------
        self.plainTextEdit = QtWidgets.QPlainTextEdit()
        self.plainTextEdit.setPlaceholderText("Введите текст")

        self.pushButtonPlainTextEdit = QtWidgets.QPushButton("Получить данные")

        layoutPlainTextEdit = QtWidgets.QHBoxLayout()
        layoutPlainTextEdit.addWidget(self.plainTextEdit)
        layoutPlainTextEdit.addWidget(self.pushButtonPlainTextEdit)

        # spinBox ------------------------------------------------------------
        self.spinBox = QtWidgets.QSpinBox()  # по умолчанию от 0 до 99!!!
        self.spinBox.setValue(random.randint(0, 99))  # изменил диапазон случайных значений с (-50, 50) на (0, 99)!!!
        self.spinBox.setSuffix(' km')  # добавил суффикс к значениям spinBox!!!
        self.spinBox.setWrapping(True)  # закольцевал spinBox!!!

        self.pushButtonSpinBox = QtWidgets.QPushButton("Получить данные")

        layoutSpinBox = QtWidgets.QHBoxLayout()
        layoutSpinBox.addWidget(self.spinBox)
        layoutSpinBox.addWidget(self.pushButtonSpinBox)

        # doubleSpinBox ------------------------------------------------------
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox()  # по умолчанию от 0.00 до 99.99!!!
        self.doubleSpinBox.setValue(random.uniform(0, 99.99))  # изменил диапазон случайных значений с (-50, 50) на
        # (0, 99.99) и метод randint на uniform!!!
        self.doubleSpinBox.setPrefix('$ ')  # добавил префикс к значениям doubleSpinBox!!!
        self.doubleSpinBox.setWrapping(True)  # закольцевал doubleSpinBox!!!

        self.pushButtonDoubleSpinBox = QtWidgets.QPushButton("Получить данные")

        layoutDoubleSpinBox = QtWidgets.QHBoxLayout()
        layoutDoubleSpinBox.addWidget(self.doubleSpinBox)
        layoutDoubleSpinBox.addWidget(self.pushButtonDoubleSpinBox)

        # timeEdit -----------------------------------------------------------
        self.timeEdit = QtWidgets.QTimeEdit()
        self.timeEdit.setTime(QtCore.QTime.currentTime().addSecs(random.randint(-10000, 10000)))

        self.pushButtonTimeEdit = QtWidgets.QPushButton("Получить данные")

        layoutTimeEdit = QtWidgets.QHBoxLayout()
        layoutTimeEdit.addWidget(self.timeEdit)
        layoutTimeEdit.addWidget(self.pushButtonTimeEdit)

        # dateTimeEdit -------------------------------------------------------
        self.dateTimeEdit = QtWidgets.QDateTimeEdit()
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime().addDays(random.randint(-10, 10)))
        self.dateTimeEdit.setCalendarPopup(True)  # добавил выпадающий календарь для удобства!!!

        self.pushButtonDateTimeEdit = QtWidgets.QPushButton("Получить данные")

        layoutDateTimeEdit = QtWidgets.QHBoxLayout()
        layoutDateTimeEdit.addWidget(self.dateTimeEdit)
        layoutDateTimeEdit.addWidget(self.pushButtonDateTimeEdit)

        # plainTextEditLog ---------------------------------------------------
        self.plainTextEditLog = QtWidgets.QPlainTextEdit()
        self.plainTextEditLog.setReadOnly(True)  # убрал возможность вносить изменения в окно лога!!!

        self.pushButtonClearLog = QtWidgets.QPushButton("Очистить лог")

        layoutLog = QtWidgets.QHBoxLayout()
        layoutLog.addWidget(self.plainTextEditLog)
        layoutLog.addWidget(self.pushButtonClearLog)

        # main layout

        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addLayout(layoutComboBox)
        layoutMain.addLayout(layoutLineEdit)
        layoutMain.addLayout(layoutTextEdit)
        layoutMain.addLayout(layoutPlainTextEdit)
        layoutMain.addLayout(layoutSpinBox)
        layoutMain.addLayout(layoutDoubleSpinBox)
        layoutMain.addLayout(layoutTimeEdit)
        layoutMain.addLayout(layoutDateTimeEdit)
        layoutMain.addLayout(layoutLog)

        self.setLayout(layoutMain)

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """

        self.pushButtonComboBox.clicked.connect(self.onPushButtonComboBoxClicked)  # подключить слот для вывода текста из comboBox в plainTextEditLog при нажатии на кнопку
        self.pushButtonLineEdit.clicked.connect(self.onPushButtonLineEditClicked)  # сразу был подключен слот для вывода текста из textEdit в plainTextEditLog при нажатии на кнопку!!!
        self.pushButtonTextEdit.clicked.connect(self.onPushButtonTextEditClicked)  # подключить слот для вывода текста из textEdit в plainTextEditLog при нажатии на кнопку
        self.pushButtonPlainTextEdit.clicked.connect(self.onPushButtonPlainTextEditClicked)  # подключить слот для вывода текста из plaineTextEdit в plainTextEditLog при нажатии на кнопку
        self.pushButtonSpinBox.clicked.connect(self.onPushButtonSpinBoxClicked)  # подключить слот для вывода значения из spinBox в plainTextEditLog при нажатии на кнопку
        self.pushButtonDoubleSpinBox.clicked.connect(self.onPushButtonDoubleSpinBoxClicked)  # подключить слот для вывода значения из doubleSpinBox в plainTextEditLog при нажатии на кнопку
        self.pushButtonTimeEdit.clicked.connect(self.onPushButtonTimeEditClicked)  # подключить слот для вывода времени из timeEdit в plainTextEditLog при нажатии на кнопку
        self.pushButtonDateTimeEdit.clicked.connect(self.onPushButtonDateTimeEditClicked)  # подключить слот для вывода времени из dateTimeEdit в plainTextEditLog при нажатии на кнопку
        self.pushButtonClearLog.clicked.connect(self.plainTextEditLog.clear)  # подключить слот для очистки plainTextEditLog при нажатии на кнопку
        #
        self.comboBox.currentIndexChanged.connect(self.changeComboBoxIndex)  # подключить слот для вывода текста в plainTextEditLog при изменении выбранного элемента в comboBox
        self.spinBox.valueChanged.connect(self.changeSpinBoxValue)  # подключить слот для вывода значения в plainTextEditLog при изменении значения в spinBox
        self.dateTimeEdit.dateTimeChanged.connect(self.changeDateTimeEditValue)  # подключить слот для вывода датывремени в plainTextEditLog при изменении датывремени в dateTimeEdit

    # slots --------------------------------------------------------------
    # Самостоятельная реализация слотов для сигналов
    # Заменил в слотах setPlainText на insertPlainText с переводом каретки на новую строку (\n)!!!

    def onPushButtonComboBoxClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonComboBox
        :return: None
        """

        self.plainTextEditLog.insertPlainText(self.comboBox.currentText() + '\n')

    def onPushButtonLineEditClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonLineEdit
        :return: None
        """

        self.plainTextEditLog.insertPlainText(self.lineEdit.text() + '\n')

    def onPushButtonTextEditClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonTextEdit
        :return: None
        """

        self.plainTextEditLog.insertPlainText(self.textEdit.toPlainText() + '\n')

    def onPushButtonPlainTextEditClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonPlainTextEdit
        :return: None
        """

        self.plainTextEditLog.insertPlainText(self.plainTextEdit.toPlainText() + '\n')

    def onPushButtonSpinBoxClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonSpinBox
        :return: None
        """

        self.plainTextEditLog.insertPlainText(self.spinBox.cleanText() + ' -> ' + self.spinBox.text() + '\n')

    def onPushButtonDoubleSpinBoxClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonDoubleSpinBox
        :return: None
        """

        self.plainTextEditLog.insertPlainText(
            self.doubleSpinBox.cleanText() + ' -> ' + self.doubleSpinBox.text() + '\n'
        )

    def onPushButtonTimeEditClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonTimeEdit
        :return: None
        """

        self.plainTextEditLog.insertPlainText(self.timeEdit.text() + '\n')

    def onPushButtonDateTimeEditClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonDateTimeEdit
        :return: None
        """

        self.plainTextEditLog.insertPlainText(self.dateTimeEdit.text() + '\n')

    def changeComboBoxIndex(self) -> None:
        """
        Обработка сигнала выбора значения в comboBox
        :return: None
        """

        self.plainTextEditLog.insertPlainText(
            'Индекс №' + str(self.comboBox.currentIndex()) + ' -> ' + self.comboBox.currentText() + '\n'
        )

    def changeSpinBoxValue(self) -> None:
        """
        Обработка сигнала изменения значения в spinBox
        :return: None
        """

        self.plainTextEditLog.insertPlainText(self.spinBox.cleanText() + '\n')

    def changeDateTimeEditValue(self) -> None:
        """
        Обработка сигнала изменения значения в dateTimeEdit
        :return: None
        """

        self.plainTextEditLog.insertPlainText(self.dateTimeEdit.text() + '\n')


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
