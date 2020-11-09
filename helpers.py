import re
# Constants:
LOOKML_NAME = r'^[a-z_]{1,150}$'
NONUNIQUE_PROPERTIES = {'include','link', 'filters', 'bind_filters', 'data_groups', 'named_value_format', 'sets', 'column','derived_column','includes', "allowed_value", "actions"}
MULTIVALUE_PROPERTIES = ['drill_fields', 'timeframes', 'tiers','suggestions','tags']
KEYS_WITH_NAME_FIELDS = ("user_attribute_param", "param", "form_param", "option")
OUTPUT_DIR = ''
INDT = ' '*2
NL = '\n'

def valid_name(name):
    return re.match(LOOKML_NAME,name)

def parse_references(inputString):
    '''
    Uses regular expresssions to preduce an iterator of the lookml references in a string.
    result has the shape {'raw':'${exact.field_reference}','field':'exact.field_reference', fully_qualified_reference:True}
    '''
    mustachePattern = r'\$\{([a-z\._0-9]*)\}'
    conditionPattern = r'\{\%\s{1,3}condition\s([a-z\._0-9]*)\s\%\}'
    doubleBracesPattern = r'\{\{\s{0,10}([a-z\._0-9]*)\s{0,10}\}\}'
    parameterPattern = r'\{\%\s{1,3}parameter\s([a-z\._0-9]*)\s\%\}'
    filtersPattern = r' \_filters\[\s{0,10}\'([a-z\._0-9]*)\'\]'
    fullPattern = r'(' + mustachePattern + r'|' + conditionPattern + r'|' + parameterPattern + r'|' + doubleBracesPattern + r'|' + filtersPattern + r')'
    for match in re.findall(fullPattern, inputString):
    # for match in re.findall(r'(\$\{([a-z\._0-9]*)\}|\{\%\s{1,3}condition\s([a-z\._0-9]*)\s\%\}|\{\%\s{1,3}parameter\s([a-z\._0-9]*)\s\%\}|\{\{\s{0,10}([a-z\._0-9]*)\s{0,10}\}\}| \_filters\[\s{0,10}\'([a-z\._0-9]*)\'\])',inputString):
        #Collapse the results from findall
        result = ''.join(match[1:])
        #Replace the liquid value references
        if result.endswith('._value'):
            result = result.replace('._value','')
        #Check if a fully qualified reference was used
        fq = True if '.' in ''.join(match[1:]) else False

        yield {'raw':match[0],'field':result, 'fully_qualified_reference': fq }

#Custom Exception classes
class OperationError(Exception):
    '''
        Provides messaging for issues with the operand and type
    '''
    def __init__(self, obj, operand, obj2):
        self.message = 'operation not supported' + str(type(obj)) + ' ' + str(operand) + ' ' + str(type(obj2))
        super().__init__(self.message)
class InvalidLookMLAttribute(Exception):
    '''
        Provides messaging when an attribute is attempted to be bound that does not exist
    '''
    def __init__(self, attr, cl):
        self.message = 'Attribute ' + str(attr) + ' not found for ' + str(type(cl)) 
        super().__init__(self.message)