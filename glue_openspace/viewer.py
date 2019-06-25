import os

from qtpy.QtWidgets import QLabel
from qtpy.QtGui import QImage, QPixmap

from glue.viewers.common.qt.data_viewer import DataViewer

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

    def __init__(self, *args, **kwargs):
        super(OpenSpaceDataViewer, self).__init__(*args, **kwargs)
        self.viewer_size = (320, 200)
        self._label = QLabel()
        self._image = QPixmap.fromImage(QImage(LOGO))
        self._label.setPixmap(self._image)
        self.setCentralWidget(self._label)

        self.websocket = create_connection("ws://localhost:4682/websocket")

    def get_layer_artist(self, cls, layer=None, layer_state=None):
        return cls(self.websocket, self.state, layer=layer, layer_state=layer_state)
