from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMenuBar, QStatusBar,\
    QGridLayout, QToolBar, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QComboBox, QVBoxLayout
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QSize, Qt
import sys
import sqlite3


class MainForm(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Main Window")

        menubar = self.menuBar()

        #add_icon = QIcon(r"C:\Users\arunp\Python_Projects\app13_student_management_system\img\add_icon.png")
        #self.add_button = QAction(add_icon, "Add")
        self.add_button = QAction("Add")
        self.add_button.triggered.connect(self.add_menu)

        file_menu = menubar.addMenu("File")
        help_menu = menubar.addMenu("Help")
        file_menu.addAction(self.add_button)

        self.table = QTableWidget()

        self.table.setColumnCount(4)
        column_names = ["ID", "Name", "Courses", "Mobile"]
        self.table.setHorizontalHeaderLabels(column_names)

        self.load_data()
        self.table.setVerticalHeaderLabels([])
        self.table.verticalHeader().hide()
        self.setCentralWidget(self.table)



        ##toolbar = self.addToolBar("Tool Bar")
        #toolbar.addAction(self.add_button)

        #toolbar.addWidget(QPushButton(add_icon, "ADD"))
        #toolbar.setBaseSize(16, 16)
        #toolbar.setMovable(False)
        #self.addToolBar(area=Qt.ToolBarArea(0), toolbar=toolbar)

        #self.addToolBar(toolbar)
        #toolbar.setIconSize(QSize(50, 50))

    def load_data(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()

        self.table.setRowCount(0)
        for row, item in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(item[0])))
            self.table.setItem(row, 1, QTableWidgetItem(item[1]))
            self.table.setItem(row, 2, QTableWidgetItem(item[2]))
            self.table.setItem(row, 3, QTableWidgetItem(str(item[3])))

        cursor.close()
        connection.close()

    def add_menu(self):
        add = AddStudent()
        add.exec()

class AddStudent(QDialog):

    def __init__(self):
        super().__init__()

        name = QLineEdit()
        name.setPlaceholderText("Enter the student name")

        courses = QComboBox()
        courses_list = ["Astronomy", "Biology", "Math", "Physics"]
        courses.addItems(courses_list)

        mobile = QLineEdit()
        mobile.setPlaceholderText("Enter the mobile number")

        submit = QPushButton("Submit")
        submit.clicked.connect(self.add)
        layout = QVBoxLayout()
        layout.addWidget(name)
        layout.addWidget(courses)
        layout.addWidget(mobile)
        layout.addWidget(submit)

        self.setLayout(layout)

    def add(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        #cursor.execute("INSERT INTO Students VALUES")
        print("Hi")




app = QApplication(sys.argv)
main_form = MainForm()
main_form.show()
#main_form.load_data()
app.exec()
