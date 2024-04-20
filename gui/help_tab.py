from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Help: Get support and documentation."))
