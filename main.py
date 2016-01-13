from PyQt4.QtGui import *
import PyQt4
from MainIU import MainWindow
import logging
import GlobalVar



ImagePaths = []

def main():
    import sys
    GlobalVar.logger = logging.getLogger('ImageManagementLogger')
    hdlr = logging.FileHandler('/var/tmp/ImageMangementLog.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    GlobalVar.logger.addHandler(hdlr)
    GlobalVar.logger.setLevel(logging.WARNING)
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
