"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""
import time

from PySide6 import QtWidgets, QtGui

from hw_2.ui.c_signals_events import Ui_Form


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

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # plainTextEdit ------------------------------------------------------
        self.ui.plainTextEdit.setReadOnly(True)  # убрал возможность вносить изменения в окно лога!!!

        # pushButtonLT -------------------------------------------------------
        self.ui.pushButtonLT.setAutoRepeat(True)  # добавил автоповтор действия при зажимании кнопки!!!

        # pushButtonRT -------------------------------------------------------
        self.ui.pushButtonRT.setAutoRepeat(True)  # добавил автоповтор действия при зажимании кнопки!!!

        # pushButtonLB -------------------------------------------------------
        self.ui.pushButtonLB.setAutoRepeat(True)  # добавил автоповтор действия при зажимании кнопки!!!

        # pushButtonRB -------------------------------------------------------
        self.ui.pushButtonRB.setAutoRepeat(True)  # добавил автоповтор действия при зажимании кнопки!!!

        # spinBoxX -----------------------------------------------------------
        self.ui.spinBoxX.setMaximum(
            QtWidgets.QApplication.primaryScreen().geometry().size().width() - self.minimumSize().width())
        # увеличил максимальное значение spinBoxX до (ширина основного экрана - минимальная ширина окна Form)

        # spinBoxY -----------------------------------------------------------
        self.ui.spinBoxY.setMaximum(
            QtWidgets.QApplication.primaryScreen().geometry().size().height() - self.minimumSize().height())
        # увеличил максимальное значение spinBoxY до (высота основного экрана - минимальная высота окна Form)

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """

        self.ui.pushButtonLT.clicked.connect(self.onPushButtonLTClicked)
        self.ui.pushButtonRT.clicked.connect(self.onPushButtonRTClicked)
        self.ui.pushButtonLB.clicked.connect(self.onPushButtonLBClicked)
        self.ui.pushButtonRB.clicked.connect(self.onPushButtonRBClicked)
        self.ui.pushButtonCenter.clicked.connect(self.onPushButtonCenterClicked)

        self.ui.pushButtonMoveCoords.clicked.connect(self.onPushButtonMoveCoordsClicked)

        self.ui.pushButtonGetData.clicked.connect(self.onPushButtonGetDataClicked)

    # slots --------------------------------------------------------------
    def onPushButtonLTClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonLT
        :return: None
        """

        self.move(self.pos().x() - 1, self.pos().y() - 1)

    def onPushButtonRTClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonRT
        :return: None
        """

        self.move(self.pos().x() + 1, self.pos().y() - 1)

    def onPushButtonLBClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonLB
        :return: None
        """

        self.move(self.pos().x() - 1, self.pos().y() + 1)

    def onPushButtonRBClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonRB
        :return: None
        """

        self.move(self.pos().x() + 1, self.pos().y() + 1)

    def onPushButtonCenterClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonCenter
        :return: None
        """

        self.move(
            QtWidgets.QApplication.primaryScreen().geometry().size().width() // 2 - self.size().width() // 2,
            QtWidgets.QApplication.primaryScreen().geometry().size().height() // 2 - self.size().height() // 2
        )

    def onPushButtonMoveCoordsClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonMoveCoords
        :return: None
        """

        self.move(int(self.ui.spinBoxX.text()), int(self.ui.spinBoxY.text()))

    def onPushButtonGetDataClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonGetData
        :return: None
        """

        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.insertPlainText(
            time.ctime() + " Количество подключенных мониторов: " + str(len(QtWidgets.QApplication.screens())) + '\n'
        )
        self.ui.plainTextEdit.insertPlainText(
            time.ctime() + " Название активного монитора: " + QtWidgets.QApplication.primaryScreen().name() + '\n'
        )
        self.ui.plainTextEdit.insertPlainText(
            time.ctime() + " Разрешение активного монитора: " + ' x '.join(
                map(str, (QtWidgets.QApplication.primaryScreen().geometry().size().toTuple()))) + '\n'
        )
        self.ui.plainTextEdit.insertPlainText(
            time.ctime() + " Название активного окна: " + self.objectName() + '\n'
        )
        self.ui.plainTextEdit.insertPlainText(
            time.ctime() + " Размер активного окна: " + ' x '.join(map(str, self.size().toTuple())) + '\n'
        )
        self.ui.plainTextEdit.insertPlainText(
            time.ctime() + " Минимальный размер активного окна: " + ' x '.join(
                map(str, (self.minimumSize().toTuple()))) + '\n'
        )
        self.ui.plainTextEdit.insertPlainText(
            time.ctime() + " Координаты активного окна: " + ', '.join(map(str, self.pos().toTuple())) + '\n'
        )
        self.ui.plainTextEdit.insertPlainText(
            time.ctime() + " Координаты центра активного окна: " + ', '.join(map(str, (
                self.pos().x() + self.size().width() // 2,
                self.pos().y() + self.size().height() // 2))) + '\n'
        )
        self.ui.plainTextEdit.insertPlainText(
            time.ctime() + " Состояние активного окна: " + self.windowState().name + '\n'
        )

    # events --------------------------------------------------------------
    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
        """
        Событие при перемещении окна
        :param event: QtGui.QMoveEvent
        :return:
        """

        print(time.ctime(), event.oldPos().toTuple(), '->', event.pos().toTuple())

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        Событие изменения размера окна

        :param event: QtGui.QResizeEvent
        :return: None
        """

        print(time.ctime(), event.size().width(), 'x', event.size().height())


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
