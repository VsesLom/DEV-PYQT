"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtGui, QtCore

from hw_2.ui.d_eventfilter_settings import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.loadData()
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация интерфейса
        :return: None
        """

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # comboBox -----------------------------------------------------------
        self.ui.comboBox.addItems(['bin', 'oct', 'dec', 'hex'])  # добавил системы исчисления в comboBox

        # dial ---------------------------------------------------------------
        self.ui.dial.setMaximum(999)  # изменил максимум с 99 на 999 в dial
        self.ui.dial.installEventFilter(self)  # установил фильтр событий для круглого переключателя dial

        # horizontalSlider ---------------------------------------------------
        self.ui.horizontalSlider.setMaximum(999)  # изменил максимум с 99 на 999 в horizontalSlider

        # lcdNumber ----------------------------------------------------------
        self.ui.lcdNumber.setDigitCount(10)  # изменил количество отображаемых цифр с 5 до 10 (для корректного
        # отображения двоичных значений)

    def loadData(self) -> None:
        """
        Загрузка данных в Ui
        :return: None
        """

        settings = QtCore.QSettings("ConverterApp")

        match settings.value("mode", self.ui.comboBox.currentText()):
            case 'bin':
                self.ui.lcdNumber.setBinMode()
                self.ui.comboBox.setCurrentText('bin')
            case 'oct':
                self.ui.lcdNumber.setOctMode()
                self.ui.comboBox.setCurrentText('oct')
            case 'dec':
                self.ui.lcdNumber.setDecMode()
                self.ui.comboBox.setCurrentText('dec')
            case 'hex':
                self.ui.lcdNumber.setHexMode()
                self.ui.comboBox.setCurrentText('hex')

        self.ui.dial.setValue(settings.value("value", 0))
        self.ui.horizontalSlider.setValue(settings.value("value", 0))
        self.ui.lcdNumber.display(settings.value("value", 0))

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """

        self.ui.comboBox.currentTextChanged.connect(self.changeComboBoxText)
        self.ui.dial.valueChanged.connect(self.sliderDialMoved)
        self.ui.horizontalSlider.valueChanged.connect(self.sliderHorizontalMoved)

    # slots --------------------------------------------------------------
    def changeComboBoxText(self) -> None:
        """
        Обработка сигнала выбора значения в comboBox
        :return: None
        """

        match self.ui.comboBox.currentText():
            case 'bin':
                self.ui.lcdNumber.setBinMode()
            case 'oct':
                self.ui.lcdNumber.setOctMode()
            case 'dec':
                self.ui.lcdNumber.setDecMode()
            case 'hex':
                self.ui.lcdNumber.setHexMode()

    def sliderDialMoved(self) -> None:
        """
        Обработка сигнала valueChanged для круглого переключателя dial
        :return: None
        """

        self.ui.horizontalSlider.setValue(self.ui.dial.value())
        self.ui.lcdNumber.display(self.ui.dial.value())

    def sliderHorizontalMoved(self) -> None:
        """
        Обработка сигнала valueChanged для горизонтального слайдера horizontalSlider
        :return: None
        """

        self.ui.dial.setValue(self.ui.horizontalSlider.value())
        self.ui.lcdNumber.display(self.ui.horizontalSlider.value())

    # events --------------------------------------------------------------
    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """
        Настройка дополнительного поведения для круглого переключателя dial
        :param watched: QtCore.QObject
        :param event: QtCore.QEvent
        :return: bool
        """

        if watched == self.ui.dial and event.type() == QtCore.QEvent.Type.KeyPress:
            match event.text():
                case '+':
                    self.ui.dial.setValue(self.ui.dial.value() + 1)
                    self.ui.horizontalSlider.setValue(self.ui.dial.value())
                    print(self.ui.dial.value())
                case '-':
                    self.ui.dial.setValue(self.ui.dial.value() - 1)
                    self.ui.horizontalSlider.setValue(self.ui.dial.value())
                    print(self.ui.dial.value())

        return super(Window, self).eventFilter(watched, event)

    # def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
    #     """
    #     Событие нажатия на клавишу '+' или '-' при открытом окне приложения без привязки к виджетам
    #     :param event: QtGui.QKeyEvent
    #     :return: None
    #     """
    #     match event.text():
    #         case '+':
    #             self.ui.dial.setValue(self.ui.dial.value() + 1)
    #             self.ui.horizontalSlider.setValue(self.ui.dial.value())
    #             print(self.ui.dial.value())
    #         case '-':
    #             self.ui.dial.setValue(self.ui.dial.value() - 1)
    #             self.ui.horizontalSlider.setValue(self.ui.dial.value())
    #             print(self.ui.dial.value())

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Событие закрытия окна
        :param event: QtGui.QCloseEvent
        :return: None
        """
        answer = QtWidgets.QMessageBox.question(
            self, "Закрытие окна приложения", "Вы действительно хотите закрыть окно?\n(Все текущие данные будут сохранены)"
        )
        if answer == QtWidgets.QMessageBox.Yes:
            settings = QtCore.QSettings("ConverterApp")
            settings.setValue("mode", self.ui.comboBox.currentText())
            settings.setValue("value", self.ui.lcdNumber.intValue())
            print(settings.fileName())  # для ускорения поиска сохраненных настроек в реестре
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
