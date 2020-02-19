import os

from qtpy.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QWidget
from qtpy.QtGui import QImage, QPixmap
from qtpy.QtCore import Qt

from glue.viewers.common.qt.data_viewer import DataViewer
from glue.utils.qt import messagebox_on_error

from websocket import create_connection

from .layer_artist import OpenSpaceLayerArtist
from .viewer_state import OpenSpaceViewerState
from .layer_state_widget import OpenSpaceLayerStateWidget
from .viewer_state_widget import OpenSpaceViewerStateWidget

__all__ = ['OpenSpaceDataViewer']

LOGO = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logo.png'))


class OpenSpaceDataViewer(DataViewer):

    LABEL = 'OpenSpace Viewer'
    _state_cls = OpenSpaceViewerState
    _options_cls = OpenSpaceViewerStateWidget
    _layer_style_widget_cls = OpenSpaceLayerStateWidget
    _data_artist_cls = OpenSpaceLayerArtist
    _subset_artist_cls = OpenSpaceLayerArtist

    websocket = None

    def __init__(self, *args, **kwargs):
        super(OpenSpaceDataViewer, self).__init__(*args, **kwargs)
        self._logo = QLabel()
        self._image = QPixmap.fromImage(QImage(LOGO))
        self._logo.setPixmap(self._image)
        self._logo.setAlignment(Qt.AlignCenter)

        self._ip = QLineEdit()
        self._ip.setText('ws://localhost:4682/websocket')
        self._button = QPushButton('Connect')
        self._button.clicked.connect(self.connect_to_openspace)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._logo)
        self._horizontal = QHBoxLayout()
        self._horizontal.addWidget(self._ip)
        self._horizontal.addWidget(self._button)
        self._layout.addLayout(self._horizontal)
        self._main = QWidget()
        self._main.setLayout(self._layout)

        self.setCentralWidget(self._main)

    @messagebox_on_error('An error occurred when trying to connect to OpenSpace:', sep=' ')
    def connect_to_openspace(self, *args):
        self.websocket = create_connection(self._ip.text())
        self._button.setEnabled(False)
        self._button.setText('Connected')
        for layer in self.layers:
            layer.update()

    def get_layer_artist(self, cls, layer=None, layer_state=None):
        return cls(self, self.state, layer=layer, layer_state=layer_state)
