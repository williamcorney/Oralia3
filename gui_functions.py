import mido,pickle,random,copy
from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,QPushButton,QListWidget,QRadioButton,QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtCore import Qt
class gui_functions (QWidget):
    green_signal = pyqtSignal(int)
    red_signal = pyqtSignal(int)
    note_off_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        with open('data.pkl', 'rb') as file: self.Theory2 = pickle.load(file)

        self.setWindowTitle('Piano Training')
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
        # self.listselector2.addItems(["Naturals","Sharps","Flats","Major", "Minor","Melodic","Harmonic"])
        self.listselector3 = QListWidget()
        self.listselector1.itemSelectionChanged.connect(self.theorychanged)
        self.listselector2.itemSelectionChanged.connect(self.theorysubtypechanged)
        self.listselector1.clicked.connect(self.theory_type_clicked)

        # self.keyboard_label = QLabel("")
        # self.keyboard_label.setPixmap(QPixmap("/Users/williamcorney/PycharmProjects/Oralia2/Images/keys.png"))

        self.practical_tab.horizontal = QHBoxLayout()
        self.practical_tab.horizontal.addWidget(self.listselector1, 0)
        self.practical_tab.horizontal.addWidget(self.listselector2, 0)
        self.practical_tab.horizontal.addWidget(self.listselector3, 0)
        # ADD HORIZONTAL LAYOUT TO VERTICAL LAYOUT
        self.practical_tab.layout.addLayout(self.practical_tab.horizontal)
        self.create_piano()
        #        self.practical_tab.layout.addWidget(self.keyboard_label)
        self.practical_tab.horizontal.vertical = QVBoxLayout()
        self.practical_tab.horizontal.addLayout(self.practical_tab.horizontal.vertical, 2)

        self.key_label = QLabel("C MAJOR")
        self.inversion_label = QLabel("ROOT")
        self.fingering_label = QLabel("1,2,3,1,2,3,4,5")
        self.score_label = QLabel("Score :")
        self.score_value = QLabel("1")
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.go_button_clicked)
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
        self.listselector4.addItems(['Scale  theory', "Note theory"])
        self.listselector5.addItems(
            ["What key signature is this", "How many flats and sharps does this key have", "What note is this"])

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
                    if mididata.note == self.goodnotes[0]:
                        self.goodnotes.pop(0)
                        self.green_signal.emit(mididata.note)
                        if len(self.goodnotes) == 0:

                            self.go_button_clicked()
                    else:

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
                self.key_label.setText(self.current_scale)
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



    def theorychanged (self):
        self.theorymode = (self.listselector1.selectedItems()[0].text())

    def theorysubtypechanged(self):
        self.theory_subtype = self.listselector2.selectedItems()

        self.theory_subtype_list = [item.text() for item in self.theory_subtype]



        match self.theorymode:
            case "Notes":
                pass
            case "Scales":
                pass
            case "Triads":
                self.listselector3.clear()
                self.listselector3.addItems(["Root", "First", "Second"])
            case "Sevenths":
                self.listselector3.clear()
                self.listselector3.addItems(["Root", "First", "Second", "Third"])

    def theory_type_clicked(self):
        self.listselector3.clear()
        self.listselector2.clear()
        match self.listselector1.currentItem().text():

            case "Notes":
                self.listselector2.addItems(["Naturals", "Sharps", "Flats"])
            case "Scales":
                self.listselector2.addItems(["Major", "Minor", "Melodic Minor", "Harmonic Minor"])
            case "Triads":
                self.listselector2.addItems(["Major", "Minor"])
            case "Sevenths":
                self.listselector2.addItems(["Maj7", "Min7", "7", "Dim7", "m7f5"])
            case "Modes":
                self.listselector2.addItems(
                    ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"])
            case "Keys":
                self.listselector2.addItems(["Major", "Minor"])
    def create_piano (self):
        # Create a QGraphicsScene
        self.scene = QGraphicsScene()

        # Add background image
        self.background_pixmap = QPixmap("/Users/williamcorney/PycharmProjects/Oralia2/Images/keys.png")
        self.background_item = QGraphicsPixmapItem(self.background_pixmap)
        self.scene.addItem(self.background_item)
        self.view = QGraphicsView(self.scene)

        self.practical_tab.layout.addWidget(self.view)
        self.view.setFixedSize(self.background_pixmap.size())  # Set the view size to match the background image
        self.view.setSceneRect(0, 0, self.background_pixmap.width(), self.background_pixmap.height())
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

