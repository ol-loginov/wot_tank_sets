MOD_ID = 'com.github.ol_loginov.wot_tank_groups'

TANK_COLLECTIONS_LIMIT = 10
TANK_COLLECTIONS_DEFAULT_COUNT = 5
TANK_COLLECTIONS_NUMBERS = list(range(1, TANK_COLLECTIONS_LIMIT + 1))

TANK_COLLECTIONS_MAPPING_PREFIX = 'user_tc_'


def tank_collection_mapping(n):
    return TANK_COLLECTIONS_MAPPING_PREFIX + str(n)


def is_carousel_filter_client_section(section):
    return section.endswith('CAROUSEL_FILTER_CLIENT_1')
