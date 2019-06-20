import sys
import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from ui import gui
from core.config import PATH
import core.fileHandler as fh
from core.cube import Cube


class UCastApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(UCastApp, self).__init__()
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.cubes = []

        self.ui.btnLoadDay.clicked.connect(self._loadDayPressed)
        self.ui.btnSaveClean.clicked.connect(self._saveFile)
        self.ui.btnUnload.clicked.connect(self._unloadPressed)
        self.ui.ddFeature.activated['QString'].connect(lambda text:
                                                        self.ui.gbFeatures.hide()
                                                        if text == "VIL"
                                                        else self.ui.gbFeatures.show())
        self.populate_list()

    def _saveFile(self):
        for date, loaded, clean, ts, x, y, feats, ext, row_idx in self._get_selected():
            fname = (date + "(" + ts + "," + x + "," + y + "," + feats + ")-" + clean + ext)
            if loaded != "True" or ext != ".cube":
                QMessageBox.warning(self,
                                    "Invalid data",
                                    "Data has to be loaded and extention must be .cube")
                return
            cidx = self._loaded_index((ts, x, y, feats), clean, fname)
            self.cubes[cidx].save_data()

    def _unloadPressed(self):
        selected = self._get_selected()
        if not self._are_you_sure("Are you sure?",
                                    ("You are about to unload %d file(s). "
                                        "Loading them back might take some time. "
                                        "Are you sure you want to unload them?") % len(selected)):
            return

        for date, loaded, clean, ts, x, y, feats, ext, row_idx in selected:
            fname = (date + "(" + ts + "," + x + "," + y + "," + feats + ")-" + clean + ext)
            for cube in self.cubes:
                cidx = self._loaded_index((ts, x, y, feats), clean, fname)
                if cidx != -1:
                    self.cubes.pop(cidx)
            self.ui.tableFiles.setItem(row_idx, 1, QTableWidgetItem(str(False)))
            self.ui.tableFiles.setItem(row_idx, 7, QTableWidgetItem(".npz"))

    def _loadDayPressed(self):
        for date, loaded, clean, ts, x, y, feats, ext, row_idx in self._get_selected():
            fname = (date + "(" + ts + "," + x + "," + y + "," + feats + ")-" + clean + ext)

            # Check to see if data is already loaded
            if self._loaded_index((ts, x, y, feats), clean, fname) != -1:
                if not self._are_you_sure("Data may be loaded",
                                            ("This data is already loaded. "
                                                "Are you sure you want to reload it? "
                                                "(it might take a while)")):
                    print("I was not sure")
                    continue
            try:
                if ext == ".npz":
                    c = Cube(date, clean, fh.load_one(PATH + "/" + fname))
                    c.save()
                elif ext == ".cube":
                    c = Cube.load(PATH + "/" + fname)
            except MemoryError as memerr:
                print(memerr)
                return
            # Set Loaded Column to True
            self.cubes.append(c)
            if loaded == "False":
                self.ui.tableFiles.setItem(row_idx,  # row
                                            1,  # column (Loaded)
                                            QTableWidgetItem(str(True)))
                self.ui.tableFiles.setItem(row_idx,  # row
                                            7,  # column (Extention)
                                            QTableWidgetItem(".cube"))
            else:
                self._add_file_to_table(fname.rsplit(".", 1)[0] + ".cube")
                self.ui.tableFiles.setItem(self.ui.tableFiles.rowCount() - 1,  # row
                                            1,  # column (Loaded)
                                            QTableWidgetItem(str(True)))
            print(self.cubes)

    def _get_selected(self):
        selected = []
        selected_widget = self.ui.tableFiles.selectedItems()
        for idx in range(0, len(selected_widget), self.ui.tableFiles.columnCount()):
            cols = [selected_widget[idx + cidx].text()
                            for cidx in range(self.ui.tableFiles.columnCount())]
            row = cols + [selected_widget[idx].row()]
            selected.append(row)
        return selected

    def populate_list(self):
        self.ui.tableFiles.clearContents()
        for r in range(self.ui.tableFiles.rowCount()):
            self.ui.tableFiles.removeRow(r)
        for filename in os.listdir(PATH):
            if filename.endswith(".npz"):  # or filename.endswith(".cube"):
                self._add_file_to_table(filename)

    def _add_file_to_table(self, filename):
        for sep in "(,).":
            filename = filename.replace(sep, ";")
        date, ts, x, y, feats, clean, ext = filename.split(sep=";")
        clean = clean[1:]
        ext = "." + ext
        loaded = False
        row = (date, loaded, clean, ts, x, y, feats, ext)

        new_row_idx = self.ui.tableFiles.rowCount()
        self.ui.tableFiles.insertRow(new_row_idx)
        for cidx in range(self.ui.tableFiles.columnCount()):
            self.ui.tableFiles.setItem(new_row_idx, cidx, QTableWidgetItem(str(row[cidx])))

    def _are_you_sure(self, title, question):
        reply = QMessageBox.question(self, title, question, QMessageBox.Yes | QMessageBox.No)
        return reply == QMessageBox.Yes

    def _loaded_index(self, shape, clean, datapath):
        shape = (int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3]))
        fname_no_ext = datapath.rsplit(".", 1)[0]
        for cidx in range(len(self.cubes)):
            c = self.cubes[cidx]
            if (shape == c.shape
                    and clean == c.clean
                    and fname_no_ext == c.datapath.rsplit(".", 1)[0].rsplit("/", 1)[1]):
                return cidx
        return -1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UCastApp()
    window.show()
    sys.exit(app.exec_())
