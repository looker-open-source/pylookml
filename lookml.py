import lkml, copy 
from lang import ws,props,DuplicatePrimaryKey
import warnings

#P2: obtain the real list of timezones from Looker itself
#P2: add CLI support
#P0: legacy / backward compatibility methods
#P2: option to omit defaults
#P2: add looker version numbers to the lang map and throw warning if prop depreicated or error if not yet supported
#P1: add warnings / error types
#P0: complex props / constructs do not support an add method and + operator overloading
class prop(object):
    def __init__(self, key, value, parent, conf={}):
        self.key = key
        self.value = value
        self.parent = parent
        self.conf = conf

    def __str__(self):
        indent = ws.nl + (self.conf['indent'] * ws.s)
        if self.parent._dense():
            return f' {self.key}: {self.value}'
        else:
            return f'{indent}{self.key}: {self.value}'

    def __getattr__(self,key):
        if key in self.__dict__.keys():
            self.__dict__.__getitem__(key)
        else:
            return None

    def __contains__(self,item): return item in self.value
    def _type(self): return self.key
    def _dense(self): return len(self.value) <= ws.dense_str_len

class lookml(object):
    _member_classes  = list()
    def __init__(self, data, parent=None):
        self.parent = parent
        self + data
    
    def __setattr__(self, key, value):
        if key in self._allowed_children():
            self._insert(key,value)
        else:
            object.__setattr__(self, key, value)

    def __getattr__(self,key):
        if key.startswith('_add_hook'):
            if key in self.__dict__.keys():
                self.__dict__.__getitem__(key)
            else:
                None
        if key in self.__dict__.keys():
            self.__dict__.__getitem__(key)
        elif key in self._allowed_children():
            return prop_router(key,'__default__', self)
    
    def __getitem__(self,item):
        return self.__dict__.__getitem__(item)

    def __contains__(self,item):
        return item in self.__dict__

    def _allowed_children(self): return props._allowed_children[self._type()]
    def _conf(self): 
        if self._type() == 'model':
            return {
                'docs_url': 'https://docs.looker.com/reference/model-reference'
            }
        elif self._type() == 'manifest':
            return {
                'docs_url': 'https://docs.looker.com/reference/manifest-reference'
            }
        else:
            # return props.cfg[self.parent._type()][self._type()]
            return props.cfg[self._type()][self.parent._type()]

    def _dense(self): return len(list(self())) <= ws.dense_children_threshold 
    #P2: this causes a stack overflow: or self._length() <= ws.dense_str_len

    def __iter__(self):
        def i():
            for v in list(self.__dict__.values()):
                yield v
        self._valueiterator = iter(i())
        return self

    def __next__(self):
        try:
            return next(self._valueiterator)
        except:
            raise StopIteration

    def __call__(self,type=prop, exclude_type=tuple(), sub_type=None, exclude_subtype=None):
        for item in self:
            if isinstance(item,type)\
                and not isinstance(item, exclude_type)\
                and (item._type() in self._allowed_children())\
                and (True if not sub_type else item._type() == sub_type)\
                and (True if not exclude_subtype else item._type() not in exclude_subtype):
                yield item

    def _s(self, *args,**kwargs): 
        data = list(self(*args,**kwargs))
        string = ''
        for item in data:
            string += str(item)
        string = string + ' ' if len(data) > 0 else string
        # string = string + ws.nl if len(data) > 0 else string
        return string

    def _type(self): return self.__class__.__name__.lower()
    def __len__(self): return len([i for i in self()])
    def _length(self): return len([str(i) for i in self()])
    def __bool__(self): return len(self) > 0
    def _json(self): return lkml.load(str(self))
    def _insert(self,key,value):
        #special top level namespace insertion for 'member classes', careful of filters keyword issues
        if key in self._member_classes and self._type() not in props.cfg['filters'].keys():
            for member in value:
                self.__dict__.update(
                    { member['name'] : classMap[key](member,self) }
                )
        #normal property insertion
        elif key in self._allowed_children():
            #step 1) instantiate the property
            candidate = prop_router( key, value, self )
            if self._add_hook(key, candidate):
                self.__dict__.update( { key: candidate } )
            
        #special private attribute insertion, currently limited to 'name'
        elif key == 'name':
            self.__dict__.update( { key: value } )
        #else, skip and throw an invalid property warning
        else:
            warnings.warn(
                f'{key} skipped. {key} not a valid attribute of {self._type()} '
                f'refer to: {self._conf()["docs_url"]}'
                )
    def _add_hook_type(self,candidate_prop):
        # print(self.parent)
        # print(candidate_prop)
        return True
    

    def _add_hook(self, key, candidate_val):
        callback = '_add_hook_' + key
        func = getattr(self, callback, None)
        if callable(func):
            return func(candidate_val)
        else:
            return True

    def __add__(self,other):
        if isinstance(other,str):
            try:
                # Handles the special case where lkml passes single object wrapped in a collection list
                parsed = lkml.load(other)[self._type() + 's'][0]
            except:
                parsed = lkml.load(other)

        elif isinstance(other,dict):
            parsed = other

        for key,value in parsed.items():
            is_plural = True if (key[:-1] in props.plural_keys) else False
            key = key[:-1] if is_plural else key
            #special cases to treat as singular
            if self._type() in props.cfg['filters'].keys() and key == 'filter': 
                key = key + 's'
            elif self._type() == 'explore_source' and key == 'bind_filter':
                key = key + 's'

            self._insert(key,value)

class Field(lookml):
    def __str__(self):
        if self._dense():
            return f'{ws.nl+(ws.s)}{self._type()}: {self.name} {{{ self._s() }}}'
        else:
            return (
                f'{ws.nl}{ws.s}{self._type()}: {self.name} {{'
                f'{ self._s(type=prop) }'
                f'{ws.nl}{ws.s}}}'
            )

    def __getattr__(self,key):

        #full reference
        if key == '__ref__' and self._type() in props.field_types:
            if self.parent:
                return ('${' + self.parent.name + '.' + self.name + '}')
        #Short Reference
        elif key == '__refs__' and self._type() in props.field_types:
            return ('${' + self.name + '}')

        #full reference -- regex escaped
        elif key == '__refre__' and self._type() in props.field_types:
            if self.parent:
                return ('\$\{' + self.parent.name + '\.' + self.name + '\}')
        #Short reference -- regex escaped
        elif key == '__refsre__' and self._type() in props.field_types:
            if self.parent:
                return ('\$\{' + self.name + '\}')
        #Raw Reference
        elif key == '__refr__' and self._type() in props.field_types:
            if self.parent:
                return (self.parent.name + '.' + self.name)
        #Raw refence short
        elif key == '__refrs__' and self._type() in props.field_types:
            if self.parent:
                return (self.name)
        #Raw Reference regex
        elif key == '__refrre__' and self._type() in props.field_types:
            if self.parent:
                return (self.parent.name + '\.' + self.name)
        else:
            super().__getattr__(key)
            #return prop_router(key,'__default__', self)

class Dimension(Field):
    def _add_hook_primary_key(self, candidate_prop):
        if self.parent.__pk:
            if candidate_prop:
                raise DuplicatePrimaryKey( self.parent, self)
            else:
                self.parent.__pk = candidate_prop
        else:
            self.parent.__pk = candidate_prop
            return True

class Measure(Field): pass
class Filter(Field): pass
class Parameter(Field): pass
class Dimension_Group(Field): pass

#P0: create model type
class Model(lookml):
    _member_classes = [
        #  'explore'
    ]
    class dotdict(dict):
        def __getattr__(self,item):
            if item in self.__dict__.keys():
                return self.__dict__[item]
            elif item in self.keys():
                return self.__getitem__(item)
            else:
                return object.__getattr__(item)
        def __str__(self):
            tmp = ws.nl
            for i in self.values():
                tmp += (ws.nl + str(i))
            return tmp

    def __init__(self,data):
        self.explores = self.dotdict()
        self.views = self.dotdict()
        self + data
    
    def __add__(self,data):
        if isinstance(data,dict):
            if 'explores' in data.keys():
                for explore in data['explores']:
                    self.explores.update(
                            {explore['name']:Explore(explore, parent=self)}
                                )
                del data['explores']
            if 'views' in data.keys():
                for view in data['views']:
                    self.views.update(
                            {view['name']:View(view, parent=self)}
                                )
                del data['views']
            super().__add__(data)
    
        if isinstance(data,str):
            parsed = lkml.load(data)
            self.__add__(parsed)

    def __getattr__(self,key):
        if key in self.__dict__.keys():
            self.__dict__.__getitem__(key)
        elif key in self._allowed_children():
            return prop_router(key,'__default__', self)

    def __str__(self):
        return (
            f'{ self._s(sub_type="connection")}'
            f'{ self._s(exclude_subtype="connection") }'
            f'{ str(self.views) }'
            f'{ str(self.explores) }'
        )

class Explore(lookml):
    _member_classes = [
    ]
    def _dense(self): return False
    def __str__(self): 
        return (f'{self._type()}: {self.name} {{'
                f'{ self._s(sub_type="join") }'
                f'{ self._s(type=(prop),exclude_subtype="join") }'
                f'{ws.nl}}}')

class Join(lookml): pass
#P0: create manifest type
class Manifest(lookml):
    _member_classes = []

    
#P0: re-integrate File type
#P0: re-integrate project type

class View(lookml):
    # top level namespace
    _member_classes = [
         'dimension'
        ,'measure'
        ,'dimension_group'
        ,'filter'
        ,'parameter'
    ]
    def __init__(self, data, parent=None):
        self.__pk = None
        super().__init__(data, parent)

    def _first_order_fields(self):
        '''
            returns: generates fields that reference DB fields directly
        '''
        for field in self(type=Field):
            if '${TABLE}.' in field.sql:
                yield field

    def _fields(self): return self(type=Field)
    def _dims(self): return self(type=Dimension)
    def _dim_groups(self): return self(type=Dimension_Group)
    def _measures(self): return self(type=Measure)
    def _params(self): return self(type=Parameter)
    def _filters(self): return self(type=Filter)
    def _dense(self): return False

    def __str__(self):
        return (
            f'{self._type()}: {self.name} {{'
                f'{ self._s(exclude_subtype="set") }'
                f'{ self._s(type=Filter) }'
                f'{ self._s(type=Parameter) }'
                f'{ self._s(type=Dimension) }'
                f'{ self._s(type=Dimension_Group) }'
                f'{ self._s(type=Measure) }'
                f'{ self._s(sub_type="set") }'
            f'{ws.nl}}}'
        )

class prop_block(prop):
    def __str__(self):
        dense = True if self.parent._dense() else False
        __ = ws.nl + (ws.s * self.conf['indent']) if not dense else ws.s
        return f'{__}{self.key}: {self.value} ;;'

class prop_string(prop):
    def __str__(self):
        dense = True if self.parent._dense() else False
        __ = ws.nl + (ws.s * self.conf['indent']) if not dense else ws.s
        return f'{__}{self.key}: "{self.value}"'
class prop_string_unquoted(prop): pass

class prop_named_construct_single(Field):
    def __init__(self,key, data, parent, conf={}):
        self._key = key
        self.conf = conf
        self + data
    def _type(self): return self._key
    def __getattr__(self,key):
        if key in self.__dict__.keys():
            self.__dict__.__getitem__(key)
    def __setattr__(self, key, value):
        #P2: way to get arround this setattr manual exceptions?
        if key in ('_key','conf'):
            object.__setattr__(self, key, value)
        elif key in props._allowed_children[self._type()]:
            self.__dict__.update( { key : prop_router( key, value, self) } )
        else:
            object.__setattr__(self, key, value)

    def __str__(self):
        i = self.conf['indent']
        if self._dense():
            return f'{ws.nl+(ws.s*i)}{self._type()}: {self.name} {{{ self._s() }}}'
        else:
            return (
                f'{ws.nl}{ws.s*i}{self._type()}: {self.name} {{'
                f'{ self._s(type=prop) }'
                f'{ws.nl}{ws.s*i}}}'
            )
class prop_named_construct(prop):
    def __init__(self, key, value, parent, conf={}):
        self.key = key
        self.value = value
        self.parent = parent
        self.conf = conf
        self.children = {}
        for instance in value:
            child = prop_named_construct_single(key, instance, self, conf=props.cfg[key][parent._type()])
            self.children.update({child.name:child})

    def __setattr__(self, key, value):
        if key in ('key','value','parent','conf','children'):
            object.__setattr__(self, key, value)
        if key in props._allowed_children[self.key]:
            self.__dict__.update( { key : prop_router( key, value, self) } )
        else:
            object.__setattr__(self, key, value)

    def __getattr__(self,key):
        if key in self.children.keys():
            return self.children.__getitem__(key)
        elif key in self.__dict__.keys():
            return self.__dict__.__getitem__(key)
        else:
            return None

    def __getitem__(self,item):
        if isinstance(item, int):
            return self.children[item]

    def __str__(self):
        dense = True if self.parent._dense() else False
        __ = ws.nl + (ws.s * self.conf['indent']) if not dense else ws.s
        rendered = ''
        for name, child in self.children.items():
            rendered += f'''{ child }'''
        return rendered

class prop_anonymous_construct(prop):
    def __init__(self, key, value, parent, conf={}):
        self.key = key
        self.value = value
        self.parent = parent
        self.conf = conf
        self.children = {}
        for name,child in value.items():
            self.children.update({name: prop_router(name,child,self)})

    def __setattr__(self, key, value):
        #P2: fix this, I think it can be done without hard coding the variable names
        if key in ('key','value','parent','conf','children'):
            object.__setattr__(self, key, value)
        if key in props._allowed_children[self.key]:
            self.__dict__.update( { key : prop_router( key, value, self) } )
        else:
            object.__setattr__(self, key, value)

    def __getattr__(self,key):
        if key in self.__dict__.keys():
            self.__dict__.__getitem__(key)
        elif key in self.children.keys():
            return self.children[key]
        else:
            return None

    def print_children(self):
        rendered_children = ''
        for child in self.children.values():
            rendered_children += (child.conf['indent']*ws.s) + str(child)
        rendered_children += ws.nl + (self.conf['indent'] * ws.s)
        return rendered_children
    def _dense(self): return len(self.children) == 0

    def __str__(self):
        dense = True if self.parent._dense() and self._dense() else False
        i = self.conf['indent']
        __ = ws.nl + (ws.s * i) if not dense else ws.s
        return f'''{__}{self.key}: {{ { self.print_children() } }}'''

class prop_anonymous_construct_plural(prop): 
    def __init__(self, key, value, parent, conf={}):
        self.key = key
        self.value = value
        self.parent = parent
        self.conf = conf
        #P0: need to loop over / iterate over the contents of children
        self.children = []
        # P0: create an add method for adding additional children 
        for construct in value:
            child = []
            for name,attr in construct.items():
                child.append(prop_router(name,attr,self))
            self.children.append(child)

    #P0: add support for textual addition / + operator overloading at any level. Need to support parsing if string, consume if dict
    def __setattr__(self, key, value):
        if key in ('key','value','parent','conf','children'):
            object.__setattr__(self, key, value)
        elif self.key != 'filters':
            if key in props._allowed_children[self.key]:
                self.__dict__.update( { key : prop_router( key, value, self) } )
        else:
            object.__setattr__(self, key, value)

    def __getattr__(self,key):
        if key in self.__dict__.keys():
            self.__dict__.__getitem__(key)
        else:
            return None
    def __getitem__(self,item):
        if isinstance(item, int):
            return self.children[item]

    def _print_child(self, child):
        rendered = ''
        for attr in child:
            rendered += ws.nl + (attr.conf['indent'] * ws.s) + str(attr)
        rendered += ws.nl + (self.conf['indent'] * ws.s)
        return rendered

    def __str__(self):
        # dense = True if self.parent._dense() else False
        dense = True if self.parent._dense() and self._dense() else False
        __ = ws.nl + (ws.s * self.conf['indent']) if not dense else ws.s
        rendered = ''
        for child in self.children:
            rendered += f'''{__}{self.key}: {{ { self._print_child(child) } }}'''
        return rendered

class common_list_functions(object):
    def __add__(self, other):
        if isinstance(other, str):
            self.value.append(other)
        elif isinstance(other, list):
            for item in other:
                self.value.append(item)
    def __sub__(self,other):
        if isinstance(other, str):
            self.value.remove(other)
        elif isinstance(other, list):
            for item in other:
                self.value.remove(item)
    def __contains__(self,other):
        return other in self.value
    def __iter__(self):
        self._valueiterator = iter(self.value)
        return self

    def __next__(self):
        try:
            return next(self._valueiterator)
        except:
            raise StopIteration

class prop_list_unquoted(prop, common_list_functions): 
    def __str__(self):
        dense = True if self.parent._dense() else False
        i = self.conf['indent']
        __ = ws.nl + (ws.s * i) if not dense else ws.s
        if len(self.value) > ws.list_multiline_threshold:
            return (f'{__}{self.key}: { "[" +ws.nl + (ws.s*(i+1))}'
                    f'{(", " + ws.nl + (ws.s*(i+1))).join(self.value) }'
                    f'{ ws.nl + (ws.s*(i+1)) + "]" }'
                    )
        else:
            return f'{__}{self.key}: { "[" + ", ".join(self.value) + "]" }'

class prop_list_quoted(prop, common_list_functions):
    def __str__(self):
        dense = True if self.parent._dense() else False
        i = self.conf['indent']
        __ = ws.nl + (ws.s * i) if not dense else ws.s

        if len(self.value) > ws.list_multiline_threshold:
            return (f'''{__}{self.key}: { '[' + ws.nl + (ws.s*(i+1)) + '"'}'''
                    f'''{('", ' + ws.nl + (ws.s*(i+1)) + '"').join(self.value) }'''
                    f'''{ '"' + ws.nl + (ws.s*(i+1)) + ']' }'''
                    )
        elif len(self.value) > 0:
            return f'''{__}{self.key}: { '["' + '","'.join(self.value) + '"]' }'''
        else:
            return f'{__}{self.key}: { "[]" }'

class prop_options(prop):
    def __init__(self, key, value, parent, conf={}):
        self.key = key
        self.value = value
        self.parent = parent
        self.conf = conf
        assert value in conf['allowed_values']

class prop_options_quoted(prop_string): 
    def __init__(self, key, value, parent, conf={}):
        self.key = key
        self.value = value
        self.conf = conf
        assert value in conf['allowed_values']

class prop_expression(prop): pass
class flt(object):
    def __init__(self,key,value):
        self.key, self.value = key, value
    
    def __str__(self):
        return f'{self.key}:"{self.value}"'
    
    def contains(self,expression):
        self.value = '%' + expression + '%'

class srt(object):
    #sorts: [field_name_1: asc | desc, field_name_2: asc | desc, …]
    def __init__(self,key,value):
        self.key, self.value = key, value
    
    def __str__(self):
        return f'{self.key}: {self.value} '
    
    def asc(self):
        self.value = 'asc'
    def desc(self):
        self.value = 'desc'

class prop_filters(prop_anonymous_construct_plural): 
    # Old Style:
    #{'filters': [{'field': 'foo', 'value': '%cool%'}, {'field': 'bar', 'value': '%great%'}], 'name': 'filters'}
    # New Style:
    #{'filters': {'foo': '%cool%', 'bar': '%great%'}, 'name': 'filters'}
    def __init__(self, key, value, parent, conf={}):
        self.key = key
        self.parent = parent
        self.conf = conf
        if isinstance(value,list):
            self.value = {f['field']:flt(f['field'],f['value']) for f in value}
        else:
            self.value = {k:flt(k,v) for k,v in value.items()}

    def __str__(self):
        fltrs = [ str(f)  for f in self.value.values()]
        indent = ws.nl + (ws.s * self.conf['indent']) if not self.parent._dense() else ws.s
        if len(self.value) > ws.list_multiline_threshold:
            return (f'{indent}{self.key}: [ {ws.nl}       ' 
                    f"{(chr(10)+'      ,').join(fltrs)}"
                    '{ws.nl}      ] ')
        else:
            return f"{indent}{self.key}: [ {', '.join(fltrs)} ] "

    def __getattr__(self,key):
        if key in self.__dict__.keys():
            return self.__dict__[key]
        elif key in self.value.keys():
            return self.value[key]

    def __getitem__(self,item):
        self.value[item]

    def __add__(self,other):
        if isinstance(other,dict):
            other = {k:flt(k,v) for k,v in other.items()}
            self.value.update(other)
    
    def __sub__(self,other):
        if isinstance(other,str):
            del self.value[other]

class prop_sorts(prop_filters):
    def __init__(self, key, value, parent, conf={}):
        self.key = key
        self.parent = parent
        self.conf = conf
        if isinstance(value,list):
            self.value = {f['field']:srt(f['field'],f['value']) for f in value}
        else:
            self.value = {k:srt(k,v) for k,v in value.items()}

class prop_yesno(prop):
    def __bool__(self): return True if self.value == 'yes' else False

class prop_html(prop_block): pass
class prop_sql(prop_block): pass

def prop_router(key,value, parent):
    is_plural = True if key[:-1] in props.plural_keys else False
    key = key[:-1] if is_plural else key
    parent_type = parent._type()
    #P2: not proud of this, but the "plural keys" needs to be corrected for certain contexts. This works for now but I can't explain it well
    if parent_type in props.cfg['filters'].keys() and key == 'filter':
        key = key + 's'
    elif parent_type == 'explore_source' and key == 'bind_filter':
        key = key + 's'
    elif parent_type == 'query' and key in ('dimension','measure'):
        key = key + 's'
    conf = props.cfg[key][parent_type]
    prop_type = conf['type']
    default = conf['default_value']
    prop_map = {
         'anonymous_construct_plural': prop_anonymous_construct_plural
        ,'named_construct': prop_named_construct
        ,'named_construct_single': prop_named_construct_single
        ,'list_unquoted': prop_list_unquoted
        ,'yesno': prop_yesno
        ,'list_quoted': prop_list_quoted
        ,'string_unquoted': prop_string_unquoted
        ,'anonymous_construct': prop_anonymous_construct
        ,'string': prop_string
        ,'options': prop_options
        ,'options_quoted': prop_options_quoted
        ,'expression': prop_expression
        ,'filters': prop_filters
        ,'html': prop_html
        ,'sorts': prop_sorts
        ,'sql': prop_sql
    }
    if value == '__default__':
        return prop_map[prop_type]( key, default, parent, conf=conf)
    else:
        if key in classMap.keys():
            return None
        else:
            return prop_map[prop_type]( key, value, parent, conf=conf)

classMap = {
     'view': View
    ,'dimension': Dimension
    ,'measure': Measure
    ,'parameter': Parameter
    ,'filter': Filter
    ,'dimension_group': Dimension_Group
    ,'explore': Explore
    ,'model': Model
    ,'manifest': Manifest
}