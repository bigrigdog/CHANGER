from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Training: Train new models or refine existing ones."))
