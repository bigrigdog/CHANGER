from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        info_label = QLabel(
            "Dashboard: Overview of application status and activities")
        layout.addWidget(info_label)
