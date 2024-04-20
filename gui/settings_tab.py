from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Settings: Adjust application settings."))
