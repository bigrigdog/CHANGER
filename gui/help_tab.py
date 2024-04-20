from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Help: Get support and documentation."))
