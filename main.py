import sys
from PySide6.QtWidgets import QApplication
import os
from MainWindowCode import myWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = myWindow()
    main_window.fill_combo_box()
    main_window.showTableData()
    main_window.show()
    sys.exit(app.exec())