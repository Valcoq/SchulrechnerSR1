import math
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QPixmap
from tahaschenrechner_sr1 import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.current_value = ""
        self.stored_value = ""
        self.memory_value = 0
        self.memory_used = False
        self.current_operator = None
        self.operator_pressed = False
        self.result_shown = False
        self.entering_exponent = False
        self.exponent_value = ""
        self.angle_mode = "DEG"  
        self.ui.labellcd.setText("")
        self.ui.label2.setText("DEG")  

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
        self.ui.pb_wur.clicked.connect(self.add_square_root)
        self.ui.pb_x2.clicked.connect(self.calculate_square)
        self.ui.pb_1x.clicked.connect(self.calculate_reciprocal)
        self.ui.pb_pi.clicked.connect(self.add_pi)
        self.ui.pb_m.clicked.connect(self.memory_add)
        self.ui.pb_xm.clicked.connect(self.memory_subtract)
        self.ui.pb_mr.clicked.connect(self.memory_recall)
        self.ui.pb_eex.clicked.connect(self.start_exponent_entry)

        self.ui.pb_sin.clicked.connect(self.calculate_sin)
        self.ui.pb_cos.clicked.connect(self.calculate_cos)
        self.ui.pb_tan.clicked.connect(self.calculate_tan)
        self.ui.pb_sin.clicked.connect(self.calculate_arcsin)
        self.ui.pb_cos.clicked.connect(self.calculate_arccos)
        self.ui.pb_tan.clicked.connect(self.calculate_arctan)
        self.ui.pb_ig.clicked.connect(self.calculate_log_or_10x)  
        self.ui.pb_in.clicked.connect(self.calculate_ln_or_ex)    
        self.ui.pb_f_3.clicked.connect(self.toggle_angle_mode)    

    def toogle_lcd(self):
        if self.ui.pb_f_2.isChecked():
            self.ui.labellcd.setText("0")
        else:
            self.ui.labellcd.setText("")
            self.ui.label2.setText(self.angle_mode) 
            self.current_value = ""

    def add_number(self, number):
        if self.entering_exponent:
            self.exponent_value += str(number)
            self.ui.labellcd.setText(f"{self.current_value} {self.exponent_value}")
        else:
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
        if self.entering_exponent:
            self.finalize_exponent_entry()
        if self.stored_value and self.current_value:
            expression = self.stored_value + self.current_value
            try:
                expression = expression.replace("√", "math.sqrt(")
                expression = expression + ")" * expression.count("math.sqrt(")
                expression = expression.replace("π", "math.pi")
                expression = expression.replace("^", "**")
                expression = expression.replace(" ", "")
                result = eval(expression, {"math": math})
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"{expression} = {result}")
                self.current_value = str(result)
                self.stored_value = ""
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Ungültige Eingabe")

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
        self.ui.label2.setText(self.angle_mode)  
        self.current_value = ""
        self.stored_value = ""
        self.current_operator = None
        self.result_shown = False
        self.entering_exponent = False
        self.exponent_value = ""

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

    def add_square_root(self):  
        if self.current_value:
            self.current_value = f"√{self.current_value}"
            self.ui.labellcd.setText(self.current_value)
            self.ui.label2.setText(self.current_value)
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_square(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                result = value ** 2
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"{value}² = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_reciprocal(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                if value == 0:
                    self.ui.labellcd.setText("ERROR")
                    self.ui.label2.setText("ERROR: Division durch Null")
                else:
                    result = 1 / value
                    self.ui.labellcd.setText(str(result)[:11])
                    self.ui.label2.setText(f"1/{value} = {result}")
                    self.current_value = str(result)
                    self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def add_pi(self):
        pi_value = str(math.pi)[:11]
        self.current_value = pi_value
        self.ui.labellcd.setText(self.current_value)
        self.ui.label2.setText("π")

    def memory_add(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                self.memory_value += value
                self.memory_used = True
                self.update_memory_display()
            except Exception:
                self.ui.labellcd.setText("ERROR")

    def memory_subtract(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                self.memory_value -= value
                self.memory_used = True
                self.update_memory_display()
            except Exception:
                self.ui.labellcd.setText("ERROR")

    def memory_recall(self):
        self.current_value = str(self.memory_value)
        self.ui.labellcd.setText(self.current_value)
        self.update_memory_display()

    def memory_clear(self):
        self.memory_value = 0
        self.memory_used = False
        self.update_memory_display()

    def update_memory_display(self):
        if self.memory_used:
            self.ui.label2.setText("M")
        else:
            self.ui.label2.setText(self.angle_mode)  

    def start_exponent_entry(self):
        self.entering_exponent = True
        self.exponent_value = ""
        self.ui.labellcd.setText(f"{self.current_value} {self.exponent_value}")

    def finalize_exponent_entry(self):
        if self.entering_exponent and self.exponent_value:
            try:
                mantissa = float(self.current_value)
                exponent = int(self.exponent_value)
                scientific_number = mantissa * (10 ** exponent)
                self.current_value = str(scientific_number)
                self.ui.labellcd.setText(self.current_value)
                self.entering_exponent = False
                self.exponent_value = ""
            except Exception:
                self.ui.labellcd.setText("ERROR")
                self.entering_exponent = False
                self.exponent_value = ""

    def calculate_sin(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                if self.angle_mode == "DEG":
                    value = math.radians(value)
                elif self.angle_mode == "GRD":
                    value = math.radians(value * 0.9)  
                result = math.sin(value)
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"sin({self.current_value}) = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_cos(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                if self.angle_mode == "DEG":
                    value = math.radians(value)
                elif self.angle_mode == "GRD":
                    value = math.radians(value * 0.9)  
                result = math.cos(value)
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"cos({self.current_value}) = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_tan(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                if self.angle_mode == "DEG":
                    value = math.radians(value)
                elif self.angle_mode == "GRD":
                    value = math.radians(value * 0.9)  
                result = math.tan(value)
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"tan({self.current_value}) = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_arcsin(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                result = math.asin(value)
                if self.angle_mode == "DEG":
                    result = math.degrees(result)
                elif self.angle_mode == "GRD":
                    result = math.degrees(result) * 1.111111  
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"arcsin({self.current_value}) = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_arccos(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                result = math.acos(value)
                if self.angle_mode == "DEG":
                    result = math.degrees(result)
                elif self.angle_mode == "GRD":
                    result = math.degrees(result) * 1.111111  
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"arccos({self.current_value}) = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_arctan(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                result = math.atan(value)
                if self.angle_mode == "DEG":
                    result = math.degrees(result)
                elif self.angle_mode == "GRD":
                    result = math.degrees(result) * 1.111111 
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"arctan({self.current_value}) = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_log_or_10x(self):
        if self.angle_mode == "GRD":
            self.calculate_10x() 
        else:
            self.calculate_log() 

    def calculate_ln_or_ex(self):
        if self.angle_mode == "GRD":
            self.calculate_ex()  
        else:
            self.calculate_ln()  

    def calculate_log(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                result = math.log10(value)
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"log({self.current_value}) = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_ln(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                result = math.log(value)
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"ln({self.current_value}) = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_10x(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                result = 10 ** value
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"10^({self.current_value}) = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def calculate_ex(self):
        if self.current_value:
            try:
                value = float(self.current_value)
                result = math.exp(value)
                self.ui.labellcd.setText(str(result)[:11])
                self.ui.label2.setText(f"e^({self.current_value}) = {result}")
                self.current_value = str(result)
                self.result_shown = True
            except Exception as e:
                self.ui.labellcd.setText("ERROR")
                self.ui.label2.setText(f"ERROR: {str(e)}")
        else:
            self.ui.labellcd.setText("ERROR")
            self.ui.label2.setText("ERROR: Keine Eingabe")

    def toggle_angle_mode(self):
        if self.angle_mode == "DEG":
            self.angle_mode = "RAD"
        elif self.angle_mode == "RAD":
            self.angle_mode = "GRD"
        else:
            self.angle_mode = "DEG"
        self.ui.label2.setText(self.angle_mode) 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())