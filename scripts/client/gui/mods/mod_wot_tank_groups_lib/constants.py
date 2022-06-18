USER_GROUP_LIMIT = 10
USER_GROUP_MAPPING_PREFIX = 'usergroup_'
USER_GROUP_FILTERS = [USER_GROUP_MAPPING_PREFIX + str(i) for i in range(1, USER_GROUP_LIMIT + 1)]

def is_carousel_filter_client_section(section):
    return section.endswith('CAROUSEL_FILTER_CLIENT_1')
