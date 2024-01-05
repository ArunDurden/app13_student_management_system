from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMenuBar, QStatusBar, QGridLayout, QToolBar
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QSize, Qt
import sys


class MainForm(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Main Window")
        """
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        help_menu = menubar.addMenu("Help")
        """
        toolbar = QToolBar()
        #self.addToolBar(area=Qt.ToolBarArea(0), toolbar=toolbar)

        self.addToolBar(toolbar)
        #toolbar.setIconSize(QSize(50, 50))
        #QIcon(r"C:\PycharmProjects\app13_student_management_system\img\add_icon.png"),
        add_button = QAction("Add")
        toolbar.addAction(add_button)

        search_button = QAction(QIcon(r"C:\PycharmProjects\app13_student_management_system\img\search_icon.png"), "Search")
        toolbar.addAction(search_button)

        toolbar.addSeparator()



app = QApplication(sys.argv)
main_form = MainForm()
main_form.show()
app.exec()
