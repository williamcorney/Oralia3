import mido
from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,QPushButton,QListWidget,QRadioButton
from PyQt6.QtGui import QPixmap, QFont
class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test')
        # CREATE TAB WIDGET
        self.tab_widget = QTabWidget()
        # CREATE TABS
        self.practical_tab = QWidget()
        self.theory_tab = QWidget()
        self.settings_tab = QWidget()
        # ADD TABS
        self.tab_widget.addTab(self.practical_tab, "Practical")
        self.tab_widget.addTab(self.theory_tab, "Theory")
        self.tab_widget.addTab(self.settings_tab, "Settings")
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.East)
        # CREATE LAYOUTS
        self.practical_tab.layout = QVBoxLayout()
        self.theory_tab.layout = QVBoxLayout()
        self.settings_tab.layout = QVBoxLayout()
        # SET LAYOUTS
        self.practical_tab.setLayout(self.practical_tab.layout)
        self.theory_tab.setLayout(self.theory_tab.layout)
        self.settings_tab.setLayout(self.settings_tab.layout)
        # THESE ARE FOR PRACTICAL TAB
        self.listselector1 = QListWidget()
        self.listselector1.addItems(["Notes", "Scales", "Triads", "Sevenths", "Modes", "Keys"])


        self.listselector2 = QListWidget()
        self.listselector2.addItems(["Major", "Minor"])
        self.listselector3 = QListWidget()


        self.keyboard_label = QLabel("")
        self.keyboard_label.setPixmap(QPixmap("/Users/williamcorney/PycharmProjects/Oralia2/Images/keys.png"))
        self.practical_tab.horizontal = QHBoxLayout()
        self.practical_tab.horizontal.addWidget(self.listselector1,0)
        self.practical_tab.horizontal.addWidget(self.listselector2,0)
        self.practical_tab.horizontal.addWidget(self.listselector3,0)
        # ADD HORIZONTAL LAYOUT TO VERTICAL LAYOUT
        self.practical_tab.layout.addLayout(self.practical_tab.horizontal)
        self.practical_tab.layout.addWidget(self.keyboard_label)
        self.practical_tab.horizontal.vertical = QVBoxLayout()
        self.practical_tab.horizontal.addLayout(self.practical_tab.horizontal.vertical, 2)

        self.key_label = QLabel("C MAJOR")
        self.inversion_label = QLabel("ROOT")
        self.fingering_label = QLabel("1,2,3,1,2,3,4,5")
        self.score_label = QLabel("Score :")
        self.score_value = QLabel("1")
        self.go_button = QPushButton("Go")
        self.practical_tab.horizontal.vertical.addWidget(self.key_label)
        self.practical_tab.horizontal.vertical.addWidget(self.inversion_label)
        self.practical_tab.horizontal.vertical.addWidget(self.fingering_label)


        self.practical_tab.horizontal.vertical.horizontal = QHBoxLayout()
        self.practical_tab.horizontal.vertical.addLayout(self.practical_tab.horizontal.vertical.horizontal)
        self.practical_tab.horizontal.vertical.horizontal.addWidget(self.score_label)
        self.practical_tab.horizontal.vertical.horizontal.addWidget(self.score_value)
        self.practical_tab.horizontal.vertical.addWidget(self.go_button)


        self.theory_tab.horizontal1 = QHBoxLayout()
        self.theory_tab.horizontal2 = QHBoxLayout()
        self.theory_tab.horizontal3 = QHBoxLayout()
        self.theory_tab.horizontal4 = QHBoxLayout()

        # THESE ARE FOR THEORY TAB
        self.listselector4 = QListWidget()
        self.listselector5 = QListWidget()
        self.listselector4.addItems(['Scale  theory',"Note theory"])
        self.listselector5.addItems(["What key signature is this","How many flats and sharps does this key have","What note is this"])


        self.question_label = QLabel("Which musical scale has the key signature of")
        self.question_image = QLabel("Image")
        self.question_image.setPixmap(QPixmap("/Users/williamcorney/PycharmProjects/Oralia2/png/GMAJOR.png"))

        self.set_button = QPushButton("Set")
        self.choice_one = QRadioButton("C Major")
        self.choice_two = QRadioButton("D Major")
        self.choice_three = QRadioButton("E Major")
        self.choice_four = QRadioButton(" F Major")
        self.check_answer = QPushButton("Check Answer")

        self.theory_tab.layout.addLayout(self.theory_tab.horizontal1)
        self.theory_tab.layout.addLayout(self.theory_tab.horizontal2)
        self.theory_tab.layout.addLayout(self.theory_tab.horizontal3)
        self.theory_tab.layout.addLayout(self.theory_tab.horizontal4)
        self.theory_tab.horizontal1.addWidget(self.listselector4)
        self.theory_tab.horizontal1.addWidget(self.listselector5)
        self.theory_tab.horizontal1.addWidget(self.set_button)
        self.theory_tab.horizontal2.addWidget(self.question_label)
        self.theory_tab.horizontal2.addWidget(self.question_image)
        self.theory_tab.horizontal3.addWidget(self.choice_one)
        self.theory_tab.horizontal3.addWidget(self.choice_two)
        self.theory_tab.horizontal4.addWidget(self.choice_three)
        self.theory_tab.horizontal4.addWidget(self.choice_four)
        self.theory_tab.layout.addWidget(self.check_answer)

        # SET QTABWIDGET AS THE CENTRAL WIDGET
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.tab_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()
