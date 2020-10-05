import copy
import lkml
import yaml
from lookml.helpers import *

#P1: overall code organization -> split into files: core, props, fields?
class lookml(object):
    _allowed_props = ()
    def __str__(self):
        return self.name + ': ' + self.value
    def json(self):
        return lkml.load(self.__str__())

    def __getattr__(self, key):
        if key in self.__dict__.keys():
            return self.__dict__[key]
        elif key in self._props.keys():
            return self._props.__getitem__(key)
        # elif key in memberclass1
        # elif key in memberclass2
        else:
            raise AttributeError(key)

    def __setattr__(self, name, value):
        if name in self._allowed_props:
            self.addProp(name, value)
        elif name == 'name':
            self.setName(value)
        elif name == 'value':
            self._data[name] = value
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def addProp(self, propName, propVal):
        self._data.update({propName: propVal})
        self._props.update(
                        { propName: prop_factory( {propName: propVal} ) }
                                            )
    def setName(self,name):
        object.__setattr__(self, 'name', name)
        self._data.update({'name':name})
    
    def _bind_dict(self,data):
        tmpData = copy.deepcopy(data)
        for k,v in tmpData.items():
            self.name, self.value = k, v

class addable(object):
    def __add__(self,other):
        self._bind_dict(lkml.load(other))

class prop(lookml):
    _allowed_props = ()
    def __init__(self,data):
        self._data = data
        self._bind_dict(data)
class prop_quoted(prop):
    def __str__(self): return self.name + ': "' + self.value + '"'

class prop_construct(prop):
    '''
    identifier: { key: "value" key2: "value2"}
    '''
    def __init__(self,data,token=''):
        self._data = data
        self._props = dict()
        self._token = token
        self.name =''
        # self._token = data['name']
        # self._token = data['name']
        self._bind_dict(self._data)

    def _bind_dict(self,data):
        tmpData = copy.deepcopy(data[self._token])
        for k,v in tmpData.items():
            if k == 'name':
                self.setName(v)
            else:
                self.addProp(k,v)

    def __str__(self):
        def r(data,indent_level=4):
            delim = '\n' + (' ' * 2 * indent_level)
            return delim.join(data)
        props  = [str(p) for pi,p in self._props.items() if pi != 'name']
        if len(props) < 3 and len(''.join(props)) < 30:
            return (f"{self._token}: {self.name} {{{' ' + ' '.join(props)  if props else ''} }}")
        else:
            return (f'{self._token}: {self.name} {{\n'
                        f'        {r(props)}'
                        f'\n        }}')

class prop_explore_source(prop):
    '''
    identifier: { key: "value" key2: "value2"}
    '''
    def __init__(self,data):
        self._data = data
        self._props = dict()
        self._token = 'explore_source'
        self._columns = dict()
        self._bind_dict(self._data)

    def _bind_dict(self,data):
        tmpData = copy.deepcopy(data['explore_source'])
        for k,v in tmpData.items():
            if k == 'name':
                self.setName(v)
            elif k == 'columns':
                for c in v:
                    self.addColumn(c)
            else:
                self.addProp(k,v)

    def addColumn(self,c):
        # print(c)
        self._columns.update({c['name']:prop_factory({'column':c},token='column')})

    def __str__(self):
        def r(data,indent_level=2):
            delim = '\n' + ' ' * 2 * indent_level
            return delim.join(data)
        props  = [str(p) for pi,p in self._props.items() if pi != 'name']
        columns  = [str(c) for cl,c in self._columns.items()]
        # print(columns)
        return (f"{self._token}: {self.name} {{\n     {' ' + (chr(10)+'      ').join(columns)  if columns else ''} \n    }}")
        # if len(props) < 3 and len(''.join(props)) < 20:
        #     return (f"{self._token}: {self.name} {{{' ' + ' '.join(props)  if props else ''} }}")
        # else:
        #     return (f'{self._token}: {self.name} {{\n'
        #                 f'    {r(props)}'
        #                 f'\n    }}')
    def __getattr__(self, key):
        if key in self.__dict__.keys():
            return self.__dict__[key]
        elif key in self._columns.keys():
            return self._columns.__getitem__(key)
        elif key in self._props.keys():
            return self._props.__getitem__(key)
        # elif key in memberclass1
        # elif key in memberclass2
        else:
            raise AttributeError(key)

    def __setattr__(self, name, value):
        if name in self._allowed_props:
            self.addProp(name, value)
        elif name == 'name':
            self.setName(value)
        elif name == 'value':
            self._data[name] = value
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)


#P0: support collection class for generic non-unique properties and . operator notation
class prop_list(prop):
    '''
        Handles unquoted list style properties: identifier: [a,b,c]
    '''
    #P1: support parameterizing whitespace {NL * indentlevel}, args for dense?
    def __str__(self):
        if len(self.value) < 4:
            return self.name + ': [' + ','.join(self.value) + ']'
        else:
            return self.name + ': [\n       ' + '\n      ,'.join(self.value) + '\n      ]'
    
    def __sub__(self, other):
        if isinstance(other, str):
            self.value.remove(other)
        else:
            raise OperationError(self,'-',other)
    def __add__(self,other):
        if isinstance(other, str):
            self.value.append(other)
        else:
            raise OperationError(self,'+',other)
    
    #P0: add iteration
    def __iter__(self):
        tmp = copy.deepcopy(self.value)
        self._valueiterator = iter(tmp)
        return self

    def __next__(self):
        try:
            return next(self._valueiterator)
        except:
            raise StopIteration

class prop_timeframes(prop_list):
    _allowed_props = (
         'date'
        ,'day_of_month'
        ,'day_of_week'
        ,'day_of_week_index'
        ,'day_of_year'
        ,'fiscal_month_num'
        ,'fiscal_quarter'
        ,'fiscal_quarter_of_year'
        ,'fiscal_year'
        ,'hour'
        ,'hour2'
        ,'hour3'
        ,'hour4'
        ,'hour6'
        ,'hour8'
        ,'hour12'
        ,'hour_of_day'
        ,'microsecond'
        ,'millisecond'
        ,'millisecond2'
        ,'millisecond4'
        ,'millisecond5'
        ,'millisecond8'
        ,'millisecond10'
        ,'millisecond20'
        ,'millisecond25'
        ,'millisecond40'
        ,'millisecond50'
        ,'millisecond100'
        ,'millisecond125'
        ,'millisecond200'
        ,'millisecond250'
        ,'millisecond500'
        ,'minute'
        ,'minute2'
        ,'minute3'
        ,'minute4'
        ,'minute5'
        ,'minute6'
        ,'minute10'
        ,'minute12'
        ,'minute15'
        ,'minute20'
        ,'minute30'
        ,'month'
        ,'month_name'
        ,'month_num'
        ,'quarter'
        ,'quarter_of_year'
        ,'raw'
        ,'second'
        ,'time'
        ,'time_of_day'
        ,'week'
        ,'week_of_year'
        ,'year'
        ,'yesno'
    )
    def __init__(self,data):
        self._data = data
        self._bind_dict(data)
    #P3: add some convenience methods for timeframes

class prop_list_quoted(prop_list):
    '''
        Handles quoted list style properties: identifier: ["a","b","c"]
    '''
    def __str__(self):
        if len(self.value) == 0:
            return self.name + ': []'
        elif len(self.value) < 4:
            return self.name + ': ["' + '","'.join(self.value) + '"]'
        else:
            return self.name + ': [\n       "' + '"\n      ,"'.join(self.value) + '"\n      ]'
class prop_square_dict(prop): pass # identifier: [key: "value" key2: "value2"]
class prop_non_unique(prop): pass # identifier: { key: "value" key2: "value2"} identifier: { key: "value" key2: "value2"}
class prop_filter(prop_quoted):
    def __init__(self,data):
        self._data = copy.deepcopy(data)
        tmpData = copy.deepcopy(data)
        for k,v in tmpData.items():
            self.name, self.value = k, v
    def __str__(self): return self.name + ':"' + self.value + '"'

    def contains(self,expression):
        self.value = '%' + expression + '%'
class prop_filters(prop):
    _allowed_props = ()
    def __init__(self,data):
        self._filters = dict()
        # Old Style:
        #{'filters': [{'field': 'foo', 'value': '%cool%'}, {'field': 'bar', 'value': '%great%'}], 'name': 'filters'}
        # New Style:
        #{'filters': {'foo': '%cool%', 'bar': '%great%'}, 'name': 'filters'}
        if isinstance(data['filters'],list): #Old syntax
            self._data = {'name':'filters','filters':{flt['field']:flt['value'] for flt in data['filters']}}
        else:
            self._data = data
            self._data.update({'name':'filters'})
        self._bind_dict(data)

    def addFilter(self,flt):
        for k,v in flt.items():
            self._filters.update(
                    { k : prop_filter( {k:v} ) }
                )
            self._data['filters'].update( {k:v} )

    def _bind_dict(self, data):
        tmpData = copy.deepcopy(self._data)
        for k,v in tmpData['filters'].items():
            self.addFilter({k:v})

    def __getattr__(self, key):
        # key in memberclass1
        if key in self.__dict__.keys():
            return self.__dict__[key]
        # key in memberclass1
        elif key in self._filters.keys():
            return self._filters.__getitem__(key)
        else:
            raise AttributeError(key)

    def __setattr__(self, name, value):
        #P3:  allow for the addition of fully qualified filter names...escape character in __getattr__ key?
        if name in ('_data','_filters') or name in self.__dict__.keys():
            object.__setattr__(self, name, value)
        else:
            self.addFilter({name:value})


    def __str__(self):
        fltrs = [str(flt) for f,flt in self._filters.items()]
        if len(fltrs) > 3:
            return ('filters: [ \n       ' 
                    f"{(chr(10)+'      ,').join(fltrs)}"
                    '\n      ]')
        else:
            return (f'filters: [ ' 
                    f"{', '.join(fltrs)}"
                    ' ]')
class prop_sql(prop):
    def __str__(self): return self.name + ': ' + self.value + ' ;;'
class prop_type(prop): pass
class prop_ndt(prop): pass
class prop_aggregate_table(prop): pass
def prop_factory(*args,**kwargs):
    k = list(args[0].keys())[0]
    if k in ('sql','sql_table_name'):
        return prop_sql(*args, **kwargs)
    elif k == 'type':
        return prop_type(*args, **kwargs)
    elif k in ('extends', 'drill_fields'):
        return prop_list(*args, **kwargs)
    elif k == 'timeframes':
        return prop_timeframes(*args, **kwargs)
    elif k in ('tags'):
        return prop_list_quoted(*args, **kwargs)
    elif k == 'filters':
        return prop_filters(*args, **kwargs)
    elif k == 'filter':
        return prop_filter(*args, **kwargs)
    elif k == 'derived_table':
        return DerivedTable(*args, **kwargs)
    elif k == 'explore_source':
        return prop_explore_source(*args, **kwargs)
    elif k == 'column':
        return prop_construct(*args,**kwargs)
    else:
        return prop(*args, **kwargs)

class LookMLDashboard:
    #https://stackabuse.com/reading-and-writing-yaml-to-a-file-in-python/
    def __init__(self,data):
        with open(data) as file:
            self._data = yaml.load(file, Loader=yaml.FullLoader)
    def json(self):
        return self._data

class VisConfig: pass
class QueryConfig: pass
class DashboardElement: pass #(combination of visconfig & query config)

#P0: support derived table and NDTs
class DerivedTable(lookml, addable):
    _allowed_props = (
         'cluster_keys'
        ,'create_process'
        ,'datagroup_trigger'
        ,'distribution'
        ,'distribution_style'
        ,'explore_source'
        ,'indexes'
        ,'partition_keys'
        ,'persist_for'
        ,'sortkeys'
        ,'sql'
        ,'sql_create'
        ,'sql_trigger_value'
        ,'table_compression'
        ,'table_format'
        ,'publish_as_db_view'
    )
    def __init__(self, data):
        self._data = data
        self._columns = dict()
        self._props = dict()
        self._bind_dict(self._data)

    def _bind_dict(self,data):
        tmpData = copy.deepcopy(data)
        for k,v in tmpData['derived_table'].items():
            if k == 'name':
                self.setName(v)
            # if k == 'explore_source':
            #     for k,v in v['columns']:
            #         self.addColumn(k,v)
            elif k in self._allowed_props:
                self.addProp(k,v)

    def __str__(self):
        return (
            f'derived_table: {{\n    '
            f'{self._props["explore_source"]}'
            f'\n}}'
        )

    # def addProp(self, propName, propVal):
    #     self._data.update({propName: propVal})
    #     self._props.update(
    #                     { propName: prop_factory( {propName: propVal} ) }

#P0: support model files
#P0: support view collection
#P0: suppoer explore collection

class NDT(DerivedTable): pass

class Manifest(lookml): pass
class Model(lookml, addable): pass
class Explore(lookml, addable): pass
class Join(lookml, addable): pass

class Field(lookml, addable):
    _allowed_props = (
        'drill_fields'
        ,'extends'
        ,'extension'
        ,'final'
        ,'label'
        ,'derived_table'
        ,'required_access_grants'
        ,'set'
        ,'sql_table_name'
        ,'suggestions'
        ,'view_label'
    )
    def __init__(self,data,view=None):
        self._view = view
        self._props = dict()
        if isinstance(data,str):
            if valid_name(data):
                self._data = {'name':data}
        elif isinstance(data,dict):
            self._data = data
        self._bind_dict(self._data)
        

    def _bind_dict(self,data):
        tmpData = copy.deepcopy(data)
        for k,v in tmpData.items():
            if k == 'name':
                self.setName(v)
            else:
                self.addProp(k,v)

    def __str__(self):
        def r(data,indent_level=2):
            delim = '\n' + ' ' * 2 * indent_level
            return delim.join(data)
        props  = [str(p) for pi,p in self._props.items() if pi != 'name']
        if len(props) < 3 and len(''.join(props)) < 20:
            return (f"{self._token}: {self.name} {{{' ' + ' '.join(props)  if props else ''} }}")
        else:
            return (f'{self._token}: {self.name} {{\n'
                        f'    {r(props)}'
                        f'\n    }}')

    def __getattr__(self, key):
        # if key == '__deepcopy__':
        #     return self.__class__
        if key in self.__dict__.keys():
            return self.__dict__[key]
        elif key in self._props.keys():
            return self._props.__getitem__(key)
        #full reference
        elif key == '__ref__':
            if self._view:
                return ('${' + self._view.name + '.' + self.name + '}')
        #Short Reference
        elif key == '__refs__':
            return ('${' + self.name + '}')

        #full reference -- regex escaped
        elif key == '__refre__':
            if self._view:
                return ('\$\{' + self._view.name + '\.' + self.name + '\}')
        #Short reference -- regex escaped
        elif key == '__refsre__':
            if self._view:
                return ('\$\{' + self.name + '\}')
        #Raw Reference
        elif key == '__refr__':
            if self._view:
                return (self._view.name + '.' + self.name)
        #Raw refence short
        elif key == '__refrs__':
            if self._view:
                return (self.name)
        #Raw Reference regex
        elif key == '__refrre__':
            if self._view:
                return (self._view.name + '\.' + self.name)
        #P3: evaluate if a short regex escaped version is necessary, i.e. do allowed characters in lookml name need escaping
        else:
            raise AttributeError(key)



class Dimension(Field):
    _allowed_props = (
         'action' 
        ,'allow_fill'
        ,'alpha_sort'
        ,'bypass_suggest_restrictions'
        ,'can_filter'
        ,'case'
        ,'case_sensitive'
        ,'datatype'
        ,'drill_fields'
        ,'end_location_field'
        ,'fanout_on'
        ,'full_suggestions'
        ,'group_label'
        ,'group_item_label'
        ,'html'
        ,'label_from_parameter'
        ,'link'
        ,'map_layer_name'
        ,'order_by_field'
        ,'primary_key'
        ,'required_fields'
        ,'skip_drill_filter'
        ,'start_location_field'
        ,'suggestions'
        ,'suggest_persist_for'
        ,'style'
        ,'sql'
        ,'sql_end'
        ,'sql_start'
        ,'tiers'
        ,'sql_longitude'
        ,'sql_latitude'
        ,'string_datatype'
        ,'units'
        ,'value_format'
        ,'value_format_name'
        ,'alias'
        ,'convert_tz'
        ,'description'
        ,'hidden'
        ,'label'
        ,'required_access_grants'
        ,'suggestable'
        ,'tags'
        ,'type'
        ,'suggest_dimension'
        ,'suggest_explore'
        ,'view_label'
    )
    def __init__(self, data, view=None,dbColumn=''):
        self._token = 'dimension'
        self._dbcolumn = dbColumn
        super(Dimension,self).__init__(data, view=view)
        # super(Dimension,self).__init__(*args,**kwargs)

class Measure(Field):
    _allowed_props = (
         'action'
        ,'approximate'
        ,'approximate_threshold'
        ,'allow_approximate_optimization'
        ,'can_filter'
        ,'datatype'
        ,'direction'
        ,'drill_fields'
        ,'fanout_on'
        ,'filters'
        ,'group_label'
        ,'group_item_label'
        ,'html'
        ,'label_from_parameter'
        ,'link'
        ,'list_field'
        ,'order_by_field'
        ,'percentile'
        ,'precision'
        ,'required_fields'
        ,'sql'
        ,'sql_distinct_key'
        ,'value_format'
        ,'value_format_name'
        ,'alias'
        ,'convert_tz'
        ,'description'
        ,'hidden'
        ,'label'
        ,'required_access_grants'
        ,'suggestable'
        ,'tags'
        ,'type'
        ,'suggest_dimension'
        ,'suggest_explore'
        ,'view_label'
    )
    def __init__(self,data, view=None):
        self._token = 'measure'
        super(Measure,self).__init__(data, view=view)

class Parameter(Field):
    _allowed_props = (
         'allowed_value'
        ,'bypass_suggest_restrictions'
        ,'default_value'
        ,'full_suggestions'
        ,'group_label'
        ,'group_item_label'
        ,'required_fields'
        ,'suggestions'
        ,'suggest_persist_for'
        ,'alias'
        ,'convert_tz'
        ,'description'
        ,'hidden'
        ,'label'
        ,'required_access_grants'
        ,'suggestable'
        ,'tags'
        ,'type'
        ,'suggest_dimension'
        ,'suggest_explore'
        ,'view_label'
    )
    def __init__(self,data, view=None):
        self._token = 'parameter'
        super(Parameter,self).__init__(data, view=view)

class Filter(Field):
    _allowed_props = (
         'bypass_suggest_restrictions'
        ,'case_sensitive'
        ,'datatype'
        ,'default_value'
        ,'full_suggestions'
        ,'group_label'
        ,'group_item_label'
        ,'required_fields'
        ,'suggestions'
        ,'suggest_persist_for'
        ,'sql'
        ,'alias'
        ,'convert_tz'
        ,'description'
        ,'hidden'
        ,'label'
        ,'required_access_grants'
        ,'suggestable'
        ,'tags'
        ,'type'
        ,'suggest_dimension'
        ,'suggest_explore'
        ,'view_label'
    )
    def __init__(self,data, view=None):
        self._token = 'filter'
        super(Filter,self).__init__(data, view=view)

class DimensionGroup(Field):
    _allowed_props = (
         'allow_fill'
        ,'bypass_suggest_restrictions'
        ,'can_filter'
        ,'datatype'
        ,'drill_fields'
        ,'fanout_on'
        ,'full_suggestions'
        ,'group_label'
        ,'group_item_label'
        ,'html'
        ,'intervals'
        ,'order_by_field'
        ,'skip_drill_filter'
        ,'sql'
        ,'sql_end'
        ,'sql_start'
        ,'timeframes'
        ,'alias'
        ,'convert_tz'
        ,'description'
        ,'hidden'
        ,'label'
        ,'required_access_grants'
        ,'suggestable'
        ,'tags'
        ,'type'
        ,'suggest_dimension'
        ,'suggest_explore'
        ,'view_label'
    )
    def __init__(self,data, view=None, dbColumn=''):
        self._token = 'dimension_group'
        self._dbcolumn = dbColumn
        super(DimensionGroup,self).__init__(data, view=view)
        #P3: apply _timeframex namespacing to refer to individual 

class View(lookml, addable):
    '''
    '''
    _allowed_props = (
        'drill_fields'
        ,'extends'
        ,'extension'
        ,'final'
        ,'label'
        ,'derived_table'
        ,'required_access_grants'
        ,'set'
        ,'sql_table_name'
        ,'suggestions'
        ,'view_label'
    )
    #P0: support legacy methods
    def __init__(self,data):
        self._data = dict()
        self._dimensions = dict()
        self._dimension_groups = dict()
        self._measures = dict()
        self._filters = dict()
        self._parameters = dict()
        self._fields = dict()
        self._props = dict()
        if isinstance(data,str):
            if valid_name(data):
                self._bind_dict({'name':data})
            else:
                raise Exception(data + 'was not a valid lookml name either containing mixed case,'
                                +' a special character or longer than 150 chracters')
        elif isinstance(data,dict):
            self._bind_dict(data)
        else:
            raise Exception('Input not a string or lkml dictionary')
        self._refresh()

    def __iter__(self):
        # P3: investigate if you can have mutible iteration without synthetic deep copy
        # self._tmp_str = str(self)
        # tmpData = lkml.load(self._tmp_str)
        # self._safe_copy = View(tmpData['views'][0])
        # self._valueiterator = iter(self._safe_copy._fields.values())
        self._valueiterator = iter(self._fields.values())
        return self

    def __next__(self):
        try:
            return next(self._valueiterator)
        except:
            raise StopIteration

    def dims(self):
        tmp = copy.deepcopy(self._dimensions)
        # for d in self._dimensions.values():
        for d in tmp.values():
            yield d
        # print(self._dimensions)
        # for i in [1,2,3]:
        #     yield i

    def _refresh(self):
        #refreshes the fields index after an operation
        self._fields.update(self._dimensions)
        self._fields.update(self._measures)
        self._fields.update(self._filters)
        self._fields.update(self._parameters)
        self._fields.update(self._dimension_groups)

    def _bind_dict(self,data):
        tmpData = copy.deepcopy(data)
        for k,v in tmpData.items():
            if k == 'name':
                self.setName(v)
            elif k == 'dimensions':
                for dim in v:
                    self.addDimension(dim)
            elif k == 'dimension_groups':
                for dimg in v:
                    self.addDimensionGroup(dimg)
            elif k == 'measures':
                for meas in v:
                    self.addMeasure(meas)
            elif k == 'filters':
                for flt in v:
                    self.addFilter(flt)
            elif k == 'parameters':
                for param in v:
                    self.addParameter(param)
            elif k in self._allowed_props:
                self.addProp(k,v)
    
    def __str__(self):
        def r(data): return ('\n  ' + '\n  '.join(data)) if data else ''
        # print(self._props['derived_table']._props)
        props  = [str(p) for pi,p in self._props.items() if pi in self._allowed_props] 
        dims, measures = [str(dim) for d,dim in self._dimensions.items()], [str(meas) for m,meas in self._measures.items()]
        dimgs = [str(dimg) for dg,dimg in self._dimension_groups.items()]
        filters, parameters = [str(flt) for f,flt in self._filters.items()], [str(param) for p,param in self._parameters.items()]
        return (f'view: {self.name} {{'
                  f'  {r(props)}'
                  f'  {r(dims)}'
                  f'  {r(dimgs)}'
                  f'  {r(filters)}'
                  f'  {r(parameters)}'
                  f'  {r(measures)}'
                  f'\n  }}')

    def __getattr__(self, key):
        if key in self.__dict__.keys():
            return self.__dict__[key]
        #Props
        elif key in self._props.keys():
            return self._props.__getitem__(key)
        #Fields
        elif key in self._fields.keys():
            return self._fields.__getitem__(key)
        #lookml reference
        elif key == '__ref__':
            return '${' + self.identifier + '}'
        else:
            raise AttributeError(key)

    def addDimension(self,dim, dbColumn=''):
        '''
            add a dimension to the view
            :param arg1: dimension
            :param arg2: (optional) sets the dbColumn of the field
            :type arg1: Dimension, lkml dict, str
            :type arg1: str of the raw colum name in the databse
            :return: returns class instance
            :rtype: View
        '''
        if isinstance(dim,dict):
            self._dimensions.update({
                        dim['name'] : Dimension(dim, view=self)
                        })

        if isinstance(dim, str):
            if valid_name(dim):
                self._dimensions.update({ 
                                dim : Dimension( dim, dbColumn=dbColumn, view=self )
                                    })
            else:
                raise Exception('your dimension name is not valid. It contains mixed case, '
                                'special characters or is >150 characters')

        if isinstance(dim, Dimension):
            dim._view = self
            self._dimensions.update({
                                dim.name : dim
                                })
        self._refresh()
        return self

    def addMeasure(self,meas):
        '''
            add a measure to the view
            :param arg1: measure
            :type arg1: Measure, lkml dict, str
            :return: returns class instance
            :rtype: View
        '''
        if isinstance(meas,dict):
            self._measures.update({
                        meas['name'] : Measure(meas, view=self)
                        })

        if isinstance(meas, str):
            if valid_name(meas):
                self._measures.update({ 
                                meas : Measure( meas, view=self )
                                    })
            else:
                raise Exception('your measure name is not valid. It contains mixed case, '
                                'special characters or is >150 characters')

        if isinstance(meas, Measure):
            meas._view = self
            self._measures.update({
                                meas.name : meas
                                })
        self._refresh()
        return self

    def addDimensionGroup(self,dimg,dbColumn=''):
        '''
            add a dimensiongroup to the view
            :param arg1: dimension group
            :param arg2: (optional) sets the dbColumn of the field
            :type arg1: Dimension, lkml dict, str
            :type arg1: str of the raw colum name in the databse
            :return: returns class instance
            :rtype: View
        '''
        if isinstance(dimg,dict):
            self._dimension_groups.update({
                        dimg['name'] : DimensionGroup(dimg, view=self)
                        })

        if isinstance(dimg, str):
            if valid_name(dimg):
                self._dimension_groups.update({ 
                                dimg : DimensionGroup( dimg, dbColumn=dbColumn, view=self )
                                    })
            else:
                raise Exception('your dimension_group name is not valid. It contains mixed case, '
                                'special characters or is >150 characters')

        if isinstance(dimg, DimensionGroup):
            dimg._view = self
            self._dimension_groups.update({
                                dimg.name : dimg
                                })
        self._refresh()
        return self

    def addFilter(self,flt):
        '''
            add a filter to the view
            :param arg1: filter
            :type arg1: Filter, lkml dict, str
            :return: returns class instance
            :rtype: View
        '''
        if isinstance(flt,dict):
            self._filters.update({
                        flt['name'] : Filter(flt, view=self)
                        })

        if isinstance(flt, str):
            if valid_name(flt):
                self._filters.update({ 
                                flt : Filter( flt, view=self )
                                    })
            else:
                raise Exception('your filter name is not valid. It contains mixed case, '
                                'special characters or is >150 characters')

        if isinstance(flt, Filter):
            flt._view = self
            self._filters.update({
                                flt.name : flt
                                })
        self._refresh()
        return self

    def addParameter(self,param):
        '''
            add a parameter to the view
            :param arg1: parameter
            :type arg1: Parameter, lkml dict, str
            :return: returns class instance
            :rtype: View
        '''
        if isinstance(param,dict):
            self._parameters.update({
                        param['name'] : Parameter(param, view=self)
                        })

        if isinstance(param, str):
            if valid_name(param):
                self._parameters.update({ 
                                param : Parameter( param, view=self )
                                    })
            else:
                raise Exception('your parameter name is not valid. It contains mixed case, '
                                'special characters or is >150 characters')

        if isinstance(param, Parameter):
            param._view = self
            self._parameters.update({
                                param.name : param
                                })
        self._refresh()
        return self


