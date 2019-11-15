from __future__ import absolute_import, division, print_function

from glue.config import colormaps
from glue.core.data_combo_helper import ComponentIDComboHelper
from glue.core.state_objects import StateAttributeLimitsHelper
from glue.external.echo import (CallbackProperty,
                                SelectionCallbackProperty, delay_callback,
                                keep_in_sync)
from glue.viewers.common.state import LayerState

__all__ = ['OpenSpaceLayerState']


class OpenSpaceLayerState(LayerState):
    """
    A state object for OpenSpace layers.

    This is copied from the WWT layer, and some aspects of this aren't implemented in the
    OpenSpace plugin yet.
    """

    layer = CallbackProperty()
    color = CallbackProperty()
    size = CallbackProperty()
    alpha = CallbackProperty()

    size_mode = SelectionCallbackProperty(default_index=0)
    size = CallbackProperty()
    # size_att = SelectionCallbackProperty()
    # size_vmin = CallbackProperty()
    # size_vmax = CallbackProperty()
    size_scaling = CallbackProperty(1)

    color_mode = SelectionCallbackProperty(default_index=0)
    # cmap_att = SelectionCallbackProperty()
    # cmap_vmin = CallbackProperty()
    # cmap_vmax = CallbackProperty()
    # cmap = CallbackProperty()
    cmap_mode = color_mode

    # size_limits_cache = CallbackProperty({})
    # cmap_limits_cache = CallbackProperty({})

    def __init__(self, layer=None, **kwargs):

        self._sync_markersize = None

        super(OpenSpaceLayerState, self).__init__(layer=layer)

        self._sync_color = keep_in_sync(self, 'color', self.layer.style, 'color')
        self._sync_alpha = keep_in_sync(self, 'alpha', self.layer.style, 'alpha')
        self._sync_size = keep_in_sync(self, 'size', self.layer.style, 'markersize')

        self.color = self.layer.style.color
        self.size = self.layer.style.markersize
        self.alpha = self.layer.style.alpha

        # self.size_att_helper = ComponentIDComboHelper(self, 'size_att',
        #                                               numeric=True,
        #                                               categorical=False)
        # self.cmap_att_helper = ComponentIDComboHelper(self, 'cmap_att',
        #                                               numeric=True,
        #                                               categorical=False)

        # self.size_lim_helper = StateAttributeLimitsHelper(self, attribute='size_att',
        #                                                   lower='size_vmin', upper='size_vmax',
        #                                                   cache=self.size_limits_cache)

        # self.cmap_lim_helper = StateAttributeLimitsHelper(self, attribute='cmap_att',
        #                                                   lower='cmap_vmin', upper='cmap_vmax',
        #                                                   cache=self.cmap_limits_cache)

        # self.add_callback('layer', self._on_layer_change)
        # if layer is not None:
        #     self._on_layer_change()

        # self.cmap = colormaps.members[0][1]

        OpenSpaceLayerState.color_mode.set_choices(self, ['Fixed'])
        OpenSpaceLayerState.size_mode.set_choices(self, ['Fixed'])

        self.update_from_dict(kwargs)

    # def _on_layer_change(self, layer=None):
    #     with delay_callback(self, 'cmap_vmin', 'cmap_vmax', 'size_vmin', 'size_vmax'):
    #         if self.layer is None:
    #             self.cmap_att_helper.set_multiple_data([])
    #             self.size_att_helper.set_multiple_data([])
    #         else:
    #             self.cmap_att_helper.set_multiple_data([self.layer])
    #             self.size_att_helper.set_multiple_data([self.layer])

    # def update_priority(self, name):
    #     return 0 if name.endswith(('vmin', 'vmax')) else 1

    def _layer_changed(self):

        super(OpenSpaceLayerState, self)._layer_changed()

        if self._sync_markersize is not None:
            self._sync_markersize.stop_syncing()

        if self.layer is not None:
            self.size = self.layer.style.markersize
            self._sync_markersize = keep_in_sync(self, 'size', self.layer.style, 'markersize')

    # def flip_size(self):
    #     self.size_lim_helper.flip_limits()

    # def flip_cmap(self):
    #     self.cmap_lim_helper.flip_limits()