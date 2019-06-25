import os

from qtpy.QtWidgets import QWidget

from glue.external.echo.qt import autoconnect_callbacks_to_qt
from glue.utils.qt import load_ui

__all__ = ['OpenSpaceViewerStateWidget']


class OpenSpaceViewerStateWidget(QWidget):

    def __init__(self, viewer_state=None, session=None):

        super(OpenSpaceViewerStateWidget, self).__init__()

        self.ui = load_ui('viewer_state.ui', self,
                          directory=os.path.dirname(__file__))

        self.viewer_state = viewer_state
        self._connections = autoconnect_callbacks_to_qt(self.viewer_state, self.ui)
