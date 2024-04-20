from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class LibraryTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Library: Manage your voice models here."))
