from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMenuBar, QStatusBar, \
                            QGridLayout, QToolBar, QPushButton, QTableWidget, QTableWidgetItem, \
                            QDialog, QLineEdit, QComboBox, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtGui import QIcon, QAction, QMouseEvent
from PyQt6.QtCore import QSize, Qt, QEvent
import sys
import mysql.connector


class DatabaseConnection:

    def __init__(self, host="localhost", user="root", password="pythoncourse", database="school"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connection(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        return connection

    @staticmethod
    def cursor(connection):
        cursor = connection.cursor()
        return cursor


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

        self.about_button = QAction("About")
        self.about_button.triggered.connect(self.about)

        file_menu = menubar.addMenu("File")
        help_menu = menubar.addMenu("Help")

        file_menu.addAction(self.add_button)
        file_menu.addAction(self.search_button)

        help_menu.addAction(self.about_button)

        self.table = TableWidget(self)
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

        self.status_bar = StatusBar()

        edit_record_button = QPushButton("Edit Record")
        edit_record_button.clicked.connect(self.edit_student)
        self.status_bar.addWidget(edit_record_button)

        delete_record_button = QPushButton("Delete Record")
        delete_record_button.clicked.connect(self.delete_student)
        self.status_bar.addWidget(delete_record_button)
        self.setStatusBar(self.status_bar)

        self.status_bar.hide()

    def mousePressEvent(self, event):
        self.status_bar.hide()

    def load_data(self):
        connection = DatabaseConnection().connection()
        cursor = DatabaseConnection.cursor(connection)
        # connection = sqlite3.connect("database.db")
        # cursor = connection.cursor()
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
        add_form = AddStudent(main_form=self)
        add_form.exec()

    def search_menu(self):
        search = SearchStudent(main_form=self)
        search.exec()

    def about(self):
        about_menu = AboutDialog()
        about_menu.exec()

    def edit_student(self):
        edit_form = EditDialog(main_form=self)
        edit_form.exec()

    def delete_student(self):
        delete_form = DeleteDialog(main_form=self)
        delete_form.exec()

    def status_bar_active(self):
        self.status_bar.show()


class StatusBar(QStatusBar):
    def mousePressEvent(self, event):
        pass


class TableWidget(QTableWidget):

    def __init__(self, main_form):
        super().__init__()
        self.main_form = main_form

    def mousePressEvent(self, event):
        row_count = self.rowCount()
        x_column = event.pos().x()
        y_row = event.pos().y()

        # print(x_column)
        # print(y_row)

        if event.pos().x() >= 399 or event.pos().y() >= row_count * 30:
            self.main_form.status_bar.hide()

        else:
            value1 = 0
            value2 = 30
            range_list = []
            dict1 = {}
            row = 0
            column = 0

            for index in range(0, row_count):
                dict1[index] = range(value1, value2)
                range_list.append(dict1[index])
                value1 = value1 + 30
                value2 = value2 + 30

            for index, item in enumerate(range_list):
                if y_row in item:
                    row = index
                    break

            if x_column in range(1, 100):
                column = 0
                # return column

            elif x_column in range(101, 200):
                column = 1

            elif x_column in range(201, 300):
                column = 2

            elif x_column in range(301, 400):
                column = 3

            # print(column)
            # print(row)

            # print(self.item(row, column).text())

            item = self.item(row, column)
            self.setCurrentItem(item)
            self.main_form.status_bar_active()


class EditDialog(QDialog):
    def __init__(self, main_form):
        super().__init__()
        self.setWindowTitle("Edit Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.main_form = main_form
        self.row = 0

        name, course, mobile = self.existing_data()

        self.name = QLineEdit()
        self.name.setText(name)

        self.courses = QComboBox()
        course_list = ["Astronomy", "Biology", "Math", "Physics"]
        self.courses.addItems(course_list)
        # self.courses.itemText(course)
        self.courses.setCurrentText(course)

        self.mobile = QLineEdit()
        self.mobile.setText(mobile)

        submit = QPushButton("Submit")
        submit.clicked.connect(self.edit)

        layout = QVBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(self.courses)
        layout.addWidget(self.mobile)
        layout.addWidget(submit)

        self.setLayout(layout)

    def existing_data(self):
        row = self.main_form.table.currentItem().row()
        row = row + 1
        # print(row)

        connection = DatabaseConnection().connection()
        cursor = DatabaseConnection.cursor(connection)
        cursor.execute("SELECT * FROM students WHERE id = %s", (row,))
        result = cursor.fetchall()
        result = list(result)
        # print(result)

        name = result[0][1]
        course = result[0][2]
        mobile = result[0][3]
        # print(name, course, mobile)

        cursor.close()
        connection.close()
        return name, course, mobile

    def edit(self):
        if self.main_form.table.currentItem():
            row = self.main_form.table.currentItem().row()
            row = str(row + 1)
            self.row = row
        else:
            row = self.row

        print(row)
        name = self.name.text()
        course = self.courses.currentText()
        mobile = self.mobile.text()

        connection = DatabaseConnection().connection()
        cursor = DatabaseConnection.cursor(connection)
        # cursor.execute(f"SELECT * FROM students WHERE rowid = {row}")
        # print(cursor.fetchall())
        query = "UPDATE students SET id = %s, name = %s, course = %s, mobile = %s WHERE id = %s"
        cursor.execute(query, (row, name, course, mobile, row))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_form.load_data()


class DeleteDialog(QDialog):
    def __init__(self, main_form):
        # print("hi")
        super().__init__()
        self.main_form = main_form
        self.setWindowTitle("Delete Row")
        # self.setFixedWidth(400)
        # self.setFixedHeight(100)

        confirmation = QLabel("Are you sure you want to delete the current row?")
        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.delete)
        no_button = QPushButton("No")
        no_button.clicked.connect(self.close_delete)

        layout = QGridLayout()
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(no_button, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

    def delete(self):
        current_row = self.main_form.table.currentRow()
        id = self.main_form.table.item(current_row, 0).text()
        print(id)

        # print(current_row)

        connection = DatabaseConnection().connection()
        cursor = DatabaseConnection.cursor(connection)
        cursor.execute("DELETE FROM students WHERE id = %s", (id, ))
        connection.commit()

        self.main_form.load_data()

        cursor.close()
        connection.close()

        self.close()

        delete_message = QMessageBox()
        delete_message.setWindowTitle("Success!!")
        delete_message.setText("Row has been successfully deleted")
        delete_message.exec()

    def close_delete(self):
        self.close()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        content = """
                    Student Database Management System
                    Build #1, built on January 16, 2024.
                    Copyright © Me
                    This app was created during Python course.
        """

        self.setText(content)

        self.setIcon(QMessageBox.Icon.Information)


class AddStudent(QDialog):
    def __init__(self, main_form):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.main_form = main_form
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
        connection = DatabaseConnection().connection()
        cursor = DatabaseConnection.cursor(connection)
        cursor.execute("SELECT * FROM students")
        table_list = cursor.fetchall()
        length = len(table_list)
        id = str(length + 1)

        cursor.execute("INSERT INTO students (id, name, course, mobile) VALUES (%s, %s ,%s, %s)",
                       (id, self.name.text(), self.courses.currentText(), self.mobile.text()))
        connection.commit()
        cursor.close()
        connection.close()

        self.main_form.load_data()


class SearchStudent(QDialog):
    def __init__(self, main_form):
        super().__init__()
        self.main_form = main_form

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

        result_list = self.main_form.table.findItems(searched_term, Qt.MatchFlag.MatchFixedString)

        for item in result_list:
            self.main_form.table.item(item.row(), 1).setSelected(True)


app = QApplication(sys.argv)
main_form = MainForm()
main_form.show()
app.exec()
