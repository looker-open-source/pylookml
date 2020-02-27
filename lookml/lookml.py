import re
import lookml.config as conf
import lkml
import github
import base64
import requests


def snakeCase(string):
    str1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', str1).lower()

def splice(*args):
    return ''.join([arg for arg in args])

def removeSpace(string):  # removing special character / [|]<>,.?}{+=~!$%^&*()-
    return re.sub('(\s|/|\[|\]|\||\,|<|>|\.|\?|\{|\}|#|=|~|!|\+|\$|\%|\^|\&|\*|\(|\)|\-|\:)+', r'', string)

def lookCase(string):
    return removeSpace(snakeCase(string))

def ws_buffer(item):
    def wrapper(*args,**kwargs):
        return splice(
                conf.PRE_FIELD_BUFFER,
                item(*args,**kwargs),
                conf.POST_FIELD_BUFFER
                )
    return wrapper

class Project:
    '''
        A LookML Project at a GitHub location or location on the filesytem
    '''
    def __init__(self,repo='',access_token=''):
        ''' 
            Can be constructed with a github access token and repository name
        '''
        self.gitsession = github.Github(access_token)
        self.repo = self.gitsession.get_repo(repo)
        # self.looker_project_name =
        # self.deploy_url = 
        pass

    def files(self,pattern=''):
        ''' Iteratively returns all the files or those matching a specific pattern '''
        pass

    def models(self, pattern=''):
        ''' Iteratively returns all of the models or those matching a specific pattern'''
        pass

    def getFile(self,path):
        '''  
            returns a single lookml File object 
        '''
        return File(self.repo.get_contents(path))

    def updateFile(self,f):
        '''  
            takes a File object and attempts to re-upload it to the project. 
        '''
        self.repo.update_file(f.path, "auto-update", str(f), sha=f.sha, branch="master")
        pass

    def newFile(self,path):
        '''
            creates a new file in the project and uploads it to github
        '''
        pass

    def deleteFile(self,path):
        '''
            deletes a file from a repository at a specific path
        '''
        pass

class views:
    '''
        A container for views which allows us to use .operator syntax 
    '''
    def __init__(self,viewlist):
        self.views = {}
        for view in viewlist:
            self.add(view)

    def __getattr__(self,key):
        return self.views[key]

    def add(self, v):
        if isinstance(v,dict):
            v = View(v)
        self.views.update({v.name:v})
        return self

    def remove(self, v):
        if not isinstance(v,str):
            v = v.name
        self.views.pop(v)
        return self

    def __iter__(self):
        self.iterPointer = iter(self.views.values())
        return self

    def __next__(self):
        try:
            return next(self.iterPointer)
        except:
            raise StopIteration


class explores:
    '''
        A container for explores which allows us to use .operator syntax 
    '''
    def __init__(self,explorelist):
        self.explores = {}
        for explore in explorelist:
            self.add(explore)

    def __getattr__(self,key):
        return self.explores[key]

    def add(self, e):
        if isinstance(e,dict):
            e = Explore(e)
        self.explores.update({e.name:e})
        return self

    def remove(self, e):
        if not isinstance(e,str):
            e = e.name
        self.explores.pop(e)
        return self

    def __iter__(self):
        self.iterPointer = iter(self.explores.values())
        return self

    def __next__(self):
        try:
            return next(self.iterPointer)
        except:
            raise StopIteration
class File:

    def __init__(self, infilepath):
        '''parse the LookML infilepath, convert to JSON, and then read into JSON object

        Args:
            infilepath (str): path to input LookML file

        Returns:
            JSON object of LookML

        '''

        self.infilepath = infilepath
        if isinstance(self.infilepath, github.ContentFile.ContentFile):
            data = base64.b64decode(self.infilepath.content).decode('ascii')
            self.json_data = lkml.load(data)

        if infilepath._rawData['name'].endswith(".model.lkml"):
            self.filetype = 'model'
        elif infilepath._rawData['name'].endswith(".view.lkml"):
            self.filetype = 'view'
        elif infilepath._rawData['name'].endswith(".explore.lkml"):
            self.filetype = 'explore'
        else:
            raise Exception("Unsupported filename " + infilepath._rawData['name'])
        # self.base_filename = os.path.basename(infilepath)
        self.path = self.infilepath._rawData['path']
        self.sha = self.infilepath._rawData['sha']
        self.base_filename = infilepath._rawData['name']
        self.base_name = self.base_filename.replace(".model.lkml", "").replace(".explore.lkml", "").replace(".view.lkml", "")        

        if 'views' in self.json_data.keys():
            self.vws = views(self.json_data['views'])
        else:
            self.vws = None
        if 'explores' in self.json_data.keys():
            self.exps = explores(self.json_data['explores'])
        else:
            self.exps = None
        

    def __getattr__(self, key):
        if key == 'views':
            return self.vws
        elif key == 'explores':
            return self.exps
        else:
            return object.__getattr__(key)

    def __str__(self):
        return splice(
            conf.NEWLINE.join([ str(e) for e in self.exps.explores.values()] ) if self.exps else ''
            ,conf.NEWLINE,
            conf.NEWLINE.join([ str(v) for v in self.vws.views.values()]) if self.vws else ''
        )

    def addView(self,v):
        self.vws.add(v)
        return self

    def addExplore(self,e):
        self.exps.add(e)
        return self

    def __add__(self, other):
        if isinstance(other, View):
            self.addView(other)
        elif isinstance(other, Explore):
            self.addExplore(other)

class writeable(object):
    def __init__(self, *args, **kwargs):
        self.identifier = kwargs.get('identifier', '')
        if not self.identifier:
            self.identifier = kwargs.get('name', '')
        if not self.identifier:
            if len(args) > 1:
                if isinstance(args[1],str):
                    self.identifier = args[1]
                elif isinstance(args[1],View):
                    self.identifier = args[1].identifier
                elif isinstance(args[0],dict):
                        self.bind_lkml(args[0])
            else:
                self.identifier = ''        
        self.extension = kwargs.get('extension', '.lkml')
        self.fileName = self.identifier + self.extension     
        self.outputFolder = kwargs.get('output_dir',conf.OUTPUT_DIR)
        if self.outputFolder:
            self.path = self.outputFolder  + self.fileName if self.outputFolder.endswith('/') else self.outputFolder  + '/' +  self.fileName
        else:
            self.path = self.fileName
        
    def bind_lkml(self,lkmldict):
        '''Writable is never used, it's only a base class for extension
            Each class inheriting from this must implement bind_lkml
        '''
        pass

    def setFolder(self,folder):
        self.outputFolder = folder
        self.path = self.outputFolder + self.fileName if self.outputFolder.endswith('/') else self.outputFolder  + '/' +  self.fileName
        return self

    def setName(self, identifier):
        ''' create a synonym with identifier'''
        self.identifier = identifier
        return self

    def write(self,overWriteExisting=True):
        ''' Checks to see if the file exists before writing'''
        print("Writing to: %s" % (self.path) )
        if overWriteExisting:
            with open(self.path, 'w') as opened_file:
                try:
                    opened_file.write(self.__str__())
                except:
                    pass
        else:
            try:
                fh = open(self.path, 'r')
                fh.close()
            except FileNotFoundError:
                with open(self.path, 'w') as opened_file:
                    opened_file.write(self.__str__())

class View(writeable):
    __slots__ = [
             'sql_table_name'
            ,'derived_table'
            ,'tableSource'
            ,'message'
            ,'fields'
            ,'primaryKey'
            ,'schema'
            ,'properties'
            ,'children'
            ,'parent'
            ,'fileName'
            ]
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(self, *args, **kwargs)
        if 'sql_table_name' in kwargs.keys():
            self.sql_table_name = Property('sql_table_name', kwargs.get('sql_table_name', 'view'))
            self.tableSource = True
        elif 'derived_table' in kwargs.keys():
            self.derived_table = Property('derived_table', kwargs.get('derived_table', 'view'))
            self.tableSource = False
        else:
            self.tableSource = None
        self.message = kwargs.get('message', '')

        #At Some Point may want to refactor the internal data structures
        # self.dimension_groups = dict()
        # self.dimensions = dict()
        # self.measures = dict()
        # self.filters = dict()
        # self.sets = dict()
        
        self.fields = {}
        self.schema = kwargs.get('schema', {})
        self.properties = Properties(self.schema)
        self.primaryKey = ''

        #If passed a dictionary it is assumed to be the LKML schema
        if len(args) >= 1:
            # print(args)
            if isinstance(args[0],dict):
                self.bind_lkml(args[0])

        self.children = {}
        self.parent = None
        self.fileName = self.identifier + '.view.lkml'
        if self.outputFolder:
            self.path = self.outputFolder  + self.fileName if self.outputFolder.endswith('/') else self.outputFolder  + '/' +  self.fileName
        else:
            self.path = self.fileName
    
    

    def bind_lkml(self,jsonDict):
        self.setName(jsonDict.pop('name'))
        view_keys = [element for element in jsonDict]
        if 'measures' in view_keys:
            for measure in jsonDict['measures']:
                self + Measure(measure)
        else:
            pass

        if 'dimensions' in view_keys:
            for dim in jsonDict['dimensions']:
                self + Dimension(dim)
        else:
            pass
        
        if 'filters' in view_keys:
            for flter in jsonDict['filters']:
                self + Filter(flter)
        else:
            pass

        if 'filters' in view_keys:
            for dim in jsonDict['dimension_groups']:
                self + DimensionGroup(dim)
        else:
            pass


    #TODO define iteration
    # def __iter__(self):
    # def __next__(self):

    def __str__(self):
        return splice(
                        splice('#',self.message,conf.NEWLINE) if self.message else '', 
                        'view: ', self.identifier, ' {', 
                        conf.NEWLINE,self.source(),conf.NEWLINE, 
                        conf.NEWLINE.join([str(p) for p in self.properties.getProperties()]), 
                        conf.NEWLINE.join([str(field) for field in self.getFieldsSorted()]), 
                        splice(conf.NEWLINE,'}',conf.NEWLINE),
                        *[str(child) for child in self.children.values()] if self.children else ''
                        )

    def __repr__(self):
        return "%s (%r) fields: %s" % (self.__class__, self.identifier, len(self)) 

    def __len__(self):
        return len([f for f in self.getFields()])

    def __add__(self,other):
        if isinstance(other, Field):
            return self.addField(other)
        elif isinstance(other, str):
            return self.addDimension(dbColumn=other)
        else: 
            raise Exception(str(type(other)) + ' cannot be added to View')

    def __radd__(self,other):
        return self.__add__(other)

    def __sub__(self,other):
        if isinstance(other, Field):
            return self.removeField(other)
        elif isinstance(other, str):
            return self.removeField(other)
        elif isinstance(other,View):
            return self.children.pop(other.identifier,None)
        else: 
            raise Exception(str(type(other)) + ' cannot be subtracted from View')

    def __rsub__(self,other):
        return self.__sub__(other)

    def __invert__(self):
        ''' hides all dimensions (not measures) '''
        for dim in self.getDimensions():
            dim.hide()
        for dim in self.getDimensionGroups():
            dim.hide()
        for dim in self.getParameters():
            dim.hide()
        for dim in self.getFilters():
            dim.hide()
        return self

    def __contains__(self,item):
        return item in self.fields.keys()

    def __getitem__(self,identifier):
        return self.getField(identifier)

    def __getattr__(self, key):
        # print(self.__dict__.keys())
        if key in self.__dict__.keys():
            return self.__dict__[key]
        # elif key in super.__dict__.keys():
        #     return super.__dict__[key]
        elif key == 'name':
            return self.identifier
        elif key == 'pk':
            return self.getPrimaryKey()
        elif key == 'ref':
            return splice('${',self.identifier,'}')
        # elif key == 'path':
        #     return self.path
        else:
            return self.__getitem__(key)

    def __setattr__(self, name, value):
        if name == 'label':
            self.setLabel(value)
            return self
        elif name == 'name':
            self.setName(value)
            return self
        elif name == 'pk':
            self.setPrimaryKey(value)
            return self
        else:
            object.__setattr__(self, name, value)

    def source(self):
        if self.tableSource == None:
            return ''
        elif self.tableSource == False:
            return str(self.derived_table)
        else:
            return str(self.sql_table_name)

    def setSqlTableName(self,sql_table_name='',schema=''):
        ''' Set the sql table name, returns self'''
        if schema:
            tmp = splice(
                    conf.DB_FIELD_DELIMITER_START, schema , conf.DB_FIELD_DELIMITER_END,'.', 
                    conf.DB_FIELD_DELIMITER_START, sql_table_name ,conf.DB_FIELD_DELIMITER_END
                    )
        else:
            tmp = splice(
                    conf.DB_FIELD_DELIMITER_START, sql_table_name ,conf.DB_FIELD_DELIMITER_END
                    )
        self.sql_table_name = Property('sql_table_name',tmp)
        self.tableSource = True
        self.derived_table = None
        return self

    def setMessage(self, message):
        '''Sets a Commented Message above the view'''
        self.message = ''.join(['#', message])
        return self

    def setLabel(self, label):
        ''' Sets the view label property'''
        self.properties.addProperty('label',label)
        return self

    def setExtensionRequired(self):
        ''' Sets the view to be "extension: required" '''
        self.properties.addProperty('extension','required')
        return self    

    def getFieldsByTag(self,tag):
        for field in self.getFields():
            if tag in field.tags:
                yield field

    def getFields(self):
        '''Returns all the fields as a generator'''
        for field, literal in self.fields.items():
            ## Does this yeild only return the first value of this loop?
            yield literal

    def getFieldsSorted(self):
        ''' returns all the fields sorted first by alpabetical dimensions/filters, then alphabetical measures '''
        return sorted(self.fields.values(), key=lambda field: ''.join([str(isinstance(field, Measure)), field.identifier]))

    def getFieldNames(self):
        ''' Returns field names/identifiers as a generator yielding strings '''
        for field, literal in self.fields.items():
            yield field

    def getField(self, identifier):
        ''' Returns a specific field based on identifier/string lookup'''
        try:
            # print(identifier)
            return self.fields[identifier]
        except KeyError:
            raise KeyError

    def getFieldByDBColumn(self, dbColumn):
        ''' Converts the db column to lookCase for identifier lookup.....'''
        #TODO: re-implement this to actually use the DB column as a key (keep in mind that doesn't need to be unique...)
        #TODO: Raise a not found exception here instead of silently failing with a notfound key
        return self.fields.get(lookCase(dbColumn), Field(identifier='Not Found'))
    
    def addField(self, field):
        '''Takes a field object as an argument and adds it to the view, if the field is a dimension and primary key it will be set as the view primary key'''
        # uses the 'setView' method on field which returns self so that field can fully qualify itself and so that field can be a member of view
        self.fields.update({field.identifier: field.setView(self)})
        # If a primary key is added it will overwrite the existing primary key....
        if isinstance(field, Dimension):
            if field.isPrimaryKey():
                # field.setPrimaryKey()
                self.setPrimaryKey(field.identifier)
        return self
    
    def removeField(self,field):
        '''Removes a field, either by object or by string of identifier, safely checks and de-refs primary key'''
        def pk(k):
            if k.isPrimaryKey():
                self.unSetPrimaryKey()
        if isinstance(field,Field):
            if isinstance(field,Dimension):
                pk(field)
            pk(self.getField(field.identifier))
            return self.fields.pop(field.identifier, None)
        elif isinstance(field,str):
            dimToDel = self.getField(field)
            if isinstance(dimToDel,Dimension):
                pk(dimToDel)
            return self.fields.pop(field, None)
        else:
            raise Exception('Not a string or Field instance provided')

    def addFields(self, fields):
        ''' An iterable collection of field objects will be passed to the add field function. Helpful for adding many fields at once'''
        for field in fields:
            self.addField(field)
        return self

    def setPrimaryKey(self, f, callFromChild=False):
        ''' A string identifier or a field object can be passed, and will be set as the new primary key of the view'''
        self.unSetPrimaryKey()
        if isinstance(f, Dimension):
            if not callFromChild:
                f.setPrimaryKey()
            self.primaryKey = f.identifier
        else:
            tmpField = self.getField(f)
            if isinstance(tmpField, Dimension):
                self.primaryKey = tmpField.identifier
                if not callFromChild:
                    tmpField.setPrimaryKey()
                    # tmpField.setPrimaryKey()
        return self

    def getPrimaryKey(self):
        '''returns the primary key'''
        if self.primaryKey:
            return self.getField(self.primaryKey)

    def unSetPrimaryKey(self):
        '''Unsets the view primary key returns self'''
        # pk = self.getField(self.primaryKey)
        pk = self.getPrimaryKey()
        if isinstance(pk, Dimension):
            pk.unSetPrimaryKey()
        self.primaryKey = ''
        return self

    def getDimensions(self):
        '''returns iterable of Dimension Fields'''
        return filter(lambda dim: isinstance(dim, Dimension), self.fields.values())

    def getDimensionGroups(self):
        '''returns iterable of DimensionGroup Fields'''
        return filter(lambda dim: isinstance(dim, DimensionGroup), self.fields.values())

    def getMeasures(self):
        '''returns iterable of Measure Fields'''
        return filter(lambda meas: isinstance(meas, Measure), self.fields.values())

    def getFilters(self):
        '''returns iterable of Filter Fields'''
        return filter(lambda fil: isinstance(fil, Filter), self.fields.values())

    def getParameters(self):
        '''returns iterable of Paramter Fields'''
        return filter(lambda par: isinstance(par, Parameter), self.fields.values())

    def addDimension(self,dbColumn, type='string'):
        ''' dbColumn is a string representing the column name'''
        dim = Dimension(dbColumn=dbColumn)
        dim.setType(type)
        self.addField(dim)
        return self

    def sum(self,f):
        ''' A Synonym for addSum '''
        return self.addSum(f)

    def count(self):
        ''' A Synonym for addCount'''
        return self.addCout()

    def countDistinct(self,f):
        ''' A Synonym for addCountDistinct'''
        return self.addCountDistinct(f)

    def addCount(self):
        '''Add a count measure to the view, returns self'''
        measure = Measure(
            identifier='count', schema={'type': 'count'}
        )
        self.addField(measure)
        return self

    def addCountDistinct(self, f):
        '''Add a count distinct to the view based on a field object or field name/identifier. returns self'''
        if isinstance(f, Field):
            field = f
        else:
            field = self.getField(f)
        measure = Measure(
            identifier=''.join(['count_distinct_', field.identifier]), schema={'sql': field.ref_short}
        )
        measure.setType('count_distinct')
        self.addField(measure)
        return self

    def addSum(self, f):
        '''Add a sum to the view based on a field object or field name/identifier. returns self'''
        if isinstance(f, Field):
            field = f
        else:
            field = self.getField(f)
        measure = Measure(
            identifier=''.join(['total_', field.identifier]), schema={'sql': field.ref_short}
        )
        measure.setType('sum')
        self.addField(measure)
        return self

    def addAverage(self, f):
        '''Add a average to the view based on a field object or field name/identifier. returns self'''
        if isinstance(f, Field):
            field = f
        else:
            field = self.getField(f)
        measure = Measure(
            identifier=''.join(['average_', field.identifier]), schema={'sql': field.ref_short}
        )
        measure.setType('average')
        self.addField(measure)
        return self

    def addComparisonPeriod(self,field_to_measure,date, measure_type='count_distinct'):
        self.addFields(
                [
                    Filter().setName('reporting_period').setProperty('type','date')
                   ,Filter().setName('comparison_period').setProperty('type','date')
                   ,Measure().setName('reporting_period_measure')
                   ,Measure().setName('comparison_period_measure')
                   ]
                )
        assert isinstance(field_to_measure,Dimension)
        self.reporting_period_measure.setType(measure_type)
        self.comparison_period_measure.setType(measure_type)
        self.comparison_period.setProperty('sql',
        '''
            {0}>= {{% date_start comparison_period  %}}
            AND {0} <= {{% date_end reporting_period %}}
        '''.format('${'+date.identifier+'_raw}')
        )
        self.reporting_period_measure.setProperty(
                'sql'
                ,'''CASE 
                     WHEN {{% condition reporting_period %}} {0} {{% endcondition %}} THEN {1}
                     ELSE NULL
                    END
                    '''.format('${'+date.identifier+'_raw}',field_to_measure.ref_short)
                )
        self.comparison_period_measure.setProperty('sql',
        '''
          CASE 
           WHEN {{% condition comparison_period %}} {0} {{% endcondition %}} THEN {1}
           ELSE NULL
          END
        '''.format('${'+date.identifier+'_raw}',field_to_measure.ref_short)
        )
        return self

    def extend(self, name='', sameFile=True, required=False, *args):
        ''' Creates an extended view, optionally within the same view file 
            name (string) -> name of the extended / child view. Will default to the parent + _extended
            sameFile (boolean) -> default true, if true will result in the child being printed within the parent's string call / file print
            required (boolean) -> default false, if true will result in the parent being set to extension required
            returns the child view object
        '''
        
        if not name:
            if len(args) > 1:
                if isinstance(args[0],str):
                    child = View(args[0])
                else:
                    child = View('_'.join([self.identifier,'extended'])) 
            else:
                child = View('_'.join([self.identifier,'extended']))
        else:
            child = View(name)

        if required:
            self.setExtensionRequired()
        child.properties.addProperty('extends',self.identifier)
        child.parent = self
        if sameFile:
            self.children.update({child.identifier: child})
        return child

class ndt(View):
    def __init__(self,explore_source, *args, **kwargs):
        super(ndt, self).__init__(self, *args, **kwargs)
        self._columns = {}
        self._dcolumns = {}

        if isinstance(explore_source,Explore):
            self._explore_source = explore_source.identifier
        else:
            self._explore_source = explore_source

    def addColumn(self,name,field):
        self._columns.update({name:field})
        return self

    def addDerivedColumn(self,name,field):
        self._dcolumns.update({name:field})
        return self

    def __str__(self):
        return splice(
            'derived_table: {\n',
            'explore_source: ' + self._explore_source + ' ' , ' {',conf.NEWLINEINDENT
             ,conf.NEWLINEINDENT.join(['column: ' + k + ' { field: ' + v + '}' for k,v in self._columns.items()]),conf.NEWLINEINDENT
             ,conf.NEWLINEINDENT.join(['derived_column: ' + k + ' { sql: ' + v + ';; }' for k,v in self._dcolumns.items()])
            ,conf.NEWLINEINDENT,'}',conf.NEWLINE,'}'
        )

class Join(object):
    ''' Instantiates a LookML join object... '''
    __slots__ = ['properties', 'identifier','_from','to']

    def __init__(self, *args, **kwargs):
        self.properties = Properties(kwargs.get('schema', {}))
        self.identifier = kwargs.get('identifier', kwargs.get('view', 'error_view_not_set'))
        self._from = kwargs.get('from', None)
        self.to = kwargs.get('to', None)
        if len(args) >= 1:
            if isinstance(args[0],dict):
                self.bind_lkml(args[0])

    # def __getattribute__(self, key): 
    #     if key == 'name':
    #         return self.identifier
    #     else:
    #         return self.getProperty(key)

    # def __setattr__(self, name, value):
    #     if name in self.__dict__.keys():
    #         self.__dict__[name] = value
    #     else:
    #         object.__setattr__(self, name, value)

    def bind_lkml(self, lkmldict):
            self.setName(lkmldict.pop('name'))
            for k,v in lkmldict.items():
                self.setProperty(k,v) 

    def __str__(self):
        return splice(
                         conf.NEWLINE,'join: ', self.identifier, ' {',conf.NEWLINE,'    ',
                         conf.NEWLINEINDENT.join([str(p) for p in self.properties.getProperties()]),
                         conf.NEWLINE,'}',conf.NEWLINE
                          )

    def setName(self, identifier):
        self.identifier = identifier
        return self

    def setFrom(self,f):
        self._from = f
        return self

    def getProperty(self, prop):
        return self.properties.getProperty(prop)

    def setProperty(self, name, value):
        ''''''
        self.properties.addProperty(name, value)
        return self
    
    def setTo(self,t):
        if isinstance(t,View):
            self.to = t
        return self

    def on(self,left,operand,right):
        statement = splice(left.ref ,operand, right.ref)
        self.setOn(statement)
        return self

    def setOn(self,sql_on):
        self.properties.addProperty('sql_on', sql_on )
        return self

    def setSql(self,sql):
        self.setProperty('sql', sql)
        return self

    def setType(self, joinType):
        assert joinType in conf.JOIN_TYPES
        self.properties.addProperty('type',joinType)
        return self

    def setRelationship(self,rel):
        assert rel in conf.RELATIONSHIPS
        self.properties.addProperty('relationship',rel)
        return self

class Explore(writeable):
    ''' Represents an explore object in LookML'''
    def __init__(self, *args, **kwargs):
        super(Explore, self).__init__(self, *args, **kwargs)
        self.properties = Properties(kwargs.get('schema', {}))
        # self.identifier = kwargs.get('identifier', kwargs.get('view', 'error_view_not_set'))
        self.joins = dict()
        
        self.identifier = kwargs.get('identifier', '')
        self.base_view = kwargs.get('view',View(self.identifier))
        if not self.identifier:
            self.identifier = kwargs.get('name', '')
        if not self.identifier:
            if len(args) >= 1:
                if isinstance(args[0],str):
                    self.setName(args[0])
                elif isinstance(args[0],View):
                    self.setName(args[0].name)
                    self.base_view = args[0]
                elif isinstance(args[0],dict):
                    self.bind_lkml(args[0])
        
        self.fileName = self.identifier + '.explore.lkml'
        if self.outputFolder:
            self.path = self.outputFolder  + self.fileName if self.outputFolder.endswith('/') else self.outputFolder  + '/' +  self.fileName
        else:
            self.path = self.fileName

        

        self.view = kwargs.get('view', '')

    def bind_lkml(self,jsonDict):
        self.setName(jsonDict.pop('name'))
        if 'joins' in jsonDict.keys():
            for join in jsonDict['joins']:
                self + Join(join)        
        jsonDict.pop('joins')
        for k,v in jsonDict.items():
            self.setProperty(k,v)

    def __len__(self):
        return len(self.joins)

    def setProperty(self, name, value):
        ''''''
        self.properties.addProperty(name, value)
        return self

    def __str__(self):
        return splice(
                    '\nexplore: ', self.identifier, ' {\n    ', 
                    '\n    '.join([str(p) for p in self.properties.getProperties()]), 
                    '\n    '.join([str(join) for join in self.getJoins()]),
                     '\n}\n'
                     )

    def __add__(self,other):
        if isinstance(other,View) or isinstance(other,Join):
            self.addJoin(other) 
        else:
            raise TypeError 
        return self
    def __radd__(self,other):
        return self.__add__(other)
    def __getattr__(self, key):

    
        if key == self.base_view.name and self.base_view:
            return self.base_view
        elif key in self.joins.keys():
            return self.joins[key]
        else:
            return self.__getitem__(key)

    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            self.__dict__[name] = value
        else:
            object.__setattr__(self, name, value)

    def __getitem__(self,identifier):
        return self.getJoin(identifier)

    def createNDT(self,explore_source='', name='',fields=[]):
        if name:
            tmpView = View(name)
        else:
            tmpView = View(self.identifier + 'ndt')

        tmpndt = ndt(explore_source)

        for field in fields: 
            tmpndt.addColumn(field.ref_raw_short,field.ref_raw)
            tmpView + field.ref_raw_short
    
        tmpView.derived_table = tmpndt
        tmpView.tableSource = False
        return tmpView

    def setName(self,name): 
        self.identifier = name
        return self

    def setViewName(self,view):
        self.properties.addProperty('view_name',view)

    def addJoin(self, join):
        if isinstance(join,Join):
            self.joins.update({join.identifier : join})
            return join
        elif isinstance(join,View):
            tmpjoin = Join(View)
            tmpjoin.setName(join.name)
            tmpjoin.setTo(join)
            self.joins.update({tmpjoin.identifier : tmpjoin})
            return tmpjoin
        
    def join(self,join):
        return self.addJoin(join)

    def getJoins(self):
        for field, literal in self.joins.items():
            yield literal

    def getJoin(self, key):
        return self.joins.get(key, {})

class Model(writeable):
    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(self, *args, **kwargs)
        self.schema = kwargs.get('schema', {})
        self.properties = Properties(self.schema)
        self.explores = {}
        self.access_grants = {}
        self.fileName = self.identifier + '.model.lkml'
        if self.outputFolder:
            self.path = self.outputFolder  + self.fileName if self.outputFolder.endswith('/') else self.outputFolder  + '/' +  self.fileName
        else:
            self.path = self.fileName       
        
    def __str__(self):
        return splice(
                        '\n'.join([str(p) for p in self.properties.getProperties()]),
                        '\n' * 5, '\n'.join([str(e) for e in self.getAccessGrants()]),
                        '\n' * 5, '\n'.join([str(e) for e in self.getExplores()]),
                        )

    def __getattr__(self, key):
        # print(self.__dict__.keys())
        if key in self.__dict__.keys():
            return self.__dict__[key]
        elif key in self.explores.keys():
        # elif key == 'order_items':
            return self.explores[key]
        else:
            return self.__getitem__(key)


    def setConnection(self,value):
        self.properties.addProperty('connection',value)
        return self

    def include(self,file):
        if isinstance(file,writeable):
            self.properties.addProperty('include',file.fileName)
        else:
            self.properties.addProperty('include',file) 
        return self 

    def addAccessGrant(self, access_grant):
        self.access_grants.update({access_grant.identifier: access_grant})

    def getAccessGrants(self):
        for field, literal in self.access_grants.items():
            yield literal

    def setName(self, name):
       self.setIdentifier(name)
       return self

    def addExplore(self, explore):
        self.explores.update({explore.identifier: explore})

    def getExplores(self):
        for field, literal in self.explores.items():
            yield literal

    def getExplore(self, key):
        return self.explores.pop(key, {})

class Property(object):
    ''' A basic property / key value pair. 
    If the value is a dict it will recusively instantiate properties within itself '''
    __slots__ = ['name', 'value','num']
    def __init__(self, name, value):
        self.name = name
        self.num = 0
        if isinstance(value, str):
            self.value = value
        elif name in ('links','filters','tags','suggestions', 'actions'):
            self.value = Properties(value, multiValueSpecialHandling=name)

        elif isinstance(value, dict) or isinstance(value, list):
            self.value = Properties(value)
        
        else:
            raise Exception('not a dict, list or string')
        
    def __len__(self):
        return len(self.value)

    def __add__(self,other):
        if isinstance(self.value, str):
            pass
        elif isinstance(self.value, Properties):
            self.value.addProperty('tags',other)
        elif isinstance(self.value, list) and self.multiValueSpecialHandling in ('tags','suggestions'):
            self.schema.append(other)
        elif self.properties.multiValueSpecialHandling == 'filters':
            pass
        elif self.properties.multiValueSpecialHandling == 'links':
            pass
        else:
            pass

    def __iter__(self):
        self.num = 0
        return self

    def __next__(self):
        num = self.num
        while num <= len(self.value):
            return next(self.value)

    def __str__(self):
        if self.name.startswith('sql') or self.name == 'html':
            return splice(self.name, ': ', str(self.value), ' ;;')
        elif self.name in ['include', 'connection', 'description','value']:
            return splice(self.name, ': "', str(self.value), '"')
        elif self.name.endswith('url') or self.name.endswith('label') or self.name.endswith('format') or self.name.endswith('persist_for'):
            return splice(self.name, ': "', str(self.value), '"')
        elif self.name == 'extends':
            return splice(self.name, ': [', str(self.value), ']')
        elif self.name.startswith('explore_source'):
            return splice(self.name, str(self.value))
        elif self.name in conf.MULTIVALUE_PROPERTIES:
            return splice(self.name , ': ' , str(self.value))
        elif self.name in ('links','filters'):
            return str(self.value)
        elif self.name == ('list_member') and isinstance(self.value,str):
            return splice(str(self.value),',')
        elif self.name == 'list_member':
            return splice(str(self.value))
        elif self.name == 'list_member_quoted':
            return str(self.value)
        else:
            return splice(self.name , ': ' , str(self.value))



class Properties(object):
    '''
    Treats the collection of properties as a recursive dicitionary
    Things that fall outside of uniqueness (special cases):
    includes, links, filters, bind_filters
    Things that should be their own class:
    data_groups, named_value_format, sets
    '''
    __slots__ = ['schema','multiValueSpecialHandling','num','valueiterator']

    def __init__(self, schema, multiValueSpecialHandling=False):
        self.schema = schema
        self.num = 0
        self.valueiterator = iter(self.schema)
        self.multiValueSpecialHandling = multiValueSpecialHandling

    #TODO: Rewrite for list schema type
    def __str__(self):
        if isinstance(self.schema, dict):
            return splice(
                            '{\n    ' , 
                            '\n    '.join([str(p) for p in self.getProperties()]) ,
                            '\n    }' 
                            )
        elif isinstance(self.schema, list) and not self.multiValueSpecialHandling:
            return splice(
                            '[\n    ' , 
                            '\n    '.join([str(p) for p in self.getProperties()]) ,
                            '\n    ]' 
                            )
        elif isinstance(self.schema, list) and self.multiValueSpecialHandling in ('tags','suggestions'):
            return splice(
                            '[\n    ' , 
                            '\n    '.join(['"' + str(p) + '",' for p in self.getProperties()]) ,
                            '\n    ]' 
                            )
        elif self.multiValueSpecialHandling == 'filters':
            return splice('filters: ','\n filters: '.join([str(p) for p in self.getProperties()]))
        elif self.multiValueSpecialHandling == 'links':
            return splice('link: ','link: \n'.join([str(p) for p in self.getProperties()]))
        else:
            pass
            # raise TypeError

#TODO: Rewrite for list schema type
    def getProperty(self, identifier):
        
        if isinstance(self.schema, dict):
            if identifier == 'sql':
                # return sql_prop(identifier, self.schema.get(identifier, []))
                return Property(identifier, self.schema.get(identifier, []))
            else:    
                return Property(identifier, self.schema.get(identifier, []))
        elif isinstance(self.schema, list):
            if identifier == 'sql':
                # return sql_prop(identifier, self.schema.get(identifier, []))
                return Property(identifier, self.schema.get(identifier, []))
            else:    
                return Property(identifier, self.schema.get(identifier, [])) 

#TODO: Rewrite for list schema type
    def getProperties(self):
        if isinstance(self.schema, dict):
            for k, v in self.schema.items():
                if k in conf.NONUNIQUE_PROPERTIES:
                    for n in v:
                        yield Property(k, n)
                else:
                    yield Property(k, v)
        elif isinstance(self.schema, list):
            for item in self.schema:
                if self.multiValueSpecialHandling in ('suggestions','tags'):
                    yield Property('list_member_quoted',item)
                else:
                    yield Property('list_member',item)


    def __iter__(self):
        # self.num = 0
        self.valueiterator = iter(self.schema)
        return self

    def __next__(self):
        # num = self.num
        # while num <= len(self.schema):
        try:
            return next(self.valueiterator)
        except:
            raise StopIteration


    def __add__(self,other):
        if isinstance(self.schema, dict):
            pass
        elif isinstance(self.schema, list) and not self.multiValueSpecialHandling:
            pass
        elif isinstance(self.schema, list) and self.multiValueSpecialHandling in ('tags','suggestions'):
            self.addProperty(self.multiValueSpecialHandling,other)
        elif self.multiValueSpecialHandling == 'filters':
            pass
        elif self.multiValueSpecialHandling == 'links':
            pass
        else:
            pass

#TODO: Rewrite for list schema type
    def addProperty(self, name, value):
        if name in conf.NONUNIQUE_PROPERTIES:
            index = self.schema.get(name,[])
            index.append(value)
            self.schema.update(
                {name: index}
            )
        elif isinstance(self.schema, list):
            if value not in self.schema:
                self.schema.append(value)
        else:
            self.schema.update({name: value})
#TODO: Rewrite for list schema type
    def delProperty(self, identifier):
        self.schema.pop(identifier, None)
#TODO: Rewrite for list schema type
    def isMember(self, property):
        return property in self.schema.keys()

    def props(self):
        '''
            Returns a list of the property values. Mostly used for membership checking
        '''
        return self.schema.keys()

    def __len__(self):
        return len(self.schema)


class Field(object):
    ''' Base class for fields in LookML, only derived/child types should be instantiated '''
    __slots__ = ['schema', 'properties','db_column','identifier','view','message']
    def __init__(self, *args, **kwargs):
        self.schema = kwargs.get('schema', {})
        self.properties = Properties(self.schema)
        self.db_column = kwargs.get('dbColumn', '')
        self.message = kwargs.get('message', '')

        self.identifier = kwargs.get('identifier', None)
        if not self.identifier:
            self.identifier = kwargs.get('name', None)
        if not self.identifier:
            if len(args) > 1:
                if isinstance(args[1],str):
                    self.setName(args[1])
                    self.db_column = args[1]
            elif self.db_column:
                self.identifier = lookCase(self.db_column)
            else:
                self.identifier = ''

        self.view = kwargs.get('view', '')
        #If passed a dictionary it is assumed to be the LKML schema
        if len(args) > 1:
            if isinstance(args[1],dict):
                self.bind_lkml(args[1])

    def bind_lkml(self, lkmldict):
            self.setName(lkmldict.pop('name'))
            for k,v in lkmldict.items():
                self.setProperty(k,v) 

    def setMessage(self,message):
        self.message = message
        return self

    def getMessage(self):
        if self.message:
            return splice('#',self.message,conf.NEWLINE)
        else:
            return ''
    

    def __str__(self):
        return splice(
                        self.identifier, splice(' {',conf.NEWLINEINDENT), 
                            conf.NEWLINEINDENT.join([str(n) for n in self.properties.getProperties()]),
                            splice(conf.NEWLINE,'}')
                         )

    def __getattr__(self, key):
        if key == 'name':
            return self.identifier
        elif key == 'pk':
            return self.getPrimaryKey()
        elif key == 'ref':
            if self.view:
                return splice('${' , self.view.identifier , '.' , self.identifier , '}')
        elif key == 'ref_raw':
            if self.view:
                return splice(self.view.identifier , '.' , self.identifier)
        elif key == 'ref_raw_short':
            if self.view:
                return splice(self.identifier)
        elif key == 'ref_short':
            return splice('${' , self.identifier , '}')
        else:
            return self.properties.getProperty(key)

    def __setattr__(self, name, value):
        if name == 'label':
            self.setLabel(value)
            return self
        elif name == 'name':
            self.setName(value)
            return self
        # elif name in self.properties.props():
        elif name in conf.FIELD_LEVEL_PROPS:
            return self.setProperty(name,value)
        else:
            object.__setattr__(self, name, value)

    def setDescription(self,value):
        return self.setProperty('description', value)

    def addTag(self,tag):
        if self.properties.isMember('tags'):
            if tag not in self.tags:
                # self.tags.value.schema['tags'].append(tag)
                self.tags.value.schema.append(tag)
            #Else it's already a member
        else:
            self.setProperty('tags',[tag])

    def removeTag(self,tag):
        if self.properties.isMember('tags'):
            self.tags.value.schema.remove(tag)
        else:
            pass
            #TODO: raise an error

    def setView(self, view):
        '''
        '''
        self.view = view
        return self  # satisfies a need to linkback (look where setView is called)

    def setName(self,identifier):
        self.identifier = identifier
        return self

    def setProperty(self, name, value):
        ''''''
        self.properties.addProperty(name, value)
        return self

    def unSetProperty(self, name):
        ''''''
        self.properties.delProperty(name)
        return self

    def setSql(self, sql):
        self.setProperty('sql', sql)
        return self

    def getProperty(self, identifier):
        ''''''
        return self.properties.getProperty(identifier)

    def setType(self, type):
        ''''''
        self.properties.addProperty('type', type)
        return self

    def setNumber(self):
        ''''''
        return self.setType('number')

    def setString(self):
        ''''''
        return self.setType('string')

    def setLabel(self, label):
        ''''''
        return self.setProperty('label', label)

    def setViewLabel(self, viewLabel):
        ''''''
        return self.setProperty('view_label', viewLabel)

    def hide(self):
        ''''''
        self.properties.addProperty('hidden', 'yes')
        return self

    def unHide(self):
        ''''''
        self.properties.delProperty('hidden')
        return self

    def set_Field_Level_Permission(self, access_grant):
        if isinstance(access_grant,str):
            self.setProperty('required_access_grants', '[' + ','.join([access_grant]) + ']')
        elif isinstance(access_grant,list):
            self.setProperty('required_access_grants', '[' + ','.join(access_grant) + ']')
        return self

    def sql_nvl(self,value_if_null):
        self.sql = "NVL(" + str(self.sql.value) + "," + value_if_null + ")"


class Dimension(Field):
    def __init__(self, *args, **kwargs):
        super(Dimension, self).__init__(self, *args, **kwargs)
        # self.setDBColumn(self.db_column,changeIdentifier=False)


    def isPrimaryKey(self):
        if self.properties.isMember('primary_key') and self.properties.getProperty('primary_key').value == 'yes':
            return True
        else:
            return False

    def setDBColumn(self, dbColumn, changeIdentifier=True):
        ''''''
        self.db_column = dbColumn
        self.setProperty('sql', splice('${TABLE}.' , conf.DB_FIELD_DELIMITER_START , self.db_column , conf.DB_FIELD_DELIMITER_END))
        if changeIdentifier:
            self.identifier =lookCase(self.db_column)
        return self

    def setAllLabels(self, group: None, item: None, label: None):
        if group:
            self.setProperty('group_label', group)
        if item:
            self.setProperty('group_item_label', item)
        if label:
            self.setProperty('label', label)
        return self

    def setPrimaryKey(self):
        self.setProperty('primary_key', 'yes')
        # self.view.setPrimaryKey(self.identifier, callFromChild=True)
        return self

    def unSetPrimaryKey(self):
        self.unSetProperty('primary_key')
        return self

    def setTier(self, tiers=[]):
        if tiers:
            self.setProperty('tiers', '[0,5,10,15,20]')
        else:
            self.setProperty('tiers', '[' + ','.join(tiers) + ']')
        return self.setType('tier')

    def addLink(self,url,label,icon_url='https://looker.com/favicon.ico'):
        self.properties.addProperty('link',{
             'url'     :url
            ,'label'   :label
            ,'icon_url':icon_url
        })
        return self

    @ws_buffer
    def __str__(self):
        return splice( self.getMessage(),
                        'dimension: ', 
                        super(Dimension, self).__str__()
                        )

class DimensionGroup(Field):
    def __init__(self, *args, **kwargs):
        super(DimensionGroup, self).__init__(self, *args, **kwargs)
        if not self.properties.isMember('timeframes'):
            self.properties.addProperty('timeframes', splice('[','{},'.format(conf.NEWLINEINDENT).join(conf.TIMEFRAMES),']'))
        if not self.properties.isMember('type'):
            self.properties.addProperty('type', 'time')
        if not self.properties.isMember('sql'):
            self.properties.addProperty('sql', splice('${TABLE}.' , conf.DB_FIELD_DELIMITER_START , self.db_column , conf.DB_FIELD_DELIMITER_END))

    def setDBColumn(self, dbColumn, changeIdentifier=True):
        ''''''
        self.db_column = dbColumn
        self.setProperty('sql', splice('${TABLE}.' , conf.DB_FIELD_DELIMITER_START , self.db_column , conf.DB_FIELD_DELIMITER_END))
        if changeIdentifier:
            self.identifier = lookCase(self.db_column)
        return self
    
    @ws_buffer
    def __str__(self):
        return splice(self.getMessage(),
                        'dimension_group: ', 
                        super(DimensionGroup, self).__str__()
                        )

class Measure(Field):
    def __init__(self, *args, **kwargs):
        super(Measure, self).__init__(self, *args, **kwargs)


    @ws_buffer
    def __str__(self):
        return splice(self.getMessage(),
                        'measure: ', 
                        super(Measure, self).__str__()
                        )

class Filter(Field):
    def __init__(self, *args, **kwargs):
        super(Filter, self).__init__(self, *args, **kwargs)

    @ws_buffer
    def __str__(self):
        return splice(self.getMessage(),
                        'filter: ', 
                        super(Filter, self).__str__()
                        )

class Parameter(Field):
    def __init__(self, *args, **kwargs):
        super(Parameter, self).__init__(self, *args, **kwargs)
    
    @ws_buffer
    def __str__(self):
        return splice(self.getMessage(),
                        'parameter: ', 
                        super(Parameter, self).__str__()
                        )

class Field_Level_Permissions(Field):
    def __init__(self, *args, **kwargs):
        super(Field_Level_Permissions, self).__init__(self, *args, **kwargs)

    @ws_buffer
    def __str__(self):
        return splice(self.getMessage(),
                        '\naccess_grant: ', 
                        super(Field_Level_Permissions, self).__str__()
                        )
    
    def set_User_Attribute(self, user_attribute):
        return self.setProperty('user_attribute', user_attribute)
         
    def set_Allowed_Value(self, allowed_value):
        return self.setProperty('allowed_values', '["%s"]' %allowed_value)                        

