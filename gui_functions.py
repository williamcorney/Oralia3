import mido,pickle,random,copy
from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,QPushButton,QListWidget,QRadioButton,QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import QTimer, pyqtSignal
class gui_functions (QWidget):
    green_signal = pyqtSignal(int)
    red_signal = pyqtSignal(int)
    note_off_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.pixmap_item = {}
        self.green_signal.connect(self.insert_green_note)
        self.red_signal.connect(self.insert_red_note)
        self.note_off_signal.connect(self.delete_notes)
        self.lastnote = 0
        self.previous_scale = None

    def go_button_clicked(self):

        self.get_theory()
    def note_handler(self, mididata):

        match self.theorymode:


            case "Notes":

                if mididata.type == "note_on":

                    if mididata.note % 12 == self.goodnotes:
                        self.green_signal.emit(mididata.note)
                    else:
                        self.red_signal.emit(mididata.note)
            case "Scales":

                if mididata.type == "note_on":
                    print ("good notes are " , self.goodnotes)
                    if mididata.note == self.goodnotes[0]:
                        self.goodnotes.pop(0)
                        self.green_signal.emit(mididata.note)
                        if len(self.goodnotes) == 0:
                            # self.score_increase()
                            self.go_button_clicked()
                    else:
                        print('trigger2')
                        self.red_signal.emit(mididata.note)


        if mididata.type == "note_off":
            self.note_off_signal.emit(mididata.note)


    def insert_green_note(self,note):

        self.xcord = self.Theory2["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
        self.pixmap_item[note] = QGraphicsPixmapItem(
            QPixmap("./Images/key_" + "green" + self.Theory2["NoteFilenames"][note % 12]))
        self.pixmap_item[note].setPos(self.xcord,0)


        self.scene.addItem(self.pixmap_item[note])

    def insert_red_note(self,note):

        self.xcord = self.Theory2["NoteCoordinates"][note % 12] + ((note // 12) - 4) * 239
        self.pixmap_item[note] = QGraphicsPixmapItem(
            QPixmap("./Images/key_" + "red" + self.Theory2["NoteFilenames"][note % 12]))
        self.pixmap_item[note].setPos(self.xcord,0)
        self.scene.addItem(self.pixmap_item[note])

    def delete_notes(self, note):

        match self.theorymode:
            case "Notes":
                self.scene.removeItem(self.pixmap_item[note])

            case "Scales":
                self.scene.removeItem(self.pixmap_item[note])



    def get_theory(self):

        match self.theorymode:

            case "Notes":

                self.random_values()

                self.goodnotes = self.int

                print ('Good Note: ', self.goodnotes)

            case "Scales":

                self.random_values()
                while self.current_scale == self.previous_scale:
                    self.random_values()
                self.goodnotes = (self.midi_note_scale_generator((self.Theory2["Scales"][self.type][self.int]),
                                                                 octaves=1, base_note=60))
                self.deepnotes = copy.deepcopy(self.goodnotes)
                self.previous_scale = self.current_scale


    def midi_note_scale_generator(self, notes, octaves=1, base_note=60, repeat_middle=False, include_descending=True):
        adjusted_notes = [note + base_note for note in notes]
        extended_notes = adjusted_notes[:]

        for octave in range(1, octaves):
            extended_notes.extend([note + 12 * octave for note in adjusted_notes[1:]])

        if include_descending:
            if repeat_middle:
                reversed_notes = extended_notes[::-1]
            else:
                reversed_notes = extended_notes[:-1][::-1]
            extended_notes.extend(reversed_notes)

        return extended_notes

    def random_values (self):

        match self.theorymode:
            case "Notes":
                self.type = random.choice(self.theory_subtype_list)
                self.notes =  self.Theory2["Notes"][self.type]
                self.int = (random.choice(self.notes))
                while self.lastnote == self.int:
                    self.int = (random.choice(self.notes))
                self.letter = (self.Theory2["Chromatic"][self.int])
                self.lastnote = self.int

            case "Scales":
                self.int = random.choice ([0,2,4,5,7,9,11])
                #self.int = random.randint(0, 11)
                self.letter = self.Theory2["Enharmonic"][self.int]
                self.type = random.choice(self.theory_subtype_list)
                self.current_scale = f"{self.letter} {self.type}"
                print ('Current scale: ', self.current_scale)

                print (self.letter)

            case "Triads":

                self.int = random.randint(0, 11)
                self.letter = self.Theory2["Enharmonic"][self.int]
                self.type = random.choice(self.theory_subtype_list)
                self.current_scale = f"{self.letter} {self.type}"
                self.inv= random.choice(self.invselected)

            case "Sevenths":


                self.int = random.randint(0, 11)
                self.letter = self.Theory2["Enharmonic"][self.int]
                self.type = random.choice(self.theory_subtype_list)
                self.current_scale = f"{self.letter} {self.type}"
                self.inv = random.choice(self.invselected)

            case "Modes":

                self.int = random.randint(0, 11)
                self.letter = self.Theory2["Enharmonic"][self.int]
                self.type = random.choice(self.theory_subtype_list)
                self.current_scale = f"{self.letter} {self.type}"
            case "Keys":

                # work in progress

                self.type = random.choice(self.theory_subtype_list)
                self.int = random.randint(0, 11)
                #print (self.Theory2["Theory"][self.type])
                #self.letter = self.Theory2["Theory"][self.type][self.int]
                key_value_pair = list(self.Theory2["Theory"][self.type].items())[self.int]
                print (key_value_pair)



