from __future__ import absolute_import, division, print_function

from astropy import units as u

from glue.external.echo import (CallbackProperty, ListCallbackProperty,
                                SelectionCallbackProperty)

from glue.core.data_combo_helper import ComponentIDComboHelper
from glue.viewers.common.state import ViewerState

MODES = ['Sky']
MODES_BODIES = []

ALT_UNITS = [u.m, u.km, u.AU, u.lyr, u.pc, u.kpc, u.Mpc,
             u.imperial.ft, u.imperial.inch, u.imperial.mi]

ALT_TYPES = ['Distance']

CELESTIAL_FRAMES = ['ICRS', 'FK5', 'FK4', 'Galactic']

__all__ = ['OpenSpaceViewerState']


class OpenSpaceViewerState(ViewerState):

    mode = SelectionCallbackProperty(default_index=0)
    frame = SelectionCallbackProperty(default_index=0)

    lon_att = SelectionCallbackProperty(default_index=0)
    lat_att = SelectionCallbackProperty(default_index=1)
    alt_att = SelectionCallbackProperty(default_index=2)
    alt_unit = SelectionCallbackProperty(default_index=4)
    alt_type = SelectionCallbackProperty(default_index=0)

    layers = ListCallbackProperty()

    def __init__(self, **kwargs):

        super(OpenSpaceViewerState, self).__init__()

        OpenSpaceViewerState.mode.set_choices(self, MODES)
        OpenSpaceViewerState.frame.set_choices(self, CELESTIAL_FRAMES)
        OpenSpaceViewerState.alt_unit.set_choices(self, [str(x) for x in ALT_UNITS])
        OpenSpaceViewerState.alt_type.set_choices(self, ALT_TYPES)

        self.lon_att_helper = ComponentIDComboHelper(self, 'lon_att',
                                                     numeric=True,
                                                     categorical=False,
                                                     world_coord=True,
                                                     pixel_coord=False)

        self.lat_att_helper = ComponentIDComboHelper(self, 'lat_att',
                                                     numeric=True,
                                                     categorical=False,
                                                     world_coord=True,
                                                     pixel_coord=False)

        self.alt_att_helper = ComponentIDComboHelper(self, 'alt_att',
                                                     numeric=True,
                                                     categorical=False,
                                                     world_coord=True,
                                                     pixel_coord=False)

        self.add_callback('layers', self._on_layers_changed)
        self._on_layers_changed()

        self.update_from_dict(kwargs)

    def _on_layers_changed(self, *args):
        self.lon_att_helper.set_multiple_data(self.layers_data)
        self.lat_att_helper.set_multiple_data(self.layers_data)
        self.alt_att_helper.set_multiple_data(self.layers_data)

    def _update_priority(self, name):
        if name == 'layers':
            return 2
        else:
            return 0

