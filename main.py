import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget

from gui.cloning_tab import CloningTab
from gui.dashboard_tab import DashboardTab
from gui.help_tab import HelpTab
from gui.library_tab import LibraryTab
from gui.settings_tab import SettingsTab
from gui.training_tab import TrainingTab


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Voice Cloning GUI")
        # Set the geometry of the main window
        self.setGeometry(100, 100, 800, 600)
        self.table_widget = MainTabs(self)
        self.setCentralWidget(self.table_widget)


class MainTabs(QTabWidget):
    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        self.addTab(DashboardTab(), "Dashboard")
        self.addTab(CloningTab(), "Cloning")
        self.addTab(TrainingTab(), "Training")
        self.addTab(LibraryTab(), "Library")
        self.addTab(SettingsTab(), "Settings")
        self.addTab(HelpTab(), "Help")


def main():
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
