import re, os
import lookml.config as conf
import lkml
import github
import base64
import requests
import time, copy
from string import Template


#Required for V1:
# TODO: Whitespace issues 
# TODO: bring in old code allowing shell git access 


# ###### V2 ########### 
# TODO: rationally break up the megafile...
# TODO: rationalize operator overloading
# get model metadata from API --> go where?
# TODO: Constants
# TODO: use lkml.keys to define parameter / property specific behavior
# TODO: customize attibute access on JOIN class
# TODO: get a better handle on __getattr__ infite loops and fix consitently
# TODO: leverage inheretance on the dunder methods
# TODO: go back and add slots optimizations
# TODO: track all ancestors, all decendants (grandchildren) in a file
# TODO: equality operator for object comparison | complete some of the dundermethod operator overloading schemes
# TODO: parse manifest file
# TODO: parse locale json file (i.e. localizaiton)
# TODO: Add support for defining a user's config file in the working directory which allows easy configuration / scripting 
# TODO: internal optimizations: good abstractions, no unnecessary memory, better internal class structure / data strcuture  
# TODO: better whitespace and style control
# TODO: adding comment messages at the top of all object types: view, file, explore etc
# TODO: documentation standards in code -- docstrings, function descriptions etc...
# TODO: go through and create / optimize slots for performance
# TODO: Common Sql Functions added to the SQL paramter
# TODO: use lkml.json_data to serve as the underlying data structure (plural keys, keys with name fields etc)
# TODO: eliminate the "phanton property" in that a class instance is only created on get / observation.... (getters and setters should mutate the underlying json at all times to ensure conssistency)

# ###### Post V2 #######
# TODO: Boilerplate Code for this... [super view example...multi-model example...liveupdate service (lambda / cloud funcitons)]
# TODO: Common Macros --> i.e. fast blocks 
#         # Ideas:
#         #  BigQuery table JSON auto creates the LookML
#         #  Aggregate Awareness Macro
#         #  Auto EAV Unnester
#         #  Automatic Creation of NDT for pivot by rank type stuff
#         #  Calendar Table
#         #  SFDC Waterfall
#         #  Guided Star Schema Generation?
#         #  Multi Grain period over period 
#         #  Drill to vis with constants
#         #  Incremental PDTs? --> This breaks as of Looker 7?
#         #  Negative Intervals Hacking
#         #  Linking macro, Intel linking block?
#         #  Fancy Conditional Formatting examples
#         #  Something with slowly changing dimensions
# TODO: Interactive block construction macro --> i.e. fast blocks 
# TODO: Parse the Manifest file
# TODO: Common HTML Functions added to the HTML paramter
# ### Long term or debatable ###
# TODO: Preserve initial ordering?

# TODO: Enhanecement: Make the internal datastructure of the class the JSON.... i.e. as the class state is modified so is the underlying json.


def snakeCase(string):
    str1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', str1).lower()

def splice(*args):
    return ''.join([arg for arg in args])

def removeSpace(string):  # removing special character / [|]<>,.?}{+=~!$%^&*()-
    return re.sub('(\s|/|\[|\]|\||\,|<|>|\.|\?|\{|\}|#|=|~|!|\+|\$|\%|\^|\&|\*|\(|\)|\-|\:)+', r'', string)

def lookCase(string):
    return removeSpace(snakeCase(string))

def sortMe(func):
    ''' returns all the fields sorted first by alpabetical dimensions/filters, then alphabetical measures '''
    return sorted(list(func), key=lambda field: field.identifier)

def stringify(collection,delim=conf.NEWLINEINDENT, prefix=True):
    '''
        calls string and concatinates each item in a collection
    '''
    # return delim + delim.join([str(item) for item in collection])
    return  (delim if prefix else '') + delim.join([str(item) for item in collection])

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
    def __init__(
                    self,
                    repo='',
                    access_token='', 
                    branch="master", 
                    commitMessage="", 
                    rootDir="", 
                    looker_host="",
                    looker_project_name=""
                ):
        ''' 
            Can be constructed with a github access token and repository name
        '''
        self.type = "github"
        self.gitsession = github.Github(access_token)
        self.repo = self.gitsession.get_repo(repo)
        self.branch = branch
        if not commitMessage:
            self.commitMessage = "PyLookML Auto Updated: " + time.strftime('%h %d %Y @ %I:%M%p %Z')
        
        self.looker_host = looker_host
        if self.looker_host and not looker_host.startswith('https://'):
            self.looker_host = 'https://' + looker_host 
            if not self.looker_host.endswith('/'):
                self.looker_host = self.looker_host + '/'
    
        self.looker_project_name = looker_project_name
        self.deploy_url = ""
        self.constructDeployUrl()

    def constructDeployUrl(self):
        '''
            Constructs a github deploy URL according to this pattern:
            https://prod.host.com/webhooks/projects/projectname/deploy
        '''
        if self.looker_project_name and self.looker_host:
            self.deploy_url = self.looker_host + 'webhooks/projects/' + self.looker_project_name + '/deploy'

    def deploy(self):
        if self.deploy_url:
            requests.get(self.deploy_url)

    def files(self,path=''):
        ''' Iteratively returns all the files at a path in the project '''
        for f in  self.repo.get_contents(path):
            yield File(f)

    def file(self,path):
        '''  
            returns a single lookml File object 
        '''
        return File(self.repo.get_contents(path))

    def update(self,f):
        '''  
            takes a File object and attempts to re-upload it to the project. 
        '''
        self.repo.update_file(f.path, self.commitMessage, str(f), sha=f.sha, branch=self.branch)
        return self

    def add(self,f):
        '''
            creates a new file in the project and uploads it to github
        '''
        self.repo.create_file(f.path, self.commitMessage, str(f), branch=self.branch)
        return self

    def put(self,f):
        ''' add or update '''
        # print(f.path)
        if self.exists(f):
            if f.sha:
                self.update(f)
            else:
                f2 = self.file(f.path)
                f.setSha(f2.sha)
                self.update(f)
        else:
            self.add(f)
        

    def exists(self,f):
        '''
            returns boolean if the file exists on 
        '''
        def checkgithub(f0):
            try:
                self.repo.get_contents(f0)
                return True
            except github.GithubException as e:
                if e._GithubException__status == 404:
                    return False
        if isinstance(f,File):
            return checkgithub(f.path)
        elif isinstance(f,str):
            return checkgithub(f)

    def delete(self,f):
        '''
            deletes a file from a repository at a specific path
        '''
        if isinstance(f,str):
            f = self.getFile(f)
        self.repo.delete_file(f.path, self.commitMessage, sha=f.sha, branch=self.branch)
        return self

class File:
    class view_collection:
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
    class explore_collection:
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
    def __init__(self, f):
        def githubBootstrap():
            #custom initialization for github_api type
            #Set Basic Attributes
            self.name = f._rawData['name']
            self.sha = f._rawData['sha']
            self.base_name = self.name.replace(".model.lkml", "").replace(".explore.lkml", "").replace(".view.lkml", "")
            self.path = f._rawData['path']
            #Parse Step: Github content is returned base64 encoded
            data = base64.b64decode(f.content).decode('ascii')
            self.json_data = lkml.load(data)

        def filepathBootstrap():
            #custom initialization for path type
            #Set Basic Attributes
            self.name = os.path.basename(f)
            self.base_name = self.name.replace(".model.lkml", "").replace(".explore.lkml", "").replace(".view.lkml", "")
            self.path = os.path.relpath(f)
            self.sha = ''
            #Parse Step: file is provided 
            with open(self.path, 'r') as tmp:
                self.json_data = lkml.load(tmp)

        def viewBootstrap():
            #custom initialization for path type
            #Set Basic Attributes
            self.name = f.name + '.view.lkml'
            self.base_name = f.name
            self.path = self.name
            self.sha = ''
            #load as json_Data for compatibility with the rest of the class
            #TODO: revist if this is needed to convert back and forth or if another more direct method would be preferable
            self.json_data = lkml.load(str(f))

        def exploreBootstrap():
            #custom initialization for path type
            #Set Basic Attributes
            self.name = f.name + '.explore.lkml'
            self.base_name = f.name
            self.path = self.name
            self.sha = ''
            #load as json_Data for compatibility with the rest of the class
            #TODO: revist if this is needed to convert back and forth or if another more direct method would be preferable
            self.json_data = lkml.load(str(f))

        #Step 1 -- Data Type introspection
        if isinstance(f, github.ContentFile.ContentFile):
            self.f_type = "github_api"
            githubBootstrap()
        elif isinstance(f, View):
            self.f_type = "view"
            viewBootstrap()
        elif isinstance(f, Explore):
            self.f_type = "explore"
            exploreBootstrap()
        elif os.path.isfile(f):
            self.f_type = "path"
            filepathBootstrap()

        #Step 2 -- set a lookml "file type" mostly only used for path info 
        if self.name.endswith(".model.lkml"):
            self.filetype = 'model'
        elif self.name.endswith(".view.lkml"):
            self.filetype = 'view'
        elif self.name.endswith(".explore.lkml"):
            self.filetype = 'explore'
        else:
            raise Exception("Unsupported filename " + self.name)
            
        if 'views' in self.json_data.keys():
            self.vws = self.view_collection(self.json_data['views'])
            self.json_data.pop('views')
        else:
            self.vws = self.view_collection({})
        if 'explores' in self.json_data.keys():
            self.exps = self.explore_collection(self.json_data['explores'])
            self.json_data.pop('explores')
        else:
            self.exps = self.explore_collection({})

        self.properties = Properties(self.json_data)
        self.props = self.properties.props()


    def __getattr__(self, key):
        if key in self.__dict__.keys():
            return self.__dict__[key]
        elif key == 'views':
            return self.vws
        elif key == 'explores':
            return self.exps
        #TODO: resolve attribute access issues
        elif key in ['datagroups', 'map_layers', 'named_value_formats']:
            return self.properties.getProperty(key)
        else:
            return object.__getattr__(key)

    def __str__(self):
        return splice(
             conf.NEWLINE.join([str(p) for p in self.properties.getProperties()])
            ,conf.NEWLINE
            ,conf.NEWLINE.join([ str(e) for e in self.explores] ) if self.exps else ''
            ,conf.NEWLINE
            ,conf.NEWLINE.join([ str(v) for v in self.views]) if self.vws else ''
        )

    def setSha(self,sha):
        self.sha = sha
        return self

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

    def setFolder(self,folder):
        self.outputFolder = folder
        self.path = self.outputFolder + self.fileName if self.outputFolder.endswith('/') else self.outputFolder  + '/' +  self.fileName
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

class base(object):
    def __init__(self,input):
        self.identifier = ''
        self.properties = Properties({})
        self.message = ''
        self.token = ''
        self.indentLevel = 1
        if isinstance(input,str):
            self.setName(input)
        elif isinstance(input,dict):
            self.bind_lkml(input)
        self.templateMap = {}
        
    def bind_lkml(self, lkmldict):
            self.setName(lkmldict.pop('name'))
            for k,v in lkmldict.items():
                self.setProperty(k,v) 

    def setName(self, identifier):
        ''' create a synonym with identifier'''
        self.identifier = identifier
        return self
        
    def setLabel(self, label):
        ''''''
        return self.setProperty('label', label)

    def setMessage(self,message):
        self.message = message 
        return self

    def getMessage(self):
        if self.message:
            return splice('#',self.message,conf.NEWLINE)
        else:
            return ''
    
    def getProperty(self, prop):
        ''' Get a property from the properties collection '''
        return self.properties[prop]

    def setProperty(self, name, value):
        ''' Set a property in the properties collection '''
        self.properties.addProperty(name, value)
        return self

    def unSetProperty(self, name):
        ''''''
        self.properties.__del__(name)
        return self

    def getProperties(self):
        return self.properties.getProperties()

    def hasProp(self, property):
        return property in self.properties.props()

    def props(self):
        return self.properties.props()

    def rawProp(self,key):
        '''
            if dict type schema, needs a prop name. If list type schema needs a number index
        '''
        return self.properties.rawPropValue(key)

    def __len__(self):
        return len(self.schema)

    def __repr__(self):
        # return "%s (%r) name: %s id: %s" % (self.__class__, self.identifier, len(self), hex(id(self))) 
        return "%s  name: %s id: %s" % (self.__class__, self.identifier, hex(id(self))) 

    def __len__(self):
        return len([f for f in self.getProperties()])

    def __iter__(self):
        self.valueiterator = iter(self.getProperties())
        return self

    def __next__(self):
        try:
            return next(self.valueiterator)
        except:
            raise StopIteration

    def __str__(self):
        self.templateMap = {
             'message': self.getMessage()
            ,'identifier': self.identifier
            ,'props': stringify([ conf.INDENT + str(p) for p in self.getProperties()])
            ,'token': self.token
        }
        return Template(getattr(conf.TEMPLATES,self.token)).substitute(**self.templateMap)


class View(base):
    def __init__(self, input):
        self._fields = {}
        self.primaryKey = ''
        self.message = ''
        self.children = {}
        self.parent = None
        super(View, self).__init__(input)
        self.token = 'view'


    def __str__(self):
        self.templateMap = {
             'message':self.getMessage()
            ,'token':self.token 
            ,'identifier':self.identifier
            ,'props': stringify([str(p) for p in self.getProperties() if p.name != "sets"]) 
            ,'parameters':stringify(sortMe(self.parameters()))
            ,'filters': stringify(sortMe(self.filters()))
            ,'dimensions': stringify(sortMe(self.dims()))
            ,'dimensionGroups': stringify(sortMe(self.dimensionGroups()))
            ,'measures': stringify(sortMe(self.measures()))
            ,'sets': stringify([str(p) for p in self.getProperties() if p.name == "sets"]) 
            ,'children': stringify(self.children.values()) if self.children else ''
        } 
        return Template(getattr(conf.TEMPLATES,self.token)).substitute(**self.templateMap)

    def bind_lkml(self,jsonDict):
        t = 'measures'
        if t in jsonDict.keys():
            for field in jsonDict[t]:
                self + Measure(field)
                
            jsonDict.pop(t)
        else:
            pass

        t = 'dimensions'
        if t in jsonDict.keys():
            for field in jsonDict[t]:
                self + Dimension(field)
                
            jsonDict.pop(t)
        else:
            pass
        
        t = 'filters'
        if t in jsonDict.keys():
            for field in jsonDict[t]:
                self + Filter(field)
            
            jsonDict.pop(t)
        else:
            pass

        t = 'dimension_groups'
        if t in jsonDict.keys():
            for field in jsonDict[t]:
                self + DimensionGroup(field)
            
            jsonDict.pop(t)
        else:
            pass

        t = 'parameters'
        if t in jsonDict.keys():
            for field in jsonDict[t]:
                self + Parameter(field)

            jsonDict.pop(t)
        else:
            pass

        super().bind_lkml(jsonDict)


    def getFieldsSorted(self):
        ''' returns all the fields sorted first by alpabetical dimensions/filters, then alphabetical measures '''
        return sorted(self._fields.values(), key=lambda field: ''.join([str(isinstance(field, Measure)), field.identifier]))

    def __repr__(self):
        return "%s (%r) fields: %s id: %s" % (self.__class__, self.identifier, len(self), hex(id(self))) 

    def __len__(self):
        return len([f for f in self.fields()])

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
        for dim in self.dims():
            dim.hide()
        for dim in self.dimensionGroups():
            dim.hide()
        for dim in self.parameters():
            dim.hide()
        for dim in self.filters():
            dim.hide()
        return self

    def __contains__(self,item):
        return item in self._fields.keys()

    def __getitem__(self,identifier):
        return self.field(identifier)

    def __getattr__(self, key):
        if key in self.__dict__.keys():
            return self.__dict__[key]
        elif key == 'name':
            return self.identifier
        elif key == 'pk':
            return self.getPrimaryKey()
        elif key == '__ref__':
            return splice('${',self.identifier,'}')
        else:
            return self.field(key)

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

    def setExtensionRequired(self):
        ''' Sets the view to be "extension: required" '''
        self.properties.addProperty('extension','required')
        return self    

    def getFieldsByTag(self,tag):
        for field in self.fields():
            if tag in field.tags:
                yield field

    def fields(self):
        '''Returns all the fields as a generator'''
        for field, literal in self._fields.items():
            ## Does this yeild only return the first instance it is looped?
            yield literal

    def fieldNames(self):
        return list(self._fields.keys())

    def getFieldsByType(self, t):
        return filter(lambda field: str(field.type) == 'type: '+ t, list(self._fields.values()))

    def sumAllNumDimensions(self):
        '''
            Adds a "total" measure  to the view for all number dimensions
        '''
        for field in self.getFieldsByType('number'):
            tmpFieldName = 'total_' + field.name 
            if  tmpFieldName not in self.fieldNames() and isinstance(field,Dimension):
                self + Measure({
                    'name': tmpFieldName
                    ,'type':'sum'
                    ,'sql':field.__refs__
                })

    def field(self, f):
        ''' retrieve a field, argument can be the name or a field'''
        if isinstance(f,str):
            try:
                return self._fields[f]
            except KeyError:
                raise KeyError
        elif isinstance(f,Field):
            return self._fields[f.identifier]

    def search(self, prop, pattern):
        ''' pass a regex expression and will return the fields whose sql match '''
        if isinstance(pattern,list):
            pattern = '('+'|'.join(pattern)+')'
        searchString = r''.join([r'.*',pattern,r'.*'])
        for field in self.fields():
            if re.match(searchString,str(field.getProperty(prop))):
                yield field

    def addField(self, field):
        '''Takes a field object as an argument and adds it to the view, if the field is a dimension and primary key it will be set as the view primary key'''
        # uses the 'setView' method on field which returns self so that field can fully qualify itself and so that field can be a member of view
        self._fields.update({field.identifier: field.setView(self)})
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
            pk(self.field(field.identifier))
            return self._fields.pop(field.identifier, None)
        elif isinstance(field,str):
            dimToDel = self.field(field)
            if isinstance(dimToDel,Dimension):
                pk(dimToDel)
            return self._fields.pop(field, None)
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
            tmpField = self.field(f)
            if isinstance(tmpField, Dimension):
                self.primaryKey = tmpField.identifier
                if not callFromChild:
                    tmpField.setPrimaryKey()
                    # tmpField.setPrimaryKey()
        return self

    def getPrimaryKey(self):
        '''returns the primary key'''
        if self.primaryKey:
            return self.field(self.primaryKey)

    def unSetPrimaryKey(self):
        '''Unsets the view primary key returns self'''
        # pk = self.field(self.primaryKey)
        pk = self.getPrimaryKey()
        if isinstance(pk, Dimension):
            pk.unSetPrimaryKey()
        self.primaryKey = ''
        return self

    def dims(self):
        '''returns iterable of Dimension Fields'''
        return filter(lambda dim: isinstance(dim, Dimension), self._fields.values())

    def dimensionGroups(self):
        '''returns iterable of DimensionGroup Fields'''
        return filter(lambda dim: isinstance(dim, DimensionGroup), self._fields.values())

    def measures(self):
        '''returns iterable of Measure Fields'''
        return filter(lambda meas: isinstance(meas, Measure), self._fields.values())

    def filters(self):
        '''returns iterable of Filter Fields'''
        return filter(lambda fil: isinstance(fil, Filter), self._fields.values())

    def parameters(self):
        '''returns iterable of Paramter Fields'''
        return filter(lambda par: isinstance(par, Parameter), self._fields.values())

    def addDimension(self,dbColumn, type='string'):
        ''' '''
        dim = Dimension(dbColumn)
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
        measure = Measure( 'count' )
        measure.setType('count')
        self.addField(measure)
        return self

    def addCountDistinct(self, f):
        '''Add a count distinct to the view based on a field object or field name/identifier. returns self'''
        if isinstance(f, Field):
            field = f
        else:
            field = self.field(f)
        measure = Measure( 'count_distinct_' + field.identifier)
        measure.sql = field.__refs__
        measure.setType('count_distinct')
        self.addField(measure)
        return self

    def addSum(self, f):
        '''Add a sum to the view based on a field object or field name/identifier. returns self'''
        if isinstance(f, Field):
            field = f
        else:
            field = self.field(f)
        measure = Measure( ''.join(['total_', field.identifier]))
        measure.setType('sum')
        self.addField(measure)
        return self

    def addAverage(self, f):
        '''Add a average to the view based on a field object or field name/identifier. returns self'''
        if isinstance(f, Field):
            field = f
        else:
            field = self.field(f)
        measure = Measure(
            identifier=''.join(['average_', field.identifier]), schema={'sql': field.__refs__}
        )
        measure.setType('average')
        self.addField(measure)
        return self

    def addComparisonPeriod(self,field_to_measure,date, measure_type='count_distinct'):
        self.addFields(
                [
                    Filter('reporting_period').setName('reporting_period').setProperty('type','date')
                   ,Filter('comparison_period').setName('comparison_period').setProperty('type','date')
                   ,Measure('reporting_period_measure').setName('reporting_period_measure')
                   ,Measure('comparison_period_measure').setName('comparison_period_measure')
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
                    '''.format('${'+date.identifier+'_raw}',field_to_measure.__refs__)
                )
        self.comparison_period_measure.setProperty('sql',
        '''
          CASE 
           WHEN {{% condition comparison_period %}} {0} {{% endcondition %}} THEN {1}
           ELSE NULL
          END
        '''.format('${'+date.identifier+'_raw}',field_to_measure.__refs__)
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

class Join(base):
    ''' Instantiates a LookML join object... '''

    def __init__(self, input):
        self.properties = Properties({})
        self.identifier = ''
        self._from = ''
        self.to = ''
        super(Join,self).__init__(input)
        self.token = 'join'

    def setFrom(self,f):
        self._from = f
        return self
    
    def setTo(self,t):
        if isinstance(t,View):
            self.to = t
        return self

    def on(self,left,operand,right):
        statement = splice(left.__ref__ ,operand, right.__ref__)
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

class Explore(base):
    ''' Represents an explore object in LookML'''
    def __init__(self, input):
        self.joins = {}
        self.base_view = ''
        super(Explore, self).__init__(input)
        self.token = 'explore'

            
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

    def __str__(self):
        self.templateMap = {
             'message': self.getMessage()
            ,'identifier':self.identifier
            ,'props': stringify([str(p) for p in self.getProperties()])
            ,'joins': stringify([str(j) for j in self.getJoins()])
            ,'token': self.token
        }
        return Template(getattr(conf.TEMPLATES,self.token)).substitute(**self.templateMap)

    def __add__(self,other):
        if isinstance(other,View) or isinstance(other,Join):
            self.addJoin(other) 
        else:
            raise TypeError 
        return self
    
    def __radd__(self,other):
        return self.__add__(other)

    def __getattr__(self, key):
        if self.base_view and key == self.base_view.name:
            return self.base_view
        elif key == 'name':
            return self.identifier
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
            tmpndt.addColumn(field.__refrs__,field.__refr__)
            tmpView + field.__refrs__
    
        tmpView.derived_table = tmpndt
        tmpView.tableSource = False
        return tmpView

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

class Property(object):
    ''' A basic property / key value pair. 
    If the value is a dict it will recusively instantiate properties within itself '''
    __slots__ = ['name', 'value','num']
    def __init__(self, name, value):
        self.name = name
        self.num = 0
        if isinstance(value, str):
            self.value = value
        # lkml.keys.PLURAL_KEYS
        # ('view', 'measure', 'dimension', 'dimension_group', 'filter', 'access_filter', 
        # 'bind_filter', 'map_layer', 'parameter', 'set', 'column', 'derived_column', 'include', 
        # 'explore', 'link', 'when', 'allowed_value', 'named_value_format', 'join', 'datagroup', 'access_grant', 
        # 'sql_step', 'action', 'param', 'form_param', 'option', 'user_attribute_param', 'assert', 'test')
        elif name in ('links','filters','tags','suggestions', 'actions', 'sets', 'options', 'form_params', 'access_grants','params','allowed_values', 'named_value_formats', 'datagroups', 'map_layers'):
        # elif name+'s' in lkml.keys.PLURAL_KEYS:
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

    def __sub__(self,other):
        if isinstance(self.value, Properties) and self.value.multiValueSpecialHandling in ('tags','suggestions'):
            self.value.schema.remove(other)
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
        #TODO: multiinstance / plural
        #TODO: multivalue / list
            #TODO: brackets
            #TODO: braces
        #TODO: quoted
        #TODO: plain
        #TODO: SQL / HTML Block ;;

        def quote_pair():
            pass
        
    # lkml.keys.PLURAL_KEYS
    # ('view', 'measure', 'dimension', 'dimension_group', 'filter', 'access_filter', 
    # 'bind_filter', 'map_layer', 'parameter', 'set', 'column', 'derived_column', 'include', 
    # 'explore', 'link', 'when', 'allowed_value', 'named_value_format', 'join', 'datagroup', 'access_grant', 
    # 'sql_step', 'action', 'param', 'form_param', 'option', 'user_attribute_param', 'assert', 'test')
    # lkml.keys.KEYS_WITH_NAME_FIELDS
    # ('user_attribute_param', 'param', 'form_param', 'option')
    # lkml.keys.QUOTED_LITERAL_KEYS
    # ('label', 'view_label', 'group_label', 'group_item_label', 'suggest_persist_for', 
    # 'default_value', 'direction', 'value_format', 'name', 'url', 'icon_url', 'form_url', 'default', '
    # tags', 'value', 'description', 'sortkeys', 'indexes', 'partition_keys', 'connection', 'include', 
    # 'max_cache_age', 'allowed_values', 'timezone', 'persist_for', 'cluster_keys', 'distribution', 'extents_json_url', 
    # 'feature_key', 'file', 'property_key', 'property_label_key', 'else')
    # lkml.keys.EXPR_BLOCK_KEYS
    # ('expression_custom_filter', 'expression', 'html', 'sql_trigger_value', 'sql_table_name', 'sql_distinct_key', 
    # 'sql_start', 'sql_always_having', 'sql_always_where', 'sql_trigger', 'sql_foreign_key', 'sql_where', 'sql_end', 
    # 'sql_create', 'sql_latitude', 'sql_longitude', 'sql_step', 'sql_on', 'sql')
            
            # replace with expression block
            # if self.name.startswith('sql') or self.name == 'html':
            #     return splice(self.name, ': ', str(self.value), ' ;;')
        if self.name in (
                'links','filters','actions','options', 
                'form_params','sets', 'access_grants',
                'params', 'allowed_values', 'named_value_formats', 
                'datagroups', 'map_layers'):
                return str(self.value)
        #This one since it is a multi-value key, shouldn't be quoted literal
        elif self.name in ('tags'):
            return splice(self.name , ': ' , str(self.value))
        elif self.name in lkml.keys.EXPR_BLOCK_KEYS:
            return splice(self.name, ': ', str(self.value), ' ;;')
        # Not needed? does a default case
        # elif self.name == "strict_value_format":
        #     return splice(self.name, ': ', str(self.value))
        elif self.name in lkml.keys.QUOTED_LITERAL_KEYS:
            return splice(self.name, ': "', str(self.value), '"')
        # replace with quote literal
        # elif self.name in ['include', 'connection', 'description','value', "name","default","file"]:
        #     return splice(self.name, ': "', str(self.value), '"')
        # elif self.name.endswith('url') or self.name.endswith('label') or self.name.endswith('format') or self.name.endswith('persist_for'):
        #     return splice(self.name, ': "', str(self.value), '"')

        elif self.name in ('extends', 'alias'):
            return splice(self.name, ': [', str(self.value), ']')
        elif self.name.startswith('explore_source'):
            return splice(self.name, str(self.value))
        elif self.name == "includes":
            return splice('include: "',str(self.value),'"')
        elif self.name in conf.MULTIVALUE_PROPERTIES:
            return splice(self.name , ': ' , str(self.value))

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
    # __slots__ = ['schema','multiValueSpecialHandling','num','valueiterator']

    def __init__(self, schema, multiValueSpecialHandling=False):
        self.schema = schema
        self.num = 0
        self.valueiterator = iter(self.schema)
        self.multiValueSpecialHandling = multiValueSpecialHandling

    def __str__(self):

        def process_plural_named_constructs():
            singular = self.multiValueSpecialHandling[:-1]
            buildString = ""
            schemaDeepCopy = copy.copy(self.schema)
            for fset in schemaDeepCopy:
                buildString = buildString + conf.NEWLINE + singular + ': ' + fset.pop('name') + ' '
                buildString = buildString + str(Property('list_member',fset))
            return buildString

        def process_plural_unnamed_constructs():
            if not self.multiValueSpecialHandling == "filters":
                singular = conf.NEWLINE + self.multiValueSpecialHandling[:-1] + ': '
            else:
                singular = conf.NEWLINE + self.multiValueSpecialHandling + ': '
            
            return splice( singular , singular.join([str(p) for p in self.getProperties()]))

        def render(template,delim=' '):
            self.templateMap = {
                'data': stringify([str(p) for p in self.getProperties()], delim=delim, prefix=False)
            }
            return Template(getattr(conf.TEMPLATES,template)).substitute(self.templateMap)

            # splice(
            #                 '{\n    ' , 
            #                 '\n    '.join([str(p) for p in self.getProperties()]) ,
            #                 '\n    }' 
            #                 )

        if isinstance(self.schema, dict):
            return render('array', delim=conf.NEWLINEINDENT)
            # return splice(
            #                 '{\n    ' , 
            #                 '\n    '.join([str(p) for p in self.getProperties()]) ,
            #                 '\n    }' 
            #                 )
        elif isinstance(self.schema, list) and not self.multiValueSpecialHandling:
            return render('_list', delim=' ')
            # return splice(
            #                 '[\n    ' , 
            #                 '\n    '.join([str(p) for p in self.getProperties()]) ,
            #                 '\n    ]' 
            #                 )
        elif isinstance(self.schema, list) and self.multiValueSpecialHandling in ('tags','suggestions'):
            return splice(
                            '[\n    ' , 
                            '\n    '.join(['"' + str(p) + '",' for p in self.getProperties()]) ,
                            '\n    ]' 
                            )
        elif self.multiValueSpecialHandling in ('filters', 'links', 'actions', 'options', 'form_params','params'):
            return process_plural_unnamed_constructs()


        elif self.multiValueSpecialHandling in ("access_grants","datagroups","map_layers","named_value_formats","sets"):
            return process_plural_named_constructs()

        elif self.multiValueSpecialHandling == 'allowed_values':
            if isinstance(self.schema[0],dict):
                return splice('allowed_value: ','\n allowed_value: '.join([str(p) for p in self.getProperties()]))
            elif isinstance(self.schema[0],str):
                return splice(
                                'allowed_values: [\n    ' , 
                                '\n    '.join(['"' + str(p) + '",' for p in self.getProperties()]) ,
                                '\n    ]' 
                                )
        else:
            pass

    def __getitem__(self, key):
        '''
            TODO: fix ephemeral properties...
            TDOD: Add property subtyping
        '''        
        if isinstance(self.schema, dict):
            if key == 'sql':
                # return sql_prop(identifier, self.schema.get(identifier, []))
                return Property(key, self.schema.get(key, []))
            else:    
                return Property(key, self.schema.get(key, []))
        elif isinstance(self.schema, list):
            if key == 'sql':
                # return sql_prop(identifier, self.schema.get(identifier, []))
                return Property(key, self.schema.get(key, []))
            else:    
                return Property(key, self.schema.get(key, [])) 

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
                if self.multiValueSpecialHandling in ('suggestions','tags','allowed_values'):
                    yield Property('list_member_quoted',item)
                else:
                    yield Property('list_member',item)

    def __iter__(self):
        self.valueiterator = iter(self.schema)
        return self

    def __next__(self):
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

    def __delete__(self, identifier):
        if isinstance(self.schema,dict):
            self.schema.pop(identifier, None)
        elif isinstance(self.schema,list):
            self.schema.remove(identifier, None)

    def isMember(self, property):
        if isinstance(self.schema,dict):
            return property in self.schema.keys()
        elif isinstance(self.schema,list):
            return property in self.schema
        
    def props(self):
        '''
            Returns a list of the property values. Mostly used for membership checking
        '''
        if isinstance(self.schema, dict):
            return self.schema.keys()
        elif isinstance(self.schema, list):
            return self.schema

    def rawPropValue(self,key):
        '''
            if dict type schema, needs a prop name. If list type schema needs a number index
        '''
        return self.schema[key]

    def __len__(self):
        return len(self.schema)

class Field(base):
    ''' Base class for fields in LookML, only derived/child types should be instantiated '''
    def __init__(self, input):
        self.db_column = ''
        super(Field, self).__init__(input)
        self.templateMap = {

        }

    def children(self):
        if self.view:
            for dependent in self.view.search('sql',[self.__refsre__,self.__refre__]):
                yield dependent

    def change_name_and_child_references(self, newName):
        '''
            Change the name of the field and references to it in sql (does not yet perform the same for HTML / Links / Drill Fields / Sets / Actions etc)
        '''
        #TODO: complete checking all places for dependencies. 
        old = copy.copy(self.name)
        oldrefsre = copy.copy(self.__refsre__)
        oldrefre = copy.copy(self.__refre__)
        self.setName(newName)
        for f in self.view.search('sql',[oldrefsre,oldrefre]):
            f.sql = re.sub(oldrefsre, self.__refs__, str(f.sql.value))
            f.sql = re.sub(oldrefre, self.__ref__, str(f.sql.value))
        self.view.removeField(old)
        self.view + self
        return self

    # def __str__(self):
    #     self.templateMap = {
    #          'message': self.message
    #         ,'identifier':self.identifier
    #         ,'props': stringify([str(p) for p in self.getProperties()])
    #     }
    #     return Template(getattr(conf.TEMPLATES,self.token)).substitute(self.templateMap)
 

    def __getattr__(self, key):

        if key == 'name':
            return self.identifier
        elif key == 'pk':
            return self.getPrimaryKey()
        #full reference
        elif key == '__ref__':
            if self.view:
                return splice('${' , self.view.identifier , '.' , self.identifier , '}')
        #Short Reference
        elif key == '__refs__':
            return splice('${' , self.identifier , '}')

        #full reference -- regex escaped
        elif key == '__refre__':
            if self.view:
                return splice('\$\{' , self.view.identifier , '\.' , self.identifier , '\}')
        #Short reference -- regex escaped
        elif key == '__refsre__':
            if self.view:
                return splice('\$\{' , self.identifier , '\}')
        #Raw Reference
        elif key == '__refr__':
            if self.view:
                return splice(self.view.identifier , '.' , self.identifier)
        #Raw refence short
        elif key == '__refrs__':
            if self.view:
                return splice(self.identifier)
        #Raw Reference regex
        elif key == '__refrre__':
            if self.view:
                return splice(self.view.identifier , '\.' , self.identifier)
        else:
            return self.getProperty(key)

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

    def setView(self, view):
        '''
        '''
        self.view = view
        return self  # satisfies a need to linkback (look where setView is called)

    def setSql(self, sql):
        self.setProperty('sql', sql)
        return self

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
    def __init__(self, input):
        super(Dimension, self).__init__(input)
        self.token = 'dimension'
        
    def isPrimaryKey(self):
        if self.hasProp('primary_key') and self.getProperty('primary_key').value == 'yes':
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

class DimensionGroup(Field):
    def __init__(self, input):
        super(DimensionGroup, self).__init__(input)
        if not self.properties.isMember('timeframes'):
            self.properties.addProperty('timeframes', splice('[','{},'.format(conf.NEWLINEINDENT).join(conf.TIMEFRAMES),']'))
        if not self.properties.isMember('type'):
            self.properties.addProperty('type', 'time')
        if not self.properties.isMember('sql'):
            self.properties.addProperty('sql', splice('${TABLE}.' , conf.DB_FIELD_DELIMITER_START , self.db_column , conf.DB_FIELD_DELIMITER_END))
        self.token = 'dimension_group'

    def setDBColumn(self, dbColumn, changeIdentifier=True):
        ''''''
        self.db_column = dbColumn
        self.setProperty('sql', splice('${TABLE}.' , conf.DB_FIELD_DELIMITER_START , self.db_column , conf.DB_FIELD_DELIMITER_END))
        if changeIdentifier:
            self.identifier = lookCase(self.db_column)
        return self
    
class Measure(Field):
    def __init__(self, input):
        super(Measure, self).__init__(input)
        self.token = 'measure'

class Filter(Field):
    def __init__(self, input):
        super(Filter, self).__init__(input)
        self.token = 'filter'

class Parameter(Field):
    def __init__(self, input):
        super(Parameter, self).__init__(input)
        self.token = 'parameter'
    
