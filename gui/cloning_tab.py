from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox
from utils.voice_cloning_utils import clone_voice

class CloningTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.text_edit = QTextEdit("Enter text here to synthesize speech...")
        layout.addWidget(self.text_edit)

        self.clone_button = QPushButton("Clone Voice")
        self.clone_button.clicked.connect(self.on_clone_voice)
        layout.addWidget(self.clone_button)

        self.result_label = QLabel("Click 'Clone Voice' to process the text.")
        layout.addWidget(self.result_label)

    def on_clone_voice(self):
        input_text = self.text_edit.toPlainText()
        try:
            cloned_audio = clone_voice(input_text)
            self.result_label.setText("Cloning successful. Check the output folder.")
            # Assuming you have a function to handle the playback or saving of cloned audio
        except Exception as e:
            QMessageBox.critical(self, "Error", "Failed to clone voice: " + str(e))
            self.result_label.setText("An error occurred. Please try again.")
