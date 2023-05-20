"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets, QtCore, QtGui

from a_threads import SystemInfo


class SystemInfoWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initThreads()
        self.initUi()
        self.initSignals()

    def initThreads(self) -> None:
        """
        Инициализация потоков
        :return: None
        """

        self.threadSI = SystemInfo()
        self.threadSI.status = True
        self.threadSI.start()

    def initUi(self) -> None:
        """
        Инициализация интерфейса
        :return: None
        """

        # window -------------------------------------------------------------
        self.setWindowTitle("Диспетчер ПК")
        # self.setMinimumSize(320, 110)
        # self.setMaximumSize(320, 120)

        # spinBoxDelaySI -------------------------------------------------------
        labelspinBoxDelaySI = QtWidgets.QLabel("Пауза после получения данных о системе:")
        labelspinBoxDelaySI.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred
        )

        self.spinBoxDelaySI = QtWidgets.QSpinBox()
        self.spinBoxDelaySI.setMinimumSize(60, 0)
        self.spinBoxDelaySI.setSuffix(' сек')
        self.spinBoxDelaySI.setMinimum(1)

        # layuotSpinBoxDelaySI -------------------------------------------------
        layoutSpinBoxDelaySI = QtWidgets.QHBoxLayout()
        layoutSpinBoxDelaySI.addWidget(labelspinBoxDelaySI)
        layoutSpinBoxDelaySI.addWidget(self.spinBoxDelaySI)

        # labelCPU -----------------------------------------------------------
        self.labelCPU = QtWidgets.QLabel(
            "<big><b style='color: green'>ЦП</b> <i style='color: green'>загружен на      %</i></big>"
        )
        self.labelCPU.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # labelRAM -----------------------------------------------------------
        self.labelRAM = QtWidgets.QLabel(
            "<big><b style='color: green'>ОЗУ</b> <i style='color: green'>загружено на      %</i></big>"
        )
        self.labelRAM.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(layoutSpinBoxDelaySI)
        layout.addWidget(self.labelCPU)
        layout.addWidget(self.labelRAM)

        self.setLayout(layout)

    def initSignals(self) -> None:
        """
        Инициализация сигналов
        :return: None
        """

        self.spinBoxDelaySI.valueChanged.connect(self.spinBoxDelaySIChanged)
        self.threadSI.systemInfoReceived.connect(self.reportSystemInfo)

    # slots --------------------------------------------------------------
    def spinBoxDelaySIChanged(self) -> None:
        """
        Обработка сигнала изменения значения в spinBoxDelaySI
        :return: None
        """

        self.threadSI.delay = self.spinBoxDelaySI.value()

    def reportSystemInfo(self, data: list) -> None:
        """
        Приём данных из потока и обработка их в основном цикле приложения
        :param data: информация о загрузке ЦП и ОЗУ из потока
        :return: None
        """

        def getColor(value: float) -> str:
            if value < 25.0:
                return 'green'
            elif 25.0 <= value < 50.0:
                return 'gold'
            elif 50.0 <= value < 75.0:
                return 'orange'
            else:
                return 'red'

        colorCPU = getColor(data[0])
        colorRAM = getColor(data[1])
        self.labelCPU.setText(
                f"<big><b style='color: {colorCPU}'>ЦП</b> <i style='color: {colorCPU}'>загружен на {data[0]} %</i></big>"
            )
        self.labelRAM.setText(
                f"<big><b style='color: {colorRAM}'>ОЗУ</b> <i style='color: {colorRAM}'>загружено на {data[1]} %</i></big>"
            )

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Событие закрытия окна
        :param event: QtGui.QCloseEvent
        :return: None
        """

        self.threadSI.status = False
        self.threadSI.wait(deadline=(self.threadSI.delay * 1000))
        self.threadSI.finished.connect(self.threadSI.deleteLater)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = SystemInfoWidget()
    window.show()

    app.exec()
