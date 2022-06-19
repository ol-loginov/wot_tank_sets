MOD_ID = 'com.github.ol_loginov.wot_tank_groups'

TANK_COLLECTIONS_LIMIT = 12
TANK_COLLECTIONS_DEFAULT_COUNT = 4
TANK_COLLECTIONS_NUMBERS = list(range(1, TANK_COLLECTIONS_LIMIT + 1))
TANK_COLLECTIONS_FILTER_PREFIX = 'user_tc_'
TANK_COLLECTIONS_FILTERS = [TANK_COLLECTIONS_FILTER_PREFIX + str(n) for n in TANK_COLLECTIONS_NUMBERS]


def is_carousel_filter_client_section(section):
    return section.endswith('CAROUSEL_FILTER_CLIENT_1')
