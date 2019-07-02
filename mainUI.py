import sys
import os
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from ui import gui
from core.config import PATH, IS_INVALID_R, IS_INVALID_V, Rs13, Vs13, VIL13
import core.fileHandler as fh
from core.cube import Cube
from core.plotter import Plotter
from core.cleaner import Cleaner
from DNN.learner import Learner


class UCastApp(QMainWindow):
    def __init__(self):
        super(UCastApp, self).__init__()
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.cubes = []


        for i in range(8):
            self.ui.tableFiles.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        # Signals
        self.ui.btnLoadDay.clicked.connect(self._loadDayPressed)
        self.ui.btnSaveClean.clicked.connect(self._saveFile)
        self.ui.btnUnload.clicked.connect(self._unloadPressed)
        self.ui.btnPlot.clicked.connect(self.plotPressed)
        self.ui.btnTrain.clicked.connect(self.trainPressed)
        self.ui.btnPredict.clicked.connect(self.predictPressed)
        self.ui.btnClean.clicked.connect(self.cleanPressed)

        self.ui.ddFeature.activated['QString'].connect(lambda text:
                                                        self.ui.gbFeatures.hide()
                                                        if text == "VIL"
                                                        else self.ui.gbFeatures.show())

        # Validators
        self.ui.txtEpoch.setValidator(QIntValidator(0, 10000, self.ui.txtEpoch))
        re_int_list = QRegExp("([0-9]+,)*[0-9]+")
        valid_re_int_list = QRegExpValidator(re_int_list)
        self.ui.txtTrainTimestamps.setValidator(valid_re_int_list)
        self.ui.txtPredictTimestamps.setValidator(valid_re_int_list)


        self.populate_list()

    def cleanPressed(self):
        selected = self._get_selected()
        if len(selected) != 1:
            QMessageBox.warning(self,
                                "Select only one!",
                                "Can only clean one dataset at a time!")
            return
        date, loaded, clean, ts, x, y, feats, ext, row_idx = selected[0]
        fname = (date + "(" + ts + "," + x + "," + y + "," + feats + ")-" + clean + ext)
        cidx = self._loaded_index((ts, x, y, feats), clean, fname)
        if cidx == -1:
            QMessageBox.warning(self,
                                "Fail!",
                                "Data is not loaded!")
            return
        if clean == "CLEAN" and not self._are_you_sure("Data is clean",
                                                        "Data is already marked as clean.Are " +
                                                        "you sure you want to search for invalid " +
                                                        "data points again and clean them?"):
            return
        if feats == "13":
            cleaner = Cleaner(Rs13, Vs13)
        elif feats == "24":
            cleaner = Cleaner(Rs24, Vs24)

        cleaner.clean_field(self.cubes[cidx].data, "V")
        self.cubes[cidx].clean="CLEAN"
        self.cubes[cidx].refresh_path()

        self.ui.tableFiles.setItem(row_idx,  # row
                                    1,  # column (Loaded)
                                    QTableWidgetItem(str(False)))

        fname = (date + "(" + ts + "," + x + "," + y + "," + feats + ")-" + "CLEAN" + ".MEMORY")
        self._add_file_to_table(fname)
        self.ui.tableFiles.setItem(self.ui.tableFiles.rowCount() - 1,  # row
                                    1,  # column (Loaded)
                                    QTableWidgetItem(str(True)))


    def predictPressed(self):
        selected = self._get_selected()
        if len(selected) != 1:
            QMessageBox.warning(self,
                                "Select only one!",
                                "Can only train on one dataset at a time!")
            return
        date, loaded, clean, ts, x, y, feats, ext, row_idx = selected[0]
        fname = (date + "(" + ts + "," + x + "," + y + "," + feats + ")-" + clean + ext)
        cidx = self._loaded_index((ts, x, y, feats), clean, fname)
        if cidx == -1:
            QMessageBox.warning(self,
                                "Fail!",
                                "Data is not loaded!")
            return
        try:
            timestamps = self._str_to_list(self.ui.txtPredictTimestamps.text(), ts)
        except ValueError as e:
            QMessageBox.warning(self, "Error!", str(e))
            return
        lrn = Learner(self.cubes[cidx].data)
        lrn.predict(timestamps)
        lrn.compute_errors()


    def trainPressed(self):
        selected = self._get_selected()
        if len(selected) != 1:
            QMessageBox.warning(self,
                                "Select only one!",
                                "Can only train on one dataset at a time!")
            return

        date, loaded, clean, ts, x, y, feats, ext, row_idx = selected[0]
        fname = (date + "(" + ts + "," + x + "," + y + "," + feats + ")-" + clean + ext)
        try :
            epochs = int(self.ui.txtEpoch.text())
            if epochs < 0:
                raise ValueError("Number of epochs can't be negative")
        except ValueError as e:
            QMessageBox.warning(self,
                                "Invalid number!",
                                "Invalid number!")
            return
        cidx = self._loaded_index((ts, x, y, feats), clean, fname)
        if cidx == -1:
            QMessageBox.warning(self,
                                "Fail!",
                                "Data not loaded")
            return
        try:
            timestamps = self._str_to_list(self.ui.txtTrainTimestamps.text(), ts)
        except ValueError as e:
            QMessageBox.warning(self, "Error!", str(e))
            return
        lrn = Learner(self.cubes[cidx].data)
        lrn.train(epochs, 1, timestamps)#[50, 63, 76, 89, 102, 115, 128, 141, 154, 167]
        #am folosit 3 epoci mici si 10 mari sau 10 mari si 3 mici pentru a obtine 30 de epoci in final
        #cu batch size mai mare merge mai repede, la 1010 am avut 400 de epoci in total



    def plotPressed(self):
        cbIgnore = self.ui.cbIgnore.checkState() == Qt.Checked
        levels = [self.ui.cbLevel1, self.ui.cbLevel2, self.ui.cbLevel3,
                    self.ui.cbLevel4, self.ui.cbLevel6, self.ui.cbLevel7]
        feat = self.ui.ddFeature.currentText()
        fidxs = [l_idx for l_idx in range(len(levels)) if levels[l_idx].checkState() == Qt.Checked]

        selected = self._get_selected()
        if len(selected) < 1:
            QMessageBox.warning(self,
                                "Select data",
                                "Please select at least 1 data entry")
            return
        selected_cubes = []
        dates_and_clean = []
        print(len(self.cubes), "Cuburi")
        for date, loaded, clean, ts, x, y, feats, ext, row_idx in selected:
            fname = (date + "(" + ts + "," + x + "," + y + "," + feats + ")-" + clean + ext)

            cidx = self._loaded_index((ts, x, y, feats), clean, fname)
            if cidx != -1:
                print(cidx, fname, self.cubes[cidx].datapath)
                dates_and_clean.append(self.cubes[cidx].date + " " + self.cubes[cidx].clean)
                if feats == "13":
                    if feat == "V":
                        selected_cubes.append(self.cubes[cidx].data[:, :, :, Vs13])
                    elif feat == "R":
                        selected_cubes.append(self.cubes[cidx].data[:, :, :, Rs13])
                    elif feat == "VIL":
                        selected_cubes.append(self.cubes[cidx].data[:, :, :, VIL13])
                    else:
                        raise ValueError("Invalid input")
                elif feats == "24":
                    if feat == "V":
                        selected_cubes.append(self.cubes[cidx].data[:, :, :, Vs24])
                    elif feat == "R":
                        selected_cubes.append(self.cubes[cidx].data[:, :, :, Rs24])
                    elif feat == "VIL":
                        selected_cubes.append(self.cubes[cidx].data[:, :, :, VIL24])
                    else:
                        raise ValueError("Invalid input")
        plotter = Plotter(selected_cubes, dates_and_clean, feat, cbIgnore)
        plotter.plot()

    def _saveFile(self):
        for date, loaded, clean, ts, x, y, feats, ext, row_idx in self._get_selected():
            fname = (date + "(" + ts + "," + x + "," + y + "," + feats + ")-" + clean + ext)
            if loaded != "True" or not (ext == ".cube" or ext == ".MEMORY"):
                QMessageBox.warning(self,
                                    "Invalid data",
                                    "Data has to be loaded and extention must be .cube or .MEMORY")
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

    def _str_to_list(self, string, limit):
        res =  [int(x) for x in string.split(",")]
        for x in res:
            if not (x >=0 and x < int(limit)):
                raise ValueError("Timestamp outside limits")
        return res

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
    app = QApplication(sys.argv)
    window = UCastApp()
    window.show()
    sys.exit(app.exec_())
