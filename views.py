from PyQt5.QtCore import Qt, QThread, QTimer, QRect, QMetaObject, QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QSpacerItem, QFrame, QPushButton,QFormLayout, QVBoxLayout, QApplication, QSlider, QHBoxLayout, QMenuBar, QMenu, QAction, QLabel, QSizePolicy, QTextBrowser
from PyQt5.QtGui import QImage, QColor, QFont
from pyqtgraph import ImageView
import numpy as np
import cv2
import cv2.aruco as aruco

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
        self.pushButton_View4 = QPushButton("View 4", self.horizontalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.pushButton_View4)
        self.pushButton_View5 = QPushButton("View 5", self.horizontalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.pushButton_View5)
        self.verticalLayout2_L.addLayout(self.horizontalLayout_3)
        self.horizontalLayout1.addLayout(self.verticalLayout2_L,2)
        spacerItem = QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout1.addItem(spacerItem)
        self.verticalLayout2_P = QVBoxLayout()
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

        self.pushButton_GO = QPushButton("GO", self.horizontalLayoutWidget)

        self.verticalLayout2_P.addWidget(self.pushButton_GO)


        self.horizontalLayout1.addLayout(self.verticalLayout2_P,1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1400, 25))
        self.menuPlik = QMenu(self.menubar)
        self.menuPlik.setObjectName("menuPlik")

        self.menubar.addAction(self.menuPlik.menuAction())
        MainWindow.setMenuBar(self.menubar)

        self.actionZapisz_Ramke = QAction()
        self.actionZapisz_Ramke.setObjectName("actionZapisz_Ramke")
        self.menuPlik.addAction(self.actionZapisz_Ramke)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        self.menuPlik.setTitle(_translate("MainWindow", "File"))
        self.actionZapisz_Ramke.setText(_translate("MainWindow", "Zapisz Ramkę"))
        self.Enter_robot_id_label.setText(_translate("MainWindow", "Enter robot id:"))
        self.Select_robot_id_button.setText(_translate("MainWindow", "Select"))
        self.Enter_pallet_id_label.setText(_translate("MainWindow", "Enter pallet id:"))
        self.Select_pallet_id_button.setText(_translate("MainWindow", "Select"))





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())





