from glue.core.data_combo_helper import ComponentIDComboHelper
from glue.external.echo import SelectionCallbackProperty
from glue.viewers.common.state import ViewerState

__all__ = ['OpenSpaceViewerState']


class OpenSpaceViewerState(ViewerState):

    ra_att = SelectionCallbackProperty(docstring='The attribute to use for the RA')
    dec_att = SelectionCallbackProperty(docstring='The attribute to use for the Dec')
    distance_att = SelectionCallbackProperty(docstring='The attribute to use for the distance')

    def __init__(self, *args, **kwargs):
        super(OpenSpaceViewerState, self).__init__(*args, **kwargs)
        self._ra_att_helper = ComponentIDComboHelper(self, 'ra_att', categorical=False)
        self._dec_att_helper = ComponentIDComboHelper(self, 'dec_att', categorical=False)
        self._distance_att_helper = ComponentIDComboHelper(self, 'distance_att', none='None', categorical=False)
        self.add_callback('layers', self._on_layers_change)

    def _on_layers_change(self, value):
        self._ra_att_helper.set_multiple_data(self.layers_data)
        self._dec_att_helper.set_multiple_data(self.layers_data)
        self._distance_att_helper.set_multiple_data(self.layers_data)
