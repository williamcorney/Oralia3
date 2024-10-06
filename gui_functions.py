from gui_setup import gui_setup
import mido,pickle
from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,QPushButton,QListWidget,QRadioButton,QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QFont

class gui_functions (gui_setup):
    def __init__(self):
        super().__init__()

        pass

    def note_handler(self, mididata):



        if mididata.type == "note_on":

            if mididata.note == 60:
                print ('match')



        if mididata.type == "note_off":
            if mididata.note == 60:
                self.notesoff.append(60)


        pass


    def setup_function_variables(self):
        pass




