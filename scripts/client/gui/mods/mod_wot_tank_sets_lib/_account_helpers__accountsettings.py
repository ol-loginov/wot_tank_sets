# coding=utf-8
from logging import getLogger

from .constants import is_carousel_filter_client_section, tank_collection_mapping
from .settings import Settings as S

log = getLogger(__name__)


def _add_user_group_filters_to_defaults():
    log.info('add user groups to default filters')

    # да, именно так. хоть модуль и именуется lower-case, мы пишем именно class-case
    # поэтому PyCharm и ошибку резолвинга пишет
    # noinspection PyUnresolvedReferences
    from account_helpers.AccountSettings import DEFAULT_VALUES, KEY_FILTERS

    filter_update = [(tank_collection_mapping(n), False) for n in S.get_tc_numbers_all()]
    filter_update = dict(filter_update)

    default_filters = DEFAULT_VALUES[KEY_FILTERS]
    changed_filters = []
    for key, value in default_filters.iteritems():
        if not is_carousel_filter_client_section(key):
            continue
        value.update(filter_update)
        changed_filters.append(key)


_add_user_group_filters_to_defaults()
LOADED = True
