import os

from qtpy.QtWidgets import QWidget

from glue.external.echo.qt import autoconnect_callbacks_to_qt
from glue.utils.qt import load_ui
from .viewer_state import MODES_BODIES

__all__ = ['OpenSpaceViewerStateWidget']


class OpenSpaceViewerStateWidget(QWidget):

    def __init__(self, viewer_state=None, session=None):

        super(OpenSpaceViewerStateWidget, self).__init__()

        self._viewer_state = viewer_state

        self.ui = load_ui('viewer_state_widget.ui', self,
                          directory=os.path.dirname(__file__))

        self._connect = autoconnect_callbacks_to_qt(self._viewer_state, self.ui)

        self._viewer_state.add_callback('mode', self._update_visible_options)
        self._viewer_state.add_callback('frame', self._update_visible_options)
        self._update_visible_options()

    def _update_visible_options(self, *args, **kwargs):

        show_frame = self._viewer_state.mode not in MODES_BODIES
        self.ui.label_frame.setVisible(show_frame)
        self.ui.combosel_frame.setVisible(show_frame)

        if self._viewer_state.mode in MODES_BODIES:
            self.ui.label_lon_att.setText('Longitude')
            self.ui.label_lat_att.setText('Latitude')
        else:
            if self._viewer_state.frame in ['ICRS', 'FK5', 'FK4']:
                self.ui.label_lon_att.setText('RA')
                self.ui.label_lat_att.setText('Dec')
            else:
                self.ui.label_lon_att.setText('Longitude')
                self.ui.label_lat_att.setText('Latitude')
