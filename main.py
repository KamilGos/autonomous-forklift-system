from PyQt5.QtWidgets import QApplication
from sources.app_control import AppControl

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWindow = AppControl()
    MainWindow.show()
    app.exit(app.exec_())