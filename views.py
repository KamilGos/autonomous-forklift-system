from PyQt5.QtCore import Qt, QThread, QTimer, QRect, QMetaObject, QCoreApplication, pyqtSignal, QTimer, QTime
from PyQt5.QtWidgets import QMainWindow, QDialog, QLCDNumber, QWidget,QSpinBox, QAbstractItemView, QTableWidgetItem, QHeaderView, QLineEdit,QTableWidget, QSpacerItem, QFrame, QProgressBar,  QPushButton,QFormLayout, QVBoxLayout, QApplication, QSlider, QHBoxLayout, QMenuBar, QMenu, QAction, QLabel, QSizePolicy, QTextBrowser
from PyQt5.QtGui import QImage, QColor, QFont
from pyqtgraph import ImageView


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.resize(1400, 600)
        MainWindow.setFixedSize(MainWindow.size())
        self.centralwidget = QWidget(MainWindow)
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 1400, 550))
        self.horizontalLayout1 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout1.setSpacing(2)
        self.verticalLayout2_L = QVBoxLayout()
        self.verticalLayout2_L.setGeometry(QRect(110, 110, 1400, 550))
        self.image_view = ImageView(self.horizontalLayoutWidget)
        self.verticalLayout2_L.addWidget(self.image_view)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(2)
        self.pushButton_View1 = QPushButton("View 1",self.horizontalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.pushButton_View1)
        self.pushButton_View2 = QPushButton("View 2",self.horizontalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.pushButton_View2)
        self.pushButton_View3 = QPushButton("View 3",self.horizontalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.pushButton_View3)
        # self.pushButton_View4 = QPushButton("View 4", self.horizontalLayoutWidget)
        # self.horizontalLayout_3.addWidget(self.pushButton_View4)
        # self.pushButton_View5 = QPushButton("View 5", self.horizontalLayoutWidget)
        # self.horizontalLayout_3.addWidget(self.pushButton_View5)
        self.verticalLayout2_L.addLayout(self.horizontalLayout_3)
        self.horizontalLayout1.addLayout(self.verticalLayout2_L,2)
        spacerItem = QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout1.addItem(spacerItem)
        self.verticalLayout2_P = QVBoxLayout()

        self.LCDNumber = QLCDNumber(self.horizontalLayoutWidget)
        self.LCDNumber.setSegmentStyle(QLCDNumber.Flat)

        self.LCDNumber.setMinimumHeight(60)
        self.timer = QTimer()
        self.timer.timeout.connect(self.ShowTime)
        self.timer.start(1000)
        self.ShowTime()

        self.verticalLayout2_P.addWidget(self.LCDNumber)


        self.formLayout_2PU = QFormLayout()
        self.Enter_robot_id_label = QLabel(self.horizontalLayoutWidget)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Enter_robot_id_label.setFont(font)
        self.formLayout_2PU.setWidget(0, QFormLayout.LabelRole, self.Enter_robot_id_label)
        self.Robot_id_box = QLineEdit(self.horizontalLayoutWidget)
        self.formLayout_2PU.setWidget(0, QFormLayout.FieldRole, self.Robot_id_box)
        self.Select_robot_id_button = QPushButton(self.horizontalLayoutWidget)
        font = QFont()
        font.setPointSize(9)
        self.Select_robot_id_button.setFont(font)
        self.formLayout_2PU.setWidget(1, QFormLayout.SpanningRole, self.Select_robot_id_button)
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.formLayout_2PU.setItem(2, QFormLayout.SpanningRole, spacerItem1)
        self.Enter_pallet_id_label = QLabel(self.horizontalLayoutWidget)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Enter_pallet_id_label.setFont(font)
        self.Enter_pallet_id_label.setObjectName("Enter_pallet_id_label")
        self.formLayout_2PU.setWidget(4, QFormLayout.LabelRole, self.Enter_pallet_id_label)
        self.Pallet_id_box = QLineEdit(self.horizontalLayoutWidget)
        self.formLayout_2PU.setWidget(4, QFormLayout.FieldRole, self.Pallet_id_box)
        self.Select_pallet_id_button = QPushButton(self.horizontalLayoutWidget)
        font = QFont()
        font.setPointSize(9)
        self.Select_pallet_id_button.setFont(font)
        self.Select_pallet_id_button.setObjectName("pushButton_4")
        self.formLayout_2PU.setWidget(5, QFormLayout.SpanningRole, self.Select_pallet_id_button)
        self.verticalLayout2_P.addLayout(self.formLayout_2PU)


        self.Line = QFrame(self.horizontalLayoutWidget)
        self.Line.setFrameShape(QFrame.HLine)
        self.Line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout2_P.addWidget(self.Line)
        self.Table1_Title = QLabel(self.horizontalLayoutWidget)
        font = QFont()
        font.setPointSize(9)
        font.setWeight(75)
        self.Table1_Title.setFont(font)
        self.verticalLayout2_P.addWidget(self.Table1_Title)

        self.horizontalLayout2_P_Table = QHBoxLayout(self.horizontalLayoutWidget)

        self.verticalLayout2_P_Left_Tables = QVBoxLayout(self.horizontalLayoutWidget)

        self.tableWidget = QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(3)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
        # self.tableWidget.verticalHeader().setStretchLastSection(True)
        item = QTableWidgetItem()
        item.setText("Module")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Status")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget.setColumnWidth(1, 100)
        self.verticalLayout2_P_Left_Tables.addWidget(self.tableWidget)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Camera"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Serial"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Guide"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("No initialized"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("No initialized"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("No initialized"))


        # TABLE 3 (magazine)

        self.Table3_Title = QLabel(self.horizontalLayoutWidget)
        font = QFont()
        font.setPointSize(9)
        font.setWeight(75)
        self.Table3_Title.setFont(font)
        self.verticalLayout2_P_Left_Tables.addWidget(self.Table3_Title)

        self.tableWidget3 = QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget3.setColumnCount(2)
        self.tableWidget3.setRowCount(3)
        self.tableWidget3.verticalHeader().hide()
        self.tableWidget3.horizontalHeader().setStretchLastSection(True)
        self.tableWidget3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget3.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
        # self.tableWidget.verticalHeader().setStretchLastSection(True)
        item = QTableWidgetItem()
        item.setText("Level")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget3.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Status")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget3.setHorizontalHeaderItem(1, item)
        self.tableWidget3.setColumnWidth(0, 80)
        self.tableWidget3.setColumnWidth(1, 100)
        self.verticalLayout2_P_Left_Tables.addWidget(self.tableWidget3)
        self.tableWidget3.setItem(0, 0, QTableWidgetItem("0"))
        self.tableWidget3.setItem(1, 0, QTableWidgetItem("1"))
        self.tableWidget3.setItem(2, 0, QTableWidgetItem("2"))
        self.tableWidget3.setItem(0, 1, QTableWidgetItem("Empty"))
        self.tableWidget3.setItem(1, 1, QTableWidgetItem("Empty"))
        self.tableWidget3.setItem(2, 1, QTableWidgetItem("Empty"))

        self.horizontalLayout2_P_Table.addLayout(self.verticalLayout2_P_Left_Tables)

        ## TABLE 2 (right)

        self.tableWidget2 = QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget2.setColumnCount(2)
        self.tableWidget2.setRowCount(6)
        self.tableWidget2.verticalHeader().hide()
        self.tableWidget2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget2.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
        # self.tableWidget.verticalHeader().setStretchLastSection(True)
        item = QTableWidgetItem()
        item.setText("Name")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget2.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Value")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget2.setHorizontalHeaderItem(1, item)
        self.tableWidget2.setColumnWidth(0, 80)
        self.tableWidget2.setColumnWidth(1, 100)
        self.horizontalLayout2_P_Table.addWidget(self.tableWidget2)
        self.tableWidget2.setItem(0, 0, QTableWidgetItem("Camera"))
        self.tableWidget2.setItem(1, 0, QTableWidgetItem("Serial Port"))
        self.tableWidget2.setItem(2, 0, QTableWidgetItem("Baudrate"))
        self.tableWidget2.setItem(3, 0, QTableWidgetItem("FPTV"))
        self.tableWidget2.setItem(4, 0, QTableWidgetItem("Goals"))
        self.tableWidget2.setItem(5, 0, QTableWidgetItem("Phase"))

        self.tableWidget2.setItem(0, 1, QTableWidgetItem(""))
        self.tableWidget2.setItem(1, 1, QTableWidgetItem(""))
        self.tableWidget2.setItem(2, 1, QTableWidgetItem(""))
        self.tableWidget2.setItem(3, 1, QTableWidgetItem(""))
        self.tableWidget2.setItem(4, 1, QTableWidgetItem(""))
        self.tableWidget2.setItem(5, 1, QTableWidgetItem(""))



        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout2_P_Table.addItem(spacerItem4)
        self.verticalLayout2_P.addLayout(self.horizontalLayout2_P_Table)
        ##################

        self.pushButton_GO = QPushButton("START", self.horizontalLayoutWidget)
        self.verticalLayout2_P.addWidget(self.pushButton_GO)
        self.ProgressBar = QProgressBar(self.horizontalLayoutWidget)
        self.ProgressBar.setProperty("value", 0)
        self.verticalLayout2_P.addWidget(self.ProgressBar)

        self.horizontalLayout1.addLayout(self.verticalLayout2_P,1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1400, 25))
        self.menuFPTV = QMenu(self.menubar)
        self.menuFPTV.setObjectName("FPTV")

        self.menubar.addAction(self.menuFPTV.menuAction())
        MainWindow.setMenuBar(self.menubar)

        self.actionChange_FPTV = QAction()
        self.actionChange_FPTV.setObjectName("actionChange_FPTV")
        self.menuFPTV.addAction(self.actionChange_FPTV)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def ShowTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]
        self.LCDNumber.display(text)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        self.menuFPTV.setTitle(_translate("MainWindow", "FPTV"))
        self.actionChange_FPTV.setText(_translate("MainWindow", "Change"))
        self.Enter_robot_id_label.setText(_translate("MainWindow", "Enter robot id:"))
        self.Select_robot_id_button.setText(_translate("MainWindow", "Select"))
        self.Enter_pallet_id_label.setText(_translate("MainWindow", "Enter pallet id:"))
        self.Select_pallet_id_button.setText(_translate("MainWindow", "Select"))
        self.Table1_Title .setText(_translate("MainWindow", "            Module statuses                                Paremeters"))
        self.Table3_Title .setText(_translate("MainWindow", "                 Warehouse"))

        # self.Table2_Title .setText(_translate("MainWindow", "Parameters"))



class Ui_New_FPTV_value_Window(QDialog):
    sig_Change_FPTV = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Ui_New_FPTV_value_Window, self).__init__(parent)
        self.setupUi(self)
        sig_Change_FPTV = pyqtSignal(int)
        self.pushButton_OK.clicked.connect(self.Get_New_Value)

    def Get_New_Value(self):
        value = self.spinBox.value()
        self.sig_Change_FPTV.emit(value)
        self.close()

    def setupUi(self, New_FPTV_value_Window):
        New_FPTV_value_Window.setObjectName("New_FPTV_value_Window")
        New_FPTV_value_Window.resize(433, 89)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(New_FPTV_value_Window.sizePolicy().hasHeightForWidth())
        New_FPTV_value_Window.setSizePolicy(sizePolicy)
        self.formLayoutWidget = QWidget(New_FPTV_value_Window)
        self.formLayoutWidget.setGeometry(QRect(0, 10, 431, 71))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QLabel(self.formLayoutWidget)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)
        self.spinBox = QSpinBox(self.formLayoutWidget)
        self.spinBox.setMinimum(5)
        self.spinBox.setMaximum(250)
        self.spinBox.setObjectName("spinBox")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.spinBox)
        self.pushButton_OK = QPushButton(self.formLayoutWidget)
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.pushButton_OK)

        self.retranslateUi(New_FPTV_value_Window)
        QMetaObject.connectSlotsByName(New_FPTV_value_Window)

    def retranslateUi(self, New_FPTV_value_Window):
        _translate = QCoreApplication.translate
        New_FPTV_value_Window.setWindowTitle(_translate("New_FPTV_value_Window", "New FPTV"))
        self.label.setText(_translate("New_FPTV_value_Window", "     NEW VALUE:"))
        self.pushButton_OK.setText(_translate("New_FPTV_value_Window", "OK"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())





