import math
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from tahaschenrechner_sr1 import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.current_value = ""
        self.stored_value = ""
        self.current_operator = None
        self.operator_pressed = False
        self.result_shown = False
        self.ui.labellcd.setText("")
        self.ui.label2.setText("")

        self.ui.pb_f_2.clicked.connect(self.toogle_lcd)
        self.ui.pb_cec.clicked.connect(self.clear_display)
        self.ui.pb_pro.clicked.connect(self.calculate_percentage)
        self.ui.pb_ka.clicked.connect(lambda: self.add_bracket("("))
        self.ui.pb_kg.clicked.connect(lambda: self.add_bracket(")"))

        self.ui.pb_0.clicked.connect(lambda: self.add_number(0))
        self.ui.pb_1.clicked.connect(lambda: self.add_number(1))
        self.ui.pb_2.clicked.connect(lambda: self.add_number(2))
        self.ui.pb_3.clicked.connect(lambda: self.add_number(3))
        self.ui.pb_4.clicked.connect(lambda: self.add_number(4))
        self.ui.pb_5.clicked.connect(lambda: self.add_number(5))
        self.ui.pb_6.clicked.connect(lambda: self.add_number(6))
        self.ui.pb_7.clicked.connect(lambda: self.add_number(7))
        self.ui.pb_8.clicked.connect(lambda: self.add_number(8))
        self.ui.pb_9.clicked.connect(lambda: self.add_number(9))

        self.ui.pb_ad.clicked.connect(lambda: self.set_operator("+"))
        self.ui.pb_sub.clicked.connect(lambda: self.set_operator("-"))
        self.ui.pb_mul.clicked.connect(lambda: self.set_operator("*"))
        self.ui.pb_div.clicked.connect(lambda: self.set_operator("/"))

        self.ui.pb_erg.clicked.connect(self.calculate_result)
        self.ui.pb_ko.clicked.connect(self.add_coma)
        self.ui.pb_vor.clicked.connect(self.add_vor)
        self.ui.pb_wur.clicked.connect(self.calculate_square_root)

    def toogle_lcd(self):
        if self.ui.pb_f_2.isChecked():
            self.ui.labellcd.setText("0")
        else:
            self.ui.labellcd.setText("")
            self.ui.label2.setText("")
            self.current_value = ""

    def add_number(self, number):
        if self.result_shown or self.current_value == "":
            self.current_value = str(number)
            self.result_shown = False
        else:
            self.current_value += str(number)

        self.ui.labellcd.setText(self.current_value)

    def set_operator(self, operator):
        if self.current_value:
            self.stored_value += self.current_value + " " + operator + " "
            self.ui.label2.setText(self.stored_value)
            self.current_value = ""
        elif self.stored_value and self.stored_value.strip()[-1] in "+-*/":
            self.stored_value = self.stored_value.strip()[:-1] + operator + " "
            self.ui.label2.setText(self.stored_value)

    def calculate_result(self):
        if self.stored_value and self.current_value:
            expression = self.stored_value + self.current_value
            try:
                expression = expression.replace("√", "math.sqrt(")
                expression = expression.replace("math.sqrt(", "math.srt(")
                expression = expression + ")" * expression.count("math.sqrt(")
                expression = expression.replace(" ", "")
                result = eval(expression, {"math" : math})
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"{expression} = {result}")
                self.current_value = str(result)
                self.stored_value = ""
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
        else:
            self.ui.labellcd.setText("ERROR")

    def add_coma(self):
        if "." not in self.current_value:
            self.current_value += "."
            self.ui.labellcd.setText(self.current_value)

    def add_vor(self):
        if self.current_value and self.current_value[0] != "-":
            self.current_value = "-" + self.current_value
        elif self.current_value and self.current_value[0] == "-":
            self.current_value = self.current_value[1:]
        self.ui.labellcd.setText(self.current_value)

    def add_bracket(self, bracket):
        self.current_value += bracket
        self.ui.labellcd.setText(self.current_value)

    def clear_display(self):
        self.ui.labellcd.setText("0")
        self.ui.label2.setText("")
        self.current_value = ""
        self.stored_value = ""
        self.current_operator = None
        self.result_shown = False

    def calculate_percentage(self):
        try:
            if self.stored_value and self.current_value:
                base_value = float(self.stored_value)
                percentage = float(self.current_value) / 100 * base_value
                self.current_value = str(percentage)
                self.ui.labellcd.setText(self.current_value)
            elif self.current_value:
                percentage = float(self.current_value) / 100
                self.current_value = str(percentage)
                self.ui.labellcd.setText(self.current_value)
            else:
                self.ui.labellcd.setText("ERROR")
        except Exception:
            self.ui.labellcd.setText("ERROR")

    def calculate_square_root(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                if value >= 0:
                    self.current_value = f"√({value})"
                    self.ui.labellcd.setText((self.current_value)[:11])
                    self.ui.label2.setText(f"√{value}")
                else:
                    self.ui.labellcd.setText("ERROR")

            except Exception:
                self.ui.labellcd("ERROR")

        else:
            self.ui.labellcd.setText("ERROR")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())