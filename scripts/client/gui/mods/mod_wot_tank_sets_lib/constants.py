MOD_ID = 'com.github.ol_loginov.wot_tank_sets'

CONFIGURATION_FOLDER = 'mods/config/%s' % MOD_ID

DEFAULT_TANK_COLLECTIONS_LIMIT = 10
DEFAULT_TANK_COLLECTIONS_COUNT = 5

TANK_COLLECTIONS_MAPPING_PREFIX = 'user_tc_'


def tank_collection_mapping(n):
    return TANK_COLLECTIONS_MAPPING_PREFIX + str(n)


def is_carousel_filter_client_section(section):
    return section.endswith('CAROUSEL_FILTER_CLIENT_1')


MOD_LANGUAGE = 'en'
