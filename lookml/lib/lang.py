import re, warnings
import lookml.lib.language_data.config
import lookml.lib.language_data._allowed_children
class ws:
    #basic whitespace paramters
    s = '  '
    nl = '\n'

    #size of a list type object before it breaks onto multiple lines. Int for number of items, not string length
    list_multiline_threshold = 4
    dense_children_threshold = 2
    dense_str_len = 25

    #Regex Patterns
    mustachePattern = r'\$\{([a-z\._0-9]*)\}'
    conditionPattern = r'\{\%\s{1,3}condition\s([a-z\._0-9]*)\s\%\}'
    doubleBracesPattern = r'\{\{\s{0,10}([a-z\._0-9]*)\s{0,10}\}\}'
    parameterPattern = r'\{\%\s{1,3}parameter\s([a-z\._0-9]*)\s\%\}'
    filtersPattern = r' \_filters\[\s{0,10}\'([a-z\._0-9]*)\'\]'
    fullPattern = r'(' + mustachePattern + r'|' + conditionPattern + r'|' + parameterPattern + r'|' + doubleBracesPattern + r'|' + filtersPattern + r')'
    lookml_name = r'^(\+|[a-z_])[a-z_0-9]{1,150}$'
    view_pattern = r'^\s*view\:\s[a-z_]{1,150}\s\{(\s|.)*\}\s*$' #P3 pattern will match multiple views in a row
    explore_pattern = r'^\s*explore\:\s[a-z_]{1,150}\s\{(\s|.)*\}\s*$' #P3 pattern will match multiple views in a row
    join_pattern = r'^\s*join\:\s[a-z_]{1,150}\s\{(\s|.)*\}\s*$' #P3 pattern will match multiple views in a row
    field_pattern = r'^\s*(dimension|measure|filter|parameter|dimension_group)\:\s(\+|[a-z_])[a-z_0-9]{1,150}\s\{(\s|.)*\}\s*$'
    model_pattern = r'.*'
    manifest_pattern = r'.*'

def valid_name(name):
    return re.match(ws.lookml_name,name)

def possible_view_str(s):
    return re.match(ws.view_pattern,s)

def possible_field_str(s):
    return re.match(ws.field_pattern,s)

def parse_references(inputString):
    '''
    Uses regular expresssions to preduce an iterator of the lookml references in a string.
    result has the shape {'raw':'${exact.field_reference}','field':'exact.field_reference', fully_qualified_reference:True}
    '''
    for match in re.findall(ws.fullPattern, inputString):
    # for match in re.findall(r'(\$\{([a-z\._0-9]*)\}|\{\%\s{1,3}condition\s([a-z\._0-9]*)\s\%\}|\{\%\s{1,3}parameter\s([a-z\._0-9]*)\s\%\}|\{\{\s{0,10}([a-z\._0-9]*)\s{0,10}\}\}| \_filters\[\s{0,10}\'([a-z\._0-9]*)\'\])',inputString):
        #Collapse the results from findall
        result = ''.join(match[1:])
        #Replace the liquid value references
        if result.endswith('._value'):
            result = result.replace('._value','')
        #Check if a fully qualified reference was used
        fq = True if '.' in ''.join(match[1:]) else False

        yield {'raw':match[0],'field':result, 'fully_qualified_reference': fq }

class props:
    cfg = lookml.lib.language_data.config.config
    _allowed_children = lookml.lib.language_data._allowed_children._allowed_children
    keys_with_name = (
        'user_attribute_param',
        'param',
        'form_param',
        'option',
    )
    plural_keys = (
        'view',
        'measure',
        'dimension',
        'filter',
        'dimension_group',
        'access_filter',
        'bind_filter',
        'map_layer',
        'parameter',
        'set',
        'column',
        'derived_column',
        'include',
        'explore',
        'link',
        'when',
        'allowed_value',
        'named_value_format',
        'join',
        'datagroup',
        'access_grant',
        'sql_step',
        'action',
        'param',
        'form_param',
        'option',
        'user_attribute_param',
        'assert',
        'test',
        'aggregate_table',
        "application",
        "visualization",
        "override_constant",
        "constant",
        "local_dependency",
        "remote_dependency",
        "query"
    )
    field_types = (
         'dimension'
        ,'measure'
        ,'parameter'
        ,'filter'
        ,'dimension_group'
    )

#Custom Exception classes
class OperationError(Exception):
    '''
        Provides messaging for issues with the operand and type
    '''
    def __init__(self, obj, operand, obj2):
        self.message = 'operation not supported' + str(type(obj)) + ' ' + str(operand) + ' ' + str(type(obj2))
        super().__init__(self.message)

class DuplicatePrimaryKey(Exception):
    '''
        Provides messaging when a second primary key is attempted to be added
    '''
    def __init__(self, view, dim ):
        self.message = f'A primary key cannot be added because one already exists'
        super().__init__(self.message)

class CoexistanceError(Exception):
    '''
        Provides messaging when a second primary key is attempted to be added
    '''
    def __init__(self, existing, new ,additional_message=''):
        self.message = f'A {new._type()} property cannot be added when a(n) {existing._type()} already exists. {additional_message}'
        super().__init__(self.message)