import json
import logging

from frameworks.wulf import ViewModel
# from gui.impl.gen.view_models.views.lobby.hangar.sub_views.vehicle_filter_model import VehicleFilterModel
from gui.impl.lobby.hangar.presenters.vehicle_filters_presenter import VehicleFiltersDataProvider
from gui.impl.pub.view_component import ViewComponent
from openwg_gameface import ModDynAccessor
from gui.filters.carousel_filter import SessionCarouselFilter, EventCriteriesGroup, BasicCriteriesGroup
from gui.impl.lobby.hangar.base.vehicles_filter_component import VehiclesFilterComponent
from openwg_gameface import gf_mod_inject
from .events import overrideMethod
from .l10n import l10n
from .settings import Settings as S
from gui.filters.carousel_filter import SessionCarouselFilter, EventCriteriesGroup, CriteriesGroup
from gui.shared.utils.requesters import REQ_CRITERIA
from .constants import tank_collection_mapping

log = logging.getLogger(__name__)

VIEW_ID = 'EditableTankSets'


class EditableTankSetsModel(ViewModel):
    def __init__(self, properties=4, commands=1):
        super(EditableTankSetsModel, self).__init__(properties=properties, commands=commands)
        self.onSaveCallback = None

    def getCollections(self):
        return self._getString(0)

    def setCollections(self, value):
        self._setString(0, value)

    def getModEnabled(self):
        return self._getBool(1)

    def setModEnabled(self, value):
        self._setBool(1, value)

    def setVisibleSet(self, value):
        self._setString(1, value)

    def _initialize(self):
        super(EditableTankSetsModel, self)._initialize()

        collections = list()
        for n, collection in S.get_enabled_collections():
            collections.append({
                'n': n,
                'title': collection.title,
                'icon': collection.icon,
                'active': collection.active
            })

        self._addStringProperty('collections', json.dumps(collections))
        self._addStringProperty('modEnabled', S.is_mod_enabled())
        self._addStringProperty('groupTitle', l10n("filterPopover.groupTitle"))
        self._addStringProperty('visibleSet', "null")
        self.onSave = self._addCommand('onSave')


# class EditableTankSetsPresenter(ViewComponent[EditableTankSetsModel]):
#     viewLayoutID = ModDynAccessor(VIEW_ID)
#
#     def __init__(self, filter):
#         super(EditableTankSetsPresenter, self).__init__(layoutID=EditableTankSetsPresenter.viewLayoutID(), model=EditableTankSetsModel)
#         self._filter = filter
#
#     @property
#     def viewModel(self):
#         return super(EditableTankSetsPresenter, self).getViewModel()
#
#     def prepare(self):
#         super(EditableTankSetsPresenter, self).prepare()
#
#         my_sets = list()
#         for n, collection in S.get_enabled_collections():
#             my_sets.extend({
#                 'n': n,
#                 'title': collection.title,
#                 'tooltip': collection.tooltip,
#                 'icon': collection.icon
#             })
#         self.viewModel.setSets(json.dumps(my_sets))


# class TankSetCriteriaGroup(CriteriesGroup):
#     def update(self, filters):
#         super(TankSetCriteriaGroup, self).update(filters)
#
#         if S.is_mod_enabled():
#             log.info('update TankSetCriteriaGroup')
#             tanks = set()
#             has_applied_filter = False
#             for n in S.get_tc_numbers_enabled():
#                 if tank_collection_mapping(n) in filters and filters[tank_collection_mapping(n)]:
#                     tanks |= set(S.collection(n).tanks)
#                     has_applied_filter = True
#
#             if has_applied_filter:
#                 self._criteria |= REQ_CRITERIA.CUSTOM(lambda item: TankSetCriteriaGroup.apply_tank_group_filters(item, tanks))
#
#     @staticmethod
#     def isApplicableFor(vehicle):
#         return True
#
#     @staticmethod
#     def apply_tank_group_filters(item, selected_tanks):
#         log.info('filter tank: ' + str(item.invID))
#         return item.invID in selected_tanks


# noinspection PyPep8Naming
@overrideMethod(VehicleFiltersDataProvider, '__init__')
def VehicleFiltersDataProvider___init__(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)

    if type(self) is VehicleFiltersDataProvider:
        log.info("add EditableTankSets viewModel into %s" % (type(self),))

        setattr(self, 'editableTankSetsModel', EditableTankSetsModel())
        self.viewModel._addViewModelProperty('EditableTankSets', self.editableTankSetsModel)
        gf_mod_inject(self.viewModel, 'VehicleFilterModelRef', modules=['coui://gui/gameface/mods/mod_editable_tank_sets/EditableTankSets.js'])

        # filter = self._VehicleFiltersDataProvider__filter
        # filter._criteriesGroups += (TankSetCriteriaGroup(),)

    return ret


@overrideMethod(VehicleFiltersDataProvider, '_getEvents')
def VehicleFiltersDataProvider_getEvents(base, self, *args, **kwargs):
    ret = base(self, *args, **kwargs)

    if type(self) is VehicleFiltersDataProvider:
        log.info("subscribe EditableTankSets viewModel events")

        if self.editableTankSetsModel.onSaveCallback is None:
            def callback(arg):
                S.set_active_collections(json.loads(arg.get('actives')))
                filter = self._VehicleFiltersDataProvider__filter
                log.info('update criteries groups %s' % (filter._criteriesGroups,))
                filter._updateCriteriesGroups()

            self.editableTankSetsModel.onSaveCallback = callback

        return ret + ((self.editableTankSetsModel.onSave, self.editableTankSetsModel.onSaveCallback),)

    return ret


## tests


# noinspection PyPep8Naming
# @overrideMethod(VehicleFilterModel, '__init__')
# def VehicleFilterModel__init__(base, self, *args, **kwargs):
#     log.info("VehicleFilterModel__init__")
#     ret = base(self, *args, **kwargs)
#
#     if type(self) is VehicleFiltersDataProvider:
#         self._addViewModelProperty('EditableTankSets', EditableTankSetsModel())
#         gf_mod_inject(self, 'VehicleFilterModelRef', modules=['coui://gui/gameface/mods/mod_editable_tank_sets/EditableTankSets.js'])
#     return ret


LOADED = True
