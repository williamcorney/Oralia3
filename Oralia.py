import mido,os
from PyQt6.QtWidgets import QApplication
from gui_setup import gui_setup
from PyQt6.QtCore import QTimer
from functools import partial


class MainApp(gui_setup):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Oralia')

app = QApplication([])
window = MainApp()
window.show()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with mido.open_input(callback=window.note_handler) as inport: app.exec()
