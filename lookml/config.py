    # includes, links, filters, bind_filters
    # Things that should be their own class:
    # data_groups, named_value_format, sets
NONUNIQUE_PROPERTIES = {'include','link', 'filters', 'bind_filters', 'data_groups', 'named_value_format', 'sets', 'column'}
MULTIVALUE_PROPERTIES = ['drill_fields', 'timeframes', 'tiers','suggestions']
KEYS_WITH_NAME_FIELDS = ("user_attribute_param", "param", "form_param", "option")
TIMEFRAMES = ['raw', 'year', 'quarter', 'month', 'week', 'date', 'day_of_week', 'hour', 'hour_of_day', 'minute', 'time', 'time_of_day']
JOIN_TYPES = ['left_outer','full_outer','inner','cross']
RELATIONSHIPS = ['one_to_many','many_to_one','one_to_one','many_to_many']
DB_FIELD_DELIMITER_START = '`' 
DB_FIELD_DELIMITER_END = '`'
OUTPUT_DIR = ''
INDENT = ' '*2
NEWLINE = '\n'
NEWLINEINDENT = ''.join([NEWLINE,INDENT])
PRE_FIELD_BUFFER = NEWLINE
POST_FIELD_BUFFER = NEWLINE

#TODO: change these to configurable parameters via either argparse / config file / both 