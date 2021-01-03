from PyQt5.QtWidgets import *


class ResolutionInputDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.width = QLineEdit(self)
        self.height = QLineEdit(self)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow('Width: ', self.width)
        layout.addRow('Height: ', self.height)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def get_resolution(self):
        return self.width.text(), self.height.text()
