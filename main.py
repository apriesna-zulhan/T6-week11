"""
main.py
Entry point for Post Manager application.
"""

import sys
import os

# Add project root to Python path so subpackages resolve correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from ui.main_window import MainWindow


def main():
    # Enable high-DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Post Manager")
    app.setOrganizationName("pahrul.my.id")
    app.setStyle("Fusion")  # consistent base style across platforms

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
