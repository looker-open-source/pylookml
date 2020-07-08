    # includes, links, filters, bind_filters
    # Things that should be their own class:
    # data_groups, named_value_format, sets
NONUNIQUE_PROPERTIES = {'include','link', 'filters', 'bind_filters', 'data_groups', 'named_value_format', 'sets', 'column','derived_column','includes', "allowed_value", "actions"}
MULTIVALUE_PROPERTIES = ['drill_fields', 'timeframes', 'tiers','suggestions','tags']
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
class language_rules:
    field_props = ['action', 'allow_fill', 'alpha_sort', 'bypass_suggest_restrictions', 'can_filter', 'case', 'case_sensitive', 'datatype', 'drill_fields', 'end_location_field', 'fanout_on', 'full_suggestions', 'group_label', 'group_item_label', 'html', 'label_from_parameter', 'link', 'map_layer_name', 'order_by_field', 'primary_key', 'required_fields', 'skip_drill_filter', 'start_location_field', 'suggestions', 'suggest_persist_for', 'style', 'sql', 'sql_end', 'sql_start', 'tiers', 'sql_longitude', 'sql_latitude', 'string_datatype', 'units', 'value_format', 'value_format_name', 'alias', 'convert_tz', 'description', 'hidden', 'label', 'required_access_grants', 'suggestable', 'tags', 'type', 'suggest_dimension', 'suggest_explore', 'view_label']
    view_props = ("drill_fields", "extends", "extension", "label", "derived_table", "required_access_grants", "set", "sql_table_name","suggestions", "view_label")


class TEMPLATES:
    default =  """$message$token: $identifier { $props }"""
    join = default
    dimension = default
    measure = default
    parameter = default
    filter = default
    dimension_group = default
    view = """$message
view: $identifier {$props$parameters$filters$dimensions$dimensionGroups$measures$sets}
$children"""
    explore = """
$message $token: $identifier { $props $joins }
"""
    array = """{ $data }"""
    _list = """[ $data] """
#TODO: change these to configurable parameters via either argparse / config file / both 

MAX_GRAPH_DEPTH = 20
GRAPH_COLOURS = {'view':'#F2E6E6', 'dt':'#C8BFF2', 'ndt':'#92DBEF', 'explore':'#FFE587'}
GRAPH_ENGINE = 'neato'