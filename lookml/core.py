from lookml import lkml
from lookml.lib.lang import \
    ws,valid_name,possible_view_str,\
    possible_field_str,parse_references,\
    props,OperationError,DuplicatePrimaryKey,\
    CoexistanceError
import copy, re

import warnings
from typing import NewType, Any, Generator, Union, Tuple, Type
OMIT_DEFAULTS = False
DB_FIELD_DELIMITER_START = '`' 
DB_FIELD_DELIMITER_END = '`'
# LOOKML_DASHBOARDS = False
def omit_defaults(f):
    def wrapper(*args,**kwargs):
        if OMIT_DEFAULTS and args[0]._is_default():
            return ''
        else:            
            return f(*args,**kwargs)
    return wrapper

def possible_obj_str(
    s: str, 
    # t: Union[View,Field,Explore,Model,Manifest]) -> bool:
    t: Any) -> bool:
    """
    Check if the string matches the pattern of a specific object type

    Args:
        s (str): the string to check
        t (Union[View, Field, Explore, Model, Manifest]): the object type / class

    Returns:
        bool: is it a string of that object type
    """
    if isinstance(t,View):
        return re.match(ws.view_pattern,s)
    elif isinstance(t,Field):
        return re.match(ws.field_pattern,s)
    elif isinstance(t,Explore):
        return re.match(ws.explore_pattern,s)
    elif isinstance(t,Model):
        return re.match(ws.model_pattern,s)
    elif isinstance(t,Manifest):
        return re.match(ws.manifest_pattern,s)
    else:
        return False

def snakeCase(string: str) -> str:
    str1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', str1).lower()

def removeSpace(string: str) -> str:  # removing special character / [|]<>,.?}{+=~!$%^&*()-
    return re.sub(r'(\s|/|\[|\]|\||\,|<|>|\.|\?|\{|\}|#|=|~|!|\+|\$|\%|\^|\&|\*|\(|\)|\-|\:)+', r'', string)

def lookCase(string: str) -> str:
    return removeSpace(snakeCase(string))

class prop(object):
    def __init__(self, 
            key: str, value: any, 
            parent: any, conf: dict={}):
        self.key = key
        self.value = value
        self.parent = parent
        self.conf = conf
    @omit_defaults
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
    def _is_default(self): return True if self.conf['default_value'] == self.value else False

class lookml(object):
    _member_classes  = list()
    _private_items = list()
    def __init__(self, data, parent=None):
        if isinstance(data,dict):
            pass
        elif isinstance(data, str):
            if valid_name(data):
                data = {'name':data}
            elif possible_obj_str(data,self):
                   parsed = lkml.load(data)
                   typ = self._type()+'s'
                   if typ in parsed.keys():
                       if len(parsed[typ]) == 1:
                           data = parsed[typ][0]
                       else:
                            raise Exception("Input string contains more than one " + self._type())
                   else:
                        raise Exception(f"Input string does not contain {typ}")
            else:
                raise Exception(
                                f"{data} does not match a " 
                                f"view: name {{}} or lookml name pattern")
        self.parent = parent
        self + data
    def __setattr__(self, key, value):
        if key in self._allowed_children():
            self._insert(key,value)
        else:
            object.__setattr__(self, key, value)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.name} @{hex(id(self))}>'

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

    def __sub__(self,other):
        if isinstance(other, str):
            if other in self.__dict__.keys():
                del self.__dict__[other]
            else:
                warnings.warn(f'{other} did not exist on {self.name}')
        else:
            raise OperationError(self,' - ',other)

    def __iter__(self):
        def i():
            public_items = [
                v for k,v in 
                self.__dict__.items() 
                if k not in self._private_items
                ]
            for v in public_items:
                yield v
        self._valueiterator = iter(i())
        return self

    def __next__(self):
        try:
            return next(self._valueiterator)
        except:
            raise StopIteration

    def __call__(self, 
        type=prop, 
        exclude_type=tuple(), 
        sub_type=None, 
        exclude_subtype=None,
        ) -> Generator:
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
    def _type(self) -> str: return self.__class__.__name__.lower()
    def __len__(self) -> int: return len([i for i in self()])
    def _length(self) -> int: return len([str(i) for i in self()])
    def __bool__(self) -> bool: return len(self) > 0
    def _json(self) -> dict: return lkml.load(str(self))
    def _insert(self,key: str, value: dict) -> None:
        #special top level namespace insertion for 'member classes', careful of filters keyword issues
        ac = self._allowed_children()
        if key in self._member_classes and self._type() not in props.cfg['filters'].keys():
            for member in value:
                self.__dict__.update(
                    { member['name'] : classMap[key](member,self) }
                )
        #normal property insertion
        elif key in ac:
            #step 1) instantiate the property
            candidate = prop_router( key, value, self )
            #step 2) if the hook lookup fails do nothing
            if self._add_hook(key, candidate):
                if isinstance(candidate,prop_named_construct):
                    if key not in self.__dict__.keys():
                        self.__dict__.update( { key: candidate } )
                    else:
                        self.__dict__[key].children.update(candidate.children)
                else:
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
    def _add_hook_type(self,candidate_prop) -> bool:
        #currently doesn't do anything
        # candidate_prop
        return True
    ##### Legacy Methods #####
    def setProperty(self,key: str, value: dict):
        self._insert(key,value)
        return self

    def setName(self, name: str):
        """
        Set your Field's name value

        Args:
            name (str): a valid lookml name a to z, numbers and underscores

        Returns:
            Field: Your field for method chaining

        Raises:
            Exception: invalid lookml name
        """
        if valid_name(name):
            old_name = self.name
            self.name = name
            self.parent.__dict__.pop(old_name)
            self.parent + self
            return self
        else:
            raise Exception("invalid LookML Name")
    def setDescription(self, description: str):
        """
        Set your object's description

        Warning: 
        not all LookML objects support a description attribute. This method is present
        in a small number of cases on objects which do not support the parameter.

        Args:
            description (str): a description string

        Returns:
            Field: Your field for method chaining
        """
        self.description = description
        return self
    def hasProp(self, p: str) -> bool:
        """
            Check if a property is in your object

        Args:
            p (str): the string of the property
            i.e. dim.hasProp('type') -> True

        Returns:
            Boolean: True if prop present, false if not
        """
        if p in self.__dict__.keys():
            if isinstance(self.__dict__[p],prop):
                return True
            else:
                return False
        else:
            return False
    ##### Legacy Methods #####
    def _add_hook(self, key, candidate_val):
        callback = '_add_hook_' + key
        func = getattr(self, callback, None)
        if callable(func):
            return func(candidate_val)
        else:
            return True
    #P2: _add_hook_x is not invoked for name, want to add it so that valid_name can be run
    # def _add_hook_name(self,candidate):
    #     pass

    def __add__(self,other):
        # start object addition routine
        #P1: implment add hooks here and for member classes types
        if not isinstance(other,(str,dict)):
            if isinstance(self,View) and isinstance(other,Field):
                self.__dict__.update({other.name:other})

        # end object addition 
        if isinstance(other,str):
            tmp = lkml.load(other)
            if self._type() + 's' in tmp.keys():
                parsed = tmp[0][self._type() + 's']
            else:
                parsed = tmp
            # try:
            #     # Handles the special case where lkml passes single object wrapped in a collection list
            #     parsed = lkml.load(other)[self._type() + 's'][0]
            # except:
            #     parsed = lkml.load(other)

        elif isinstance(other,dict):
            parsed = other

        if isinstance(other,str) or isinstance(other,dict):
            for key,value in parsed.items():
                is_plural = True if (key[:-1] in props.plural_keys) else False
                key = key[:-1] if is_plural else key
                #special cases to treat as singular
                if self._type() in props.cfg['filters'].keys() and key == 'filter': 
                    key = key + 's'
                elif self._type() == 'explore_source' and key == 'bind_filter':
                    key = key + 's'
                elif self._type() == 'access_grant' and key == 'allowed_value':
                    key = key + 's'
                elif self._type() == 'query' and key in ("dimension","measure"):
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
            if self.parent is not None:
                return ('${' + self.parent.name + '.' + self.name + '}')
        #Short Reference
        elif key == '__refs__' and self._type() in props.field_types:
            return ('${' + self.name + '}')

        #full reference -- regex escaped
        elif key == '__refre__' and self._type() in props.field_types:
            if self.parent is not None:
                return (r'\$\{' + self.parent.name + r'\.' + self.name + r'\}')
        #Short reference -- regex escaped
        elif key == '__refsre__' and self._type() in props.field_types:
            if self.parent is not None:
                return (r'\$\{' + self.name + r'\}')
        #Raw Reference
        elif key == '__refr__' and self._type() in props.field_types:
            if self.parent is not None:
                return (self.parent.name + '.' + self.name)
        #Raw refence short
        elif key == '__refrs__' and self._type() in props.field_types:
            if self.parent is not None:
                return (self.name)
        #Raw Reference regex
        elif key == '__refrre__' and self._type() in props.field_types:
            if self.parent is not None:
                return (self.parent.name + r'\.' + self.name)
        #return prop defaults
        elif key in self._allowed_children():
            return prop_router(key,'__default__', self)
        else:
            super().__getattr__(key)
            #return prop_router(key,'__default__', self)
    
    def addTag(self,tag: str):
        """
        Add a tag to the field's tag collection

        Args:
            tag (str): the tag to add

        Returns:
            [type]: returns your field for method chaining

        """
        self.tags + tag
        return self
    def removeTag(self,tag: str):
        """
        Remove a tag from the field's tag collection

        Args:
            tag (str): the tag to remove

        Returns:
            [type]: returns your field for method chaining

        """
        self.tags - tag
        return self
    def setType(self,typ: str):
        """
        Sets the Fields type attribute to the specified value
        i.e. dim.setType('number')

        Args:
            typ (str): an allowed lookml type for the field

        Returns:
            Field: returns itself for chaining dim.setType('number').setPrimaryKey()
        """
        self.type = typ
        return self

    def setViewLabel(self, view_label: str):
        """
        sets the view_label attribute for the field
        controlling where it rolls up on the explore screen

        Args:
            view_label (str): view_label

        Returns:
            [type]: [description]
        """
        self.view_label = view_label
        return self

    def dependency_chain(self,i=0):
        """
        Yields nested tuple datastructures showing each of the
        dependency chains coming from your field
        
        Yields:
            Tuple: (1,dimA,(2,dimB,(3,dimC,...)))
        """
        if self.parent is not None:
            i += 1
            for dependent in list(self.parent.search('sql',[self.__refsre__,self.__refre__])):
                if dependent is not None:
                    for dep in dependent.dependency_chain(i=i):
                        if dep is not None:
                            yield  i, dependent, dep
                    yield  i, dependent

    def children_all(self,i=0):
        """
        Returns the fields in the same view which directly or indirectly 
        reference your field. I.e. dim B references dim A and dim C 
        references dim B. This method returns B and C

        Yields:
            Field: fields dependent upon your field
        """
        if self.parent is not None:
            i += 1
            for dependent in list(self.parent.search('sql',[self.__refsre__,self.__refre__])):
                if dependent is not None:
                    for dep in dependent.dependency_chain(i=i):
                        if dep is not None:
                            yield dep
                    yield dependent

    def children(self):
        """
        Returns the fields in the same view which directly reference 
        the field in their sql parameter

        Yields:
            Field: fields directly referencing your field
        """
        if self.parent is not None:
            for dependent in list(self.parent.search('sql',[self.__refsre__,self.__refre__])):
                if dependent is not None:
                    yield dependent

    def _ancestor_chain(self,i=0):
        for f in re.finditer(ws.mustachePattern, self.sql.value):
            yield f.group(1)

    def ancestors(self):
        """
        return the fields directly referenced by your field

        Yields:
            Field: a generator of direct ancestors
        """
        for ref in self._ancestor_chain():
            yield self.parent[ref]
    
    def ancestors_all(self):
        for f in re.finditer(ws.mustachePattern, self.sql.value):
            yield f.group(1)

    def _render_dependency_map(self,depChain,i=0):
        # depChain = (1, 'c', (2, 'd', (3, 'e')))
        # a -> c -> d -> e
        length = len(depChain)
        if i == 0:
            print(self.name, end=" -> ")
        if length == 3:
            print(depChain[1].name,end=" -> ")
            self._render_dependency_map(depChain[2],i=1)
        elif length == 2:
            print(depChain[1].name)

    def setName_replace_references(self, newName: str):
        """
        Alias for Field.setName_safe() method
        """
        self.setName_safe(newName)
        return self

    def setName_safe(self, newName: str):
        """
        Change the name of the field and references to it in sql 
        (does not yet perform the same for HTML / Links / Drill Fields / Sets / Actions etc)

        Args:
            newName (str): the new name

        Returns:
            self for method chaining
        """
        #P2: complete checking all places for dependencies, html, links etc
        old = copy.deepcopy(self.name)
        oldrefsre = copy.deepcopy(self.__refsre__)
        oldrefre = copy.deepcopy(self.__refre__)
        self.setName(newName)
        for f in self.parent.search('sql',[oldrefsre,oldrefre]):
            f.sql = re.sub(oldrefsre, self.__refs__, str(f.sql.value))
            f.sql = re.sub(oldrefre, self.__ref__, str(f.sql.value))
        self.parent.removeField(old)
        self.parent + self
        return self

    def setSql(self,sql: str):
        """
        Set the value of your sql
        We reccomend you 
        use the preffered method of setting directly: dim.sql = "${TABLE}.id"

        Args:
            sql (str): string of your sql

        Returns:
            self
        """
        self.sql = sql
        return self

    def addLink(self,url: str,label: str,icon_url: str ='https://looker.com/favicon.ico'):
        """
        Add a link

        Args:
            url (str): string for your url (can contain liquid)
            label (str): string for your label (can contain liquid)
            icon_url (str): default is "https://looker.com/favicon.ico"

        Returns:
            self
        """
        self + f"""
        link: {{
            url: "{url}"
            label: "{label}"
            icon_url: "{icon_url}"
        }}
        """
        return self

    def setString(self):
        """
        Sets the Dimension to type string

        Returns:
            Dimension: returns your dimension for chaining 
            dim.setPrimaryKey().setType('number')
        """
        self.type = 'string'
        return self

class Dimension(Field):
    def setPrimaryKey(self):
        """
        Sets the Dimension as it's parent view's primary key 
        and adds primary_key: yes to the field

        Returns:
            Dimension: returns your dimension for chaining 
            dim.setPrimaryKey().setType('number')
        """
        self.primary_key = 'yes'
        return self
    def unSetPrimaryKey(self):
        """
        Unregisters the Field as it's parents pk and adds
        primary_key: no to the field

        Returns:
            Dimension: returns your dimension for chaining 
            dim.setPrimaryKey().setType('number')
        """
        self.primary_key = 'no'
        return self
    def setDBColumn(self, dbColumn: str,changeIdentifier: bool=True):
        """
        Sets changes your sql to refer to the new column name

        Args:
            dbColumn (str): [description]
            changeIdentifier (bool, optional): [description]. Defaults to True.

        Returns:
            Dimension: returns your dimension for chaining 
            dim.setPrimaryKey().setType('number')
        """
        self.sql = (f'${{TABLE}}.{DB_FIELD_DELIMITER_START}'
                    f'{dbColumn}{DB_FIELD_DELIMITER_END}')
        if changeIdentifier:
            self.setName_safe(lookCase(dbColumn)) 
        return self
    def setNumber(self):
        """
        Sets the Dimension to type number

        Returns:
            Dimension: returns your dimension for chaining 
            dim.setPrimaryKey().setType('number')
        """
        self.type = 'number'
        return self
        
    def _add_hook_primary_key(self, candidate_prop):
        if self.parent._View__pk is not None:
            if self.parent._View__pk.primary_key:
                if candidate_prop:
                    raise DuplicatePrimaryKey( self.parent, self)
                else:
                    self.parent._View__pk = self
                    #returns true to allow the dict.update
                    return True 
            else:
                self.parent._View__pk = self
                return True
        else:
            self.parent._View__pk = self
            #returns true to allow the dict.update
            return True 


class Measure(Field): pass
class Filter(Field): pass
class Parameter(Field): pass
class Dimension_Group(Field): pass

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
                return dict.__getattr__(item)
        def __iter__(self):
            self._valueiterator = iter(list(self.values()))
            return self

        def __sub__(self,other):
            if isinstance(other, str):
                del self[other]
            else:
                raise OperationError(self,' - ',other)

        def __next__(self):
            try:
                return next(self._valueiterator)
            except:
                raise StopIteration

        def __str__(self):
            tmp = ws.nl
            for i in self.values():
                tmp += (ws.nl + str(i))
            return tmp

    def __init__(self,data, parent=None):
        self.explores = self.dotdict()
        self.views = self.dotdict()
        self.parent = parent
        self + data
    
    def __add__(self,data):
        if isinstance(data, View):
            #handle refinements of objects in same scope by merge __dict__
            if data._is_refinement and data.name in self.views.keys():
                    self.views[data.name].__dict__.update(data.__dict__)
            else:
                data.parent = self
                self.views.update(
                        {data.name:data}
                            )
        if isinstance(data, Explore):
            #handle refinements of objects in same scope by merge __dict__
            if data._is_refinement and data.name in self.explores.keys():
                    self.explores[data.name].__dict__.update(data.__dict__)
            else:
                data.parent = self
                self.explores.update(
                        {data.name:data}
                            )
        if isinstance(data,dict):
            if 'explores' in data.keys():
                for explore in data['explores']:
                    #if refinement and pre-existing, merge object, else normal
                    if explore['name'] in self.explores.keys() and explore['name'].startswith('+'):
                        # self.explores[explore['name']].__dict__.update(explore)
                        self.__add__(Explore(explore, parent=self))
                    else:
                        self.explores.update(
                                {explore['name']:Explore(explore, parent=self)}
                                    )
                del data['explores']
            if 'views' in data.keys():
                for view in data['views']:
                    #if refinement and pre-existing, merge object, else normal
                    if view['name'] in self.views.keys() and view['name'].startswith('+'):
                        # self.views[view['name']].__dict__.update(view)
                        self.__add__(View(view, parent=self))
                    else:
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
    def __init__(self,data, parent=None):
        super().__init__(data,parent)
        self._is_refinement = True if self.name.startswith('+') else False
    def _dense(self): return False
    def __str__(self): 
        return (f'{self._type()}: {self.name} {{'
                f'{ self._s(sub_type="join") }'
                f'{ self._s(type=(prop),exclude_subtype="join") }'
                f'{ws.nl}}}')

class Manifest(lookml):
    _member_classes = []
    def __str__(self):
        return (
            f'{ self._s() }'
        )

class View(lookml):
    """
    LookML View Object
    construct with name, short string or lkml json
    
.. code-block:: python
    :linenos:

    #construct via name string
    myView = lookml.View('foo')
    myView.view_label = "made by name"
    print(myView)
    >>> view: foo {
           view_label: "made by name"
         }
    #construct via string of LookML
    myView = lookml.View('view: foo { view_label: "made by string" }')
    print(myView)
    >>> view: foo {
           view_label: "made by string"
         }
    #construct via json (in lkml format)
    myView = lookml.View({'name':'foo', 'view_label':'made by json'})
    print(myView)
    >>> view: foo {
           view_label: "made by json"
         }

    """
    _member_classes = [
         'dimension'
        ,'measure'
        ,'dimension_group'
        ,'filter'
        ,'parameter'
    ]
    _private_items = ['_View__pk']
    def __init__(self, data, parent=None):
        self.__pk = None
        super().__init__(data, parent)
        self._is_refinement = True if self.name.startswith('+') else False

    def __sub__(self,other):
        if isinstance(other, Field):
            if other.name in self.__dict__.keys():
                if len(list(other.dependency_chain())) > 1:
                    warnings.warn(
                        f'{other.__refrs__} had dependencies: '
                        f'{[f.name for f in other.children_all()]}'
                        )
                del self.__dict__[other.name]
            else:
                warnings.warn(f'{other.name} did not exist in {self.name}')
        elif isinstance(other, str):
            if other in self.__dict__.keys():
                if isinstance(self[other],Field):
                    if len(list(self[other].dependency_chain())) > 1:
                        warnings.warn(
                            f'{self[other].__refrs__} had dependencies: '
                            f'{[f.name for f in self[other].children_all()]}'
                            )
                del self.__dict__[other]
            else:
                warnings.warn(f'{other} did not exist on {self.name}')
        else:
            raise OperationError(self,' - ',other)
    def _fields(self) -> Generator: return self(type=Field)
    def _dims(self) -> Generator: return self(type=Dimension)
    def _dim_groups(self) -> Generator: return self(type=Dimension_Group)
    def _measures(self) -> Generator: return self(type=Measure)
    def _params(self) -> Generator: return self(type=Parameter)
    def _filters(self) -> Generator: return self(type=Filter)
    def _dense(self) -> Generator: return False

    def _add_hook_sql_table_name(self, sql_table_name):
        if 'derived_table' in self:
            raise CoexistanceError(
                self.derived_table,
                sql_table_name,
                additional_message='Try running del yourViewName.derived_table '
                +'before adding the sql_table_name'
                )
        else:
            return True
    def _add_hook_derived_table(self, derived_table):
        if 'sql_table_name' in self:
            raise CoexistanceError(
                self.sql_table_name,
                derived_table,
                additional_message='Try running del yourViewName.sql_table_name '
                +'before adding the derived_table'
                )
        else:
            return True

    def search(self, prop, pattern):
        '''
        pass a regex expression and will return the fields whose sql match
        :param prop: name of proprty you'd like to search
        :param pattern: the regex pattern
        :type prop: str
        :type patter: a regex search string
        :return: a generator / iteratble set of fields who have a member property matching the pattern
        :rtype: Field
        '''
        if isinstance(pattern,list):
            pattern = '('+'|'.join(pattern)+')'
        find_this = r''.join([r'.*',pattern,r'.*'])
        for field in self.fields():
            if prop in field.__dict__.keys():
                string_to_search = field.__dict__[prop].value
            else:
                string_to_search = ''
            if re.match(find_this,string_to_search):
                yield field

    def removeField(self,field):
        """
        Remove a Field from your View

        Args:
            field ([type]): [description]

        Returns:
            View: returns your view for method chaining 
            i.e. view.removeField(view.id).addCount()
        """
        self - field
        return self

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
    ##### Legacy Methods #####
    # generators #
    def fieldNames(self):
        """
        returns all the field names

        Yields:
            [type]: iteration of the fields names
        """
        for field in self._fields():
            yield field.name

    def fields(self): 
        """
        get all the Views Fields

        Returns:
            [type]: iterable collection of Fields
        """
        for f in self._fields():
            yield f

    def dimensions(self): 
        """
        get all the Views Dimensions

        Returns:
            Dimension: iterable collection of Dimensions
        """
        for d in self._dims():
            yield d

    def measures(self): 
        """
        get all the Views Measures

        Returns:
            Measure: iterable collection of Measures
        """
        for d in self._measures():
            yield d

    def dimensionGroups(self): 
        """
        iterate over the dimension_group fields in your view

        Returns:
            Iterator: Iterator of type dimension_group Field
        """
        for dg in self._dim_groups():
            yield dg

    def filters(self): 
        """
        iterate over the filter fields in your view

        Returns:
            Iterator: Iterator of type Filter Field
        """
        for f in self._filters():
            yield f 

    def parameters(self): 
        """
        iterate over the parameter fields in your view

        Returns:
            Iterator: Iterator of type Parameter Field
        """
        for p in self._params():
            yield p

    def getFieldsByTag(self,tag: str):
        """
        Loop through your fields with a specific tag present

        Args:
            tag (str): 
        Yields:
            Field: Fields with the selected tag
        """
        for f in self._fields():
            if tag in f.tags:
                yield f

    def getFieldsByType(self, typ: str):
        """
        Loop over fields with a certain type

        Args:
            typ (str): 'string','number','count'...

        Yields:
            Field: Field with the selected type attribute
        """
        for f in self._fields():
            if f.type.value == typ:
                yield f

    def getFieldsSorted(self):
        '''
        return the fields sorted first conventionally by type, then alphabetically

        Yields:
            Field: a list of fields in the natural sort order
        '''
        return sorted(self._fields(), key=lambda field: ''.join([str(isinstance(field, Measure)), field.name]))
    # end generators
        
    def addDimension(self,d: (str,Dimension),type: str = 'string'): 
        """
        Add a dimension object, or add a string DB column you would like added 

        Args:
            d ([type]): [description]
            type (str, optional): [description]. Defaults to 'string'.

        Returns:
            [type]: [description]
        """
        if isinstance(d,Dimension):
            self + d
        if isinstance(d,str):
            name = lookCase(d)
            self + f'''
            dimension: {name} {{
                type: {type}
                sql: {d} ;;
            }}
            '''
        return self

    def addCount(self): 
        """
        Adds a basic measure type count to your view

        Returns:
            self: allows for chaining myView.addCount().addDimension()
        """
        self + 'measure: count { type: count }'
        return self

    def addAverage(self, field: Dimension):
        """
        Add an average of a dimension to your view

        Args:
            field (Dimension): add a dimension object you'd like the average on
        """
        self + f'''
            measure: {field.name}_avg {{
                type: average
                sql: {field.__ref__} ;;
            }} 
        '''
        return self

    def addCountDistinct(self,field: Dimension): 
        """
        Add a count distinct of a dimension to your view

        Args:
            field (Dimension): add a dimension object you'd like the distinct on
        """
        self + f'''
            measure: {field.name}_count_distinct {{
                type: count_distinct
                sql: {field.__ref__} ;;
            }} 
        '''
        return self

    def sum(self,field: Dimension): 
        """
        Add a sum of a dimension to your view

        Args:
            field (Dimension): add a dimension object you'd like the sum on
        """
        self + f'''
            measure: {field.name}_sum {{
                type: tum
                sql: {field.__ref__} ;;
            }} 
        '''
        return self

    def sumAllNumDimensions(self):
        """
        creates a sum measure for each Dimension of type number

        Returns:
            View: returns your View for method chaining view.sumAllNumDimensions().addCount()...
        """
        for numDim in self.getFieldsByType('number'):
            self.sum(numDim)
        return self

    def setViewLabel(self,label: str):
        """
        Add a view_label to your view

        Args:
            label (str): the text of the View Label

        Returns:
            View: returns your View for method chaining view.sumAllNumDimensions().addCount()...
        """
        self.setProperty('view_label',label)
        return self

    def print_dependency_map(self):
        for field in list(self.fields()):
            for referenceChain in field.dependency_chain():
                field._render_dependency_map(referenceChain)

    def first_order_fields(self) -> Generator:
        '''
        generates fields that reference DB fields directly
        having the ${TABLE} syntax

        :return: Generator of type Field
        :rtype: Field
        '''
        for field in self(type=Field):
            if '${TABLE}.' in field.sql:
                yield field
    ##### Legacy Methods #####

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
        # if isinstance(item, int):
        return self.children[item]
        
    
    def __add__(self,other):
        #P3: since this is on the props hierarchy, need to refactor addition so it's not challenging
        #do after extensive unit tests are in place
        if isinstance(other,str):
            try:
                parsed = lkml.load(other)[self.key+'s']
            except:
                raise Exception(f'can only add {self.key} to {self.key}')

        elif isinstance(other,dict):
            parsed = other
        for item in parsed:
            candidate = prop_named_construct_single(
                    self.key, 
                    item, 
                    self.parent, 
                    conf=props.cfg[self.key][self.parent._type()]
                    )
            self.children.update({candidate.name: candidate})

    def __str__(self):
        dense = True if self.parent._dense() else False
        __ = ws.nl + (ws.s * self.conf['indent']) if not dense else ws.s
        rendered = ''
        # for name, child in self.children.items():
        for child in self.children.values():
            rendered += f'''{ child }'''
        return rendered

    def __sub__(self,other: str):
        if other in self.__dict__.keys():
            del self.__dict__[other]
        elif other in self.children.keys():
            del self.children[other]
        else:
            raise Exception(f'{other} not present in {self.key}')

    def __contains__(self,other):
        return other in self.children
    def __iter__(self):
        self._valueiterator = iter(list(self.children.values()))
        return self

    def __next__(self):
        try:
            return next(self._valueiterator)
        except:
            raise StopIteration



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

    def __sub__(self,other: str):
        if other in self.__dict__.keys():
            del self.__dict__[other]
        elif other in self.children.keys():
            del self.children[other]

#P1: does not support addition like proper lookml objects, 
# pull out add and add_hook, insert, sub and sub_hook systems into a  
# common container class

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
    class prop_anonymous_construct_child(prop_anonymous_construct):
        def remove(self):
            """
                Remove self from construct
            """
            self.parent.link.children.remove(self)

    def __init__(self, key, value, parent, conf={}):
        self.key = key
        self.value = value
        self.parent = parent
        self.conf = conf
        self.children = []
        for construct in value:
            child = self.prop_anonymous_construct_child(
                        key, 
                        construct, 
                        self.parent, 
                        conf=conf
                        )
            self.children.append(child)

    def remove(self,item):
        """
        remove an item from your 

        Args:
            item ([type]): [description]
        """
        self.children.remove(item)
    
        
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
    
    def __add__(self,other):
        #P3: since this is on the props hierarchy, need to refactor addition so it's not challenging
        #do after extensive unit tests are in place
        if isinstance(other,str):
            try:
                parsed = lkml.load(other)[self.key+'s']
            except:
                raise Exception(f'can only add {self.key} to {self.key}')

        elif isinstance(other,dict):
            parsed = other
        for item in parsed:
            candidate = self.prop_anonymous_construct_child(
                    self.key, 
                    item, 
                    self.parent,
                    conf=props.cfg[self.key][self.parent._type()]
                    )
            self.children.append(candidate)

    def __str__(self):
        dense = True if self.parent._dense() and self._dense() else False
        __ = ws.nl + (ws.s * self.conf['indent']) if not dense else ws.s
        rendered = ''
        for child in self.children:
            rendered += f'''{ str(child) }'''
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

class prop_includes(prop, common_list_functions):
    def __str__(self):
        rendered = [f'include: "{val}"' for val in self.value]
        return ws.nl.join(rendered)

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
class prop_sql(prop_block):
    def nvl(self):
        self.value = f"nvl({self.value},0)"

def prop_router(key,value, parent):
    is_plural = True if key[:-1] in props.plural_keys else False
    key = key[:-1] if is_plural else key
    parent_type = parent._type()
    #P1: not proud of this, but the "plural keys" needs to be corrected for certain contexts. This works for now but I can't explain it well
    if parent_type in props.cfg['filters'].keys() and key == 'filter':
        key = key + 's'
    elif parent_type == 'explore_source' and key == 'bind_filter':
        key = key + 's'
    elif parent_type == 'query' and key in ('dimension','measure'):
        key = key + 's'
    elif parent_type == 'access_grant' and key == 'allowed_value':
        key = key + 's'
    if key == 'query' and parent_type == 'aggregate_table':
        #P1: make more elegant / clean up this fixes an issue where because query is a named construct in the explore
        # and an anonymous construct in the aggregate table I need to take the 1 and only value out because lkml thinks
        # it's a plural key after adding it to the plural keys to fix the issue with explore > query
        value = value[0]
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
        ,'include': prop_includes
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

