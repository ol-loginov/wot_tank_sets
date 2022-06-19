# coding=utf-8
from logging import getLogger

from .constants import is_carousel_filter_client_section, TANK_COLLECTIONS_FILTERS

log = getLogger(__name__)


def _add_user_group_filters_to_defaults():
    log.info('add user groups to default filters')

    # да, именно так. хоть модуль и именуется lower-case, мы пишем именно class-case
    # поэтому PyCharm и ошибку резолвинга пишет
    # noinspection PyUnresolvedReferences
    from account_helpers.AccountSettings import DEFAULT_VALUES, KEY_FILTERS

    filter_update = {key: False for key in TANK_COLLECTIONS_FILTERS}

    default_filters = DEFAULT_VALUES[KEY_FILTERS]
    changed_filters = []
    for key, value in default_filters.iteritems():
        if not is_carousel_filter_client_section(key):
            continue
        value.update(filter_update)
        changed_filters.append(key)


_add_user_group_filters_to_defaults()
LOADED = True
