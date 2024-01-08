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
        self.add_button = QAction("Add")
        self.add_button.triggered.connect(self.add_menu)

        self.search_button = QAction("Search")
        self.search_button.triggered.connect(self.search_menu)

        file_menu = menubar.addMenu("File")
        help_menu = menubar.addMenu("Help")
        file_menu.addAction(self.add_button)
        help_menu.addAction(self.search_button)

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
        add = AddStudent(mainform=self)
        add.exec()

    def search_menu(self):
        search = SearchStudent()
        search.exec()

class AddStudent(QDialog):
    def __init__(self, mainform):
        super().__init__()
        self.mainform = mainform
        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter the student name")

        self.courses = QComboBox()
        courses_list = ["Astronomy", "Biology", "Math", "Physics"]
        self.courses.addItems(courses_list)


        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Enter the mobile number")

        submit = QPushButton("Submit")
        submit.clicked.connect(self.add)
        layout = QVBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(self.courses)
        layout.addWidget(self.mobile)
        layout.addWidget(submit)

        self.setLayout(layout)

    """def last_id(self, mainform):
        mainform.table."""

    def add(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        table_list = cursor.fetchall()
        length = len(table_list)
        ID = str(length + 1)

        print(ID, type(ID))
        print(self.name.text(), type(self.name.text()))
        print(self.courses.currentText(), type(self.courses.currentText()))
        print(self.mobile.text(), type(self.mobile.text()))
        cursor.execute("INSERT INTO students (id, name, course, mobile) VALUES (?, ? ,?, ?)",
                       (ID, self.name.text(), self.courses.currentText(), self.mobile.text()))
        connection.commit()

        self.mainform.load_data()

class SearchStudent(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search Student")

        name = QLineEdit()
        name.setPlaceholderText("Name")
        search_button = QPushButton("Search")

        layout = QVBoxLayout()
        layout.addWidget(name)
        layout.addWidget(search_button)

        self.setLayout(layout)


app = QApplication(sys.argv)
main_form = MainForm()
main_form.show()
app.exec()
