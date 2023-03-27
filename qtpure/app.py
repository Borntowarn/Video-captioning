#!/usr/bin/env python
import sys
import traceback

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from qtpure.buttonController import uploadController
from qtpure.design import Ui_MainWindow
from qtpure.design_second import Ui_MainWindow as final_window
from qtpure.dragController import dragEnterEvent, \
    dragLeaveEventWrapper, dragMoveEventWrapper, dropEventWrapper
def except_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
if __name__ == '__main__':
    app = QApplication([])
    style = open("qt_styles", mode="r", encoding='utf8')
    app.setStyleSheet(style.read())
    style.close()
    main_window = QMainWindow()

    window = Ui_MainWindow()
    window.setupUi(main_window)
    central = main_window.centralWidget()
    main_window.setAcceptDrops(True)
    main_window.dragLeaveEvent = dragLeaveEventWrapper(main_window,
                                                       window)
    main_window.dragEnterEvent = dragEnterEvent
    main_window.dragMoveEvent = dragMoveEventWrapper(main_window)
    main_window.setWindowTitle("Меню")
    new_window = QMainWindow()
    new_window_ui = final_window()
    new_window_ui.setupUi(new_window)
    new_window.setWindowTitle('Статистика')
    main_window.dropEvent = dropEventWrapper(main_window, window, new_window,
                                             new_window_ui)
    window.upload.clicked.connect(uploadController(main_window, new_window,
                                                   new_window_ui))
    new_window.closeEvent = lambda x: exit(0)
    main_window.setMinimumSize(800, 600)
    main_window.setWindowIcon(QIcon('../icon.jpg'))
    main_window.show()
    sys.excepthook = except_hook

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        raise e
    finally:
        traceback.print_exc()
        print("END")
