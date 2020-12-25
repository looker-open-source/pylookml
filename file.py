import lookml, lkml
from lang import ws
import github
import re, os, shutil, copy, base64

 

#P0: Finish defining new granular file types
'''
Factory Function:
    routes / existing instances or New()

General File:
    file (read/write)
    path management

generic lkml file (identified by .lkml)

    model file (identified by .model.lkml)
    view file
    manifest file (identified by manifest.lkml name [one and only one per project])
    

lookml dashboard (identified by extension .lookml)
    pyyaml parser

json files:
    locale (identified by .strings.json extension)

non-semantic:
    markdown file (identified by .md extension)
    js file (identified by extension .js)
    maylayer (identified by .topojson or vector tile)

'''
class baseFile(object):
    def __init__(self,path='',name=''):
        self.name = name
        self.path = path

    def setFolder(self,folder):
        self.path = folder + self.name if folder.endswith('/') else folder  + '/' +  self.name
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


class lkmlFile(baseFile):
    def __init__(self,path='',name=''):
        self.name = name
        self.path = path
        self.contents = lookml.Model(lkml.load(open(self.path,encoding="utf-8")))

    def __getattr__(self,item):
        if item in self.__dict__.keys():
            return self.__dict__[item]
        elif item in self.contents.__dict__.keys():
            return self.contents.__dict__[item]
        else:
            return object.__getattr__(item)

    def __str__(self): return str(self.contents)

class testClassgithub(baseFile):
    def __init__(self,f):
        self.name = f._rawData['name']
        self.path = f._rawData['path']
        self.sha = f._rawData['sha']
        data = base64.b64decode(f.content).decode('utf-8')
        self.contents = lookml.Model(lkml.load(data))

    def __getattr__(self,item):
        if item in self.__dict__.keys():
            return self.__dict__[item]
        elif item in self.contents.__dict__.keys():
            return self.contents.__dict__[item]
        else:
            return object.__getattr__(item)

    def __str__(self): return str(self.contents)


class mnfstFile(lkmlFile):
    def __init__(self,path='',name=''):
        self.name = name
        self.path = path
        self.contents = lookml.Manifest(lkml.load(open(self.path,encoding="utf-8")))


class baseFileOld(object): 
    '''
        A file object represents a file within a LookML project. It can be several types, can contain views, explores 
        or other properties such as inlcude or data groups
        It can be instantiated with a View, an Explore, a filepath on disk, or content from the Github API
    '''
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

        def __getitem__(self,key):
            return self.__getattr__(key)

        def add(self, v):
            if isinstance(v,dict):
                v = lookml.View(v)
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

        def __getitem__(self,key):
            return self.__getattr__(key)

        def add(self, e):
            if isinstance(e,dict):
                e = lookml.Explore(e)
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
            self.name_components = self.name.split('.')
            if len(self.name_components) <= 1:
                self.base_name = self.name
            elif len(self.name_components) == 2:
                self.base_name = self.name_components[0]
            else:
                self.base_name = '.'.join(self.name_components[:-2])
            self.path = os.path.relpath(f)
            self.sha = ''
            #Parse Step: file is provided 
            with open(self.path, 'r', encoding="utf-8") as tmp:
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
            self.name = f.name + '.model.lkml' # What about explore filetypes?
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
        elif isinstance(f, lookml.View):
            self.f_type = "view"
            viewBootstrap()
        elif isinstance(f, lookml.Explore):
            self.f_type = "explore"
            exploreBootstrap()
        elif os.path.isfile(f):
            self.f_type = "path"
            filepathBootstrap()

        #Step 2 -- set a lookml "file type" mostly only used for path info 
        if self.name.endswith('lkml'):
            self.filetype = self.name.split('.')[-2]
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

        # self.properties = Properties(self.json_data)
        # self.props = self.properties.props()

    def __getattr__(self, key):
        if key in self.__dict__.keys():
            return self.__dict__[key]
        elif key == 'views':
            return self.vws
        elif key == 'explores':
            return self.exps
        #TODO: resolve attribute access issues
        elif key in ['datagroups', 'map_layers', 'named_value_formats']:
            return self.properties[key]
        # else:
        #     # raise KeyError
        #     return object.__getattr__(key)

    def __getitem__(self,key):
        if key == 'views':
            return self.vws
        elif key == 'explores':
            return self.exps

    def __str__(self):
        # return (
        #      f'{ws.nl}'.join([ str(e) for e in self.explores] ) if self.exps else ''
        #      f'{ws.nl}'
        #      f'{ws.nl}'.join([ str(v) for v in self.views]) if self.vws else ''
        # )
        return   (f'{ws.nl}'.join([ str(e) for e in self.explores]) if self.exps else '') + (ws.nl + f'{ws.nl}'.join([ str(v) for v in self.views]) if self.vws else '')

    def setSha(self,sha):
        self.sha = sha
        return self

    def addView(self,v):
        self.vws.add(v)
        return self

    def addExplore(self,e):
        self.exps.add(e)
        return self

    def _bind_lkml(self, lkmldictraw):
        lkmldict = copy.deepcopy(lkmldictraw)
        if 'views' in lkmldict.keys():
            for view in lkmldict['views']:
                self.vws.add(lookml.View(view))
            lkmldict.pop('views')

        if 'explores' in lkmldict.keys():
            for explore in lkmldict['explores']:
                self.exps.add(lookml.Explore(explore))
            lkmldict.pop('explores')

        for k,v in lkmldict.items():
            self.setProperty(k,v) 

    def __add__(self, other):
        if isinstance(other, lookml.View):
            self.addView(other)
        elif isinstance(other, lookml.Explore):
            self.addExplore(other)
        else:
            self._bind_lkml(lkml.load(other))

    def getProperty(self, prop):
        ''' Get a property from the properties collection '''
        return self.properties[prop]

    def setProperty(self, name, value):
        ''' Set a property in the properties collection '''
        self.properties.addProperty(name, value)
        return self

    def setFolder(self,folder):
        self.path = folder + self.name if folder.endswith('/') else folder  + '/' +  self.name
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


def File(f):
    '''
        Factory Function which routes to the right class
    '''
    if isinstance(f,str):
        if f.endswith('.model.lkml'):
            return lkmlFile(f)
        if f.endswith('manifest.lkml'):
            return mnfstFile(f)
        else:
            return baseFileOld(f)

    elif isinstance(f,github.ContentFile.ContentFile):
        return testClassgithub(f)