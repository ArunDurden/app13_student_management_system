import sys

from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QWidget, QPushButton, QComboBox

class Form(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Average Speed Calculator")
        layout = QGridLayout()

        distance_label = QLabel("Distance:")
        layout.addWidget(distance_label, 0, 0)

        self.distance_line_edit = QLineEdit()
        layout.addWidget(self.distance_line_edit, 0, 1)

        self.dropdown = QComboBox()
        self.dropdown.addItem("Metric (km)")
        self.dropdown.addItem("Imperial (miles)")
        layout.addWidget(self.dropdown, 0, 2)

        time_label = QLabel("Time (hours):")
        layout.addWidget(time_label, 1, 0)

        self.time_line_edit = QLineEdit()
        layout.addWidget(self.time_line_edit, 1, 1)

        self.result = QLabel("")
        layout.addWidget(self.result, 3, 0)

        self.calculate = QPushButton("Calculate")

        self.calculate.clicked.connect(lambda: self.calculate_speed())
        layout.addWidget(self.calculate, 2, 1)

        self.setLayout(layout)

    def calculate_speed(self):
        speed = ""
        if self.dropdown.currentText() == "Metric (km)":
            speed = float(self.distance_line_edit.text()) / float(self.time_line_edit.text())
            speed = round(speed, 2)
            speed = str(speed)
            content = f"Average Speed: {speed} km/h"

        else:
            speed = int(self.distance_line_edit.text()) / int(self.time_line_edit.text())
            speed = speed * 0.621
            speed = round(speed, 2)
            speed = str(speed)
            content = f"Average Speed: {speed} mph"

        self.result.setText(content)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec()