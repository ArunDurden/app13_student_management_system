from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMenuBar, QStatusBar,\
    QGridLayout, QToolBar, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QComboBox, QVBoxLayout
from PyQt6.QtGui import QIcon, QAction, QMouseEvent
from PyQt6.QtCore import QSize, Qt, QEvent
import sys
import sqlite3


class MainForm(QMainWindow):
    def __init__(self):

        super().__init__()
        self.setWindowTitle("Main Window")
        self.setMinimumSize(800, 600)

        menubar = self.menuBar()
        add_icon = QIcon("icons/add.png")
        self.add_button = QAction(add_icon, "Add")
        self.add_button.triggered.connect(self.add_menu)

        search_icon = QIcon("./icons/search.png")
        self.search_button = QAction(search_icon, "Search")
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

        toolbar = QToolBar()
        toolbar.addAction(self.add_button)
        toolbar.addAction(self.search_button)
        self.addToolBar(toolbar)
        self.status_bar = QStatusBar()

        edit_record_button = QPushButton("Edit Record")
        edit_record_button.clicked.connect(self.edit_student)
        self.status_bar.addWidget(edit_record_button)


        delete_record_button = QPushButton("Delete Record")
        delete_record_button.clicked.connect(self.delete)
        self.status_bar.addWidget(delete_record_button)
        self.setStatusBar(self.status_bar)

        self.status_bar.hide()
        self.table.cellClicked.connect(self.status_bar_active)



    def load_data(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        #print(data)
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
        add_form = AddStudent(mainform=self)
        add_form.exec()

    def search_menu(self):
        search = SearchStudent(mainform=self)
        search.exec()

    def edit_student(self):
        edit_form = EditDialog(mainform=self)
        edit_form.exec()

    def delete(self):
        print("hi")

    def status_bar_active(self):
        self.status_bar.show()


class EditDialog(QDialog):
    def __init__(self, mainform):
        super().__init__()
        self.setWindowTitle("Edit Record")
        self.mainform = mainform

        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter the student name")

        self.courses = QComboBox()
        course_list = ["Astronomy", "Biology", "Math", "Physics"]
        self.courses.addItems(course_list)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Enter the mobile number")

        submit = QPushButton("Submit")
        submit.clicked.connect(self.edit)


        layout = QVBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(self.courses)
        layout.addWidget(self.mobile)
        layout.addWidget(submit)

        self.setLayout(layout)

    def edit(self):
        print("ss")
        row = self.mainform.table.currentItem().row()
        row = str(row + 1)
        print(row)
        name = self.name.text()
        course = self.courses.currentText()
        mobile = self.mobile.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        # cursor.execute(f"SELECT * FROM students WHERE rowid = {row}")
        # print(cursor.fetchall())
        query = "UPDATE students SET id = ?, name = ?, course = ?, mobile = ? WHERE id = ?"
        cursor.execute(query, (row, name, course, mobile, row))
        connection.commit()
        cursor.close()
        connection.close()
        self.mainform.load_data()

class AddStudent(QDialog):
    def __init__(self, mainform):
        super().__init__()
        self.setWindowTitle("Add Student")

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

    def add(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        table_list = cursor.fetchall()
        length = len(table_list)
        ID = str(length + 1)

        cursor.execute("INSERT INTO students (id, name, course, mobile) VALUES (?, ? ,?, ?)",
                       (ID, self.name.text(), self.courses.currentText(), self.mobile.text()))
        connection.commit()
        cursor.close()
        connection.close()

        self.mainform.load_data()

class SearchStudent(QDialog):
    def __init__(self, mainform):
        super().__init__()
        self.mainform = mainform

        self.setWindowTitle("Search Student")

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)

        layout = QVBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search(self):
        searched_term = self.name.text()

        """connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name = ?", (searched_term,))
        result = cursor.fetchall()
        print(result)"""

        result_list = self.mainform.table.findItems(searched_term, Qt.MatchFlag.MatchFixedString)

        for item in result_list:
            self.mainform.table.item(item.row(), 1).setSelected(True)




app = QApplication(sys.argv)
main_form = MainForm()
main_form.show()
app.exec()
