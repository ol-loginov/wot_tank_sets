import logging
import json

from frameworks.wulf import ViewModel
from gui.impl.gen.view_models.views.lobby.hangar.sub_views.vehicle_filter_model import VehicleFilterModel
from gui.impl.lobby.hangar.presenters.vehicle_filters_presenter import VehicleFiltersDataProvider
from gui.impl.pub.view_component import ViewComponent
from openwg_gameface import ModDynAccessor
from openwg_gameface import gf_mod_inject
from .events import overrideMethod
from .l10n import l10n
from .settings import Settings as S

log = logging.getLogger(__name__)

VIEW_ID = 'EditableTankSets'


class EditableTankSetsModel(ViewModel):
    def __init__(self, properties=2, commands=0):
        super(EditableTankSetsModel, self).__init__(properties=properties, commands=commands)

        gf_mod_inject(self, 'EditableTankSetsRef',
                      styles=[],
                      modules=['coui://gui/gameface/mods/mod_editable_tank_sets/EditableTankSets.js'])

    def getSets(self):
        return self._getString(0)

    def setSets(self, value):
        self._setString(0, value)

    def _initialize(self):
        super(EditableTankSetsModel, self)._initialize()
        self._addStringProperty('sets', '{}')
        self._addStringProperty('groupTitle', l10n("filterPopover.groupTitle"))


class EditableTankSetsPresenter(ViewComponent[EditableTankSetsModel]):
    viewLayoutID = ModDynAccessor(VIEW_ID)

    def __init__(self, filter):
        super(EditableTankSetsPresenter, self).__init__(layoutID=EditableTankSetsPresenter.viewLayoutID(), model=EditableTankSetsModel)
        self._filter = filter

    @property
    def viewModel(self):
        return super(EditableTankSetsPresenter, self).getViewModel()

    def prepare(self):
        super(EditableTankSetsPresenter, self).prepare()

        my_sets = list()
        for n, collection in S.get_enabled_collections():
            my_sets.extend({
                'title': collection.title,
                'tooltip': collection.tooltip,
                'icon': collection.icon
            })
        self.viewModel.setSets(json.dumps(my_sets))


@overrideMethod(VehicleFiltersDataProvider, '_getChildComponents')
def VehicleFiltersDataProvider__getChildComponents(base, self, *args, **kwargs):
    log.info("VehicleFiltersDataProvider__getChildComponents")
    ret = base(self, *args, **kwargs)
    ret[EditableTankSetsPresenter.viewLayoutID()] = lambda: EditableTankSetsPresenter(self._VehicleFiltersDataProvider__filter)
    return ret


# noinspection PyPep8Naming
@overrideMethod(VehicleFilterModel, '__init__')
def VehicleFilterModel__init__(base, self, *args, **kwargs):
    log.info("VehicleFilterModel__init__")
    ret = base(self, *args, **kwargs)

    gf_mod_inject(self, 'VehicleFilterModelRef', styles=[], modules=[])
    return ret


LOADED = True
