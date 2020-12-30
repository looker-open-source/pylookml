import time
import subprocess, os, platform, shutil
import lookml
import github
import base64
import requests
import re
import file
import lkml
import pprint
import warnings
LOOKML_DASHBOARDS = False
#import marko

def mkdir_force(dir):
    if not os.path.exists(dir):
        os.mkdir(dir,0o777)

def _optional_import_(module: str, name: str = None, package: str = None):
    import importlib
    try:
        module = importlib.import_module(module)
        return module if name is None else getattr(module, name)
    except ImportError as e:
        if package is None:
            package = module
        msg = f"install the '{package}' package to make use of this feature"
        import_error = e

        def _failed_import(*args):
            raise ValueError(msg) from import_error

        return _failed_import
yaml_load = _optional_import_('yaml', 'safe_load', package='pyyaml')
yaml_dump = _optional_import_('yaml', 'dump', package='pyyaml')

def Project(
            repo='',
            access_token='',
            branch="master",
            git_url="",
            commitMessage="",
            looker_host="",
            looker_project_name="",
            outputPath='.tmp'
        ):
    '''
        A LookML Project at a GitHub location or location on the filesytem [Factory Function]
        see _Project for subclass details
    '''
    if access_token and repo:
        return githubProject(
            repo=repo,
            access_token=access_token,
            branch=branch,
            git_url=git_url,
            commitMessage=commitMessage,
            looker_host=looker_host,
            looker_project_name=looker_project_name,
            outputPath=outputPath
            )
    elif git_url:
        return shellProject(repo=repo,access_token=access_token,branch=branch,git_url=git_url,commitMessage=commitMessage,looker_host=looker_host,looker_project_name=looker_project_name,outputPath=outputPath)

class project:
    '''
        A LookML Project at a GitHub location or location on the filesytem
    '''
    def __init__(
            self,
            repo='',
            access_token='',
            branch="master",
            git_url="",
            commitMessage="",
            looker_host="",
            looker_project_name="",
            outputPath='.tmp'
        ):
        ''' 
            Can be constructed with a github access token and repository name
        '''
        self.outputPath = outputPath
        self.branch = branch
        self.looker_project_name = looker_project_name
        self.commitMessage = "PyLookML Auto Updated: " + time.strftime('%h %d %Y @ %I:%M%p %Z') if not commitMessage else commitMessage
        self.index = dict()
        #host setup
        self.looker_host = looker_host
        if self.looker_host and not looker_host.startswith('https://'):
            self.looker_host = 'https://' + looker_host 
            if not self.looker_host.endswith('/'):
                self.looker_host = self.looker_host + '/'
        self.deploy_url = ""
        self.constructDeployUrl()

    def buildIndex(self):
        for f in self.files():
            for view in f['views']:
                for prop in view:
                    pass
                for field in view.fields():
                    for prop in field:
                        if prop.name in ('sql','html'):
                            # print(prop.name,': ', prop.value)
                            for ref in lookml.parseReferences(prop.value):
                                if ref is not None:
                                    key = ref['field'] if ref['fully_qualified_reference'] else view.name + '.' + ref['field']
                                    location = view.name + '.' + field.name + '.' + prop.name
                                    data = {'type':prop.name, 'file':f.path}
                                    if key not in self.index.keys():
                                        self.index[key] = { location: data }
                                    else:
                                        self.index[key].update({
                                           location : data
                                        })
        print(self.index)

    def __getitem__(self, key):
        return self.file(key)

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
        '''
        Iteratively returns all the lkml files at a path in the project

        :param path: directory you would like to return the files from
        :type arg1: str
        :return: generator of LookML file objects
        :rtype: generator of lookml File objects
        '''
        for f in  self.repo.get_contents(path):
            if f.type != 'dir':
                yield file.File(f)

    def file(self,path):
        '''
        returns a single LookML file at the specified path.
        examples: 
        file('order_items.view.lkml')
        file('my_folder/users.view.lkml')

        :param path: path file location
        :type arg1: str
        :return: a single lookml File
        :rtype: File
        '''
        return file.File(self.repo.get_contents(path))

    def update(self,f):
        '''
        updates an existing file to git

        :param f: the file to update
        :type f: File
        :return: self (for method chaining)
        :rtype: self
        '''
        self.repo.update_file(f.path, self.commitMessage, str(f), sha=f.sha, branch=self.branch)
        return self

    def add(self,f):
        '''
        adds a new file to git

        :param f: the file to add
        :type f: File
        :return: self (for method chaining)
        :rtype: self
        '''
        self.repo.create_file(f.path, self.commitMessage, str(f), branch=self.branch)
        return self

    def put(self,f):
        '''
        adds or updates file to git. Safe to use either use case

        :param f: the file to add/update
        :type f: File
        :return: self (for method chaining)
        :rtype: self
        '''
        if self.exists(f):
            if f.sha:
                self.update(f)
            else:
                f2 = self.file(f.path)
                f.setSha(f2.sha)
                self.update(f)
        else:
            self.add(f)
        return self
    def delete(self,f):
        '''
        deletes a file from a repository at a specific path

        :param f: the file or path
        :type f: File or str path
        :return: self
        :rtype: self
        '''
        if isinstance(f,str):
            f = self.getFile(f)
        self.repo.delete_file(f.path, self.commitMessage, sha=f.sha, branch=self.branch)
        return self
class shellProject(project):
    '''
        Project subtype that interfaces with git via its command line interface. SSH git access must be working on the machine
        files will be cloned into a subfolder of .tmp by default
    '''
    class gitController:
        def __init__(
                     self  
                    ,outputPath=''
                    ,projectName=''
                    ,branch='master'
                    ,deployMessage=''
                    ,exePath=''
                    ,includeGitDir=False
                ):
            self.platform = platform.system()
            self.preamble = []
            self.trailers = []
            if self.platform == 'Windows':
                self.exe = exePath + ' '
                self.preamble.append(self.exe)
                self.trailers.append(' & exit')
            else:
                self.exe = ''
            self.projectName = projectName

            mkdir_force(outputPath)

            self.outputPath = outputPath + '/' + self.projectName
            self.absoluteOutputPath = os.path.abspath(self.outputPath)
            self.branch = branch
            self.deployMessage = deployMessage
            
            if os.path.exists(self.absoluteOutputPath):
                shutil.rmtree(self.absoluteOutputPath)

            mkdir_force(self.absoluteOutputPath)

            if self.projectName:
                self.gitDir = ' --git-dir="' + os.path.abspath(outputPath + '/' + self.projectName + '/.git') + '" '
            else:
                self.gitDir = ' --git-dir="' + os.path.abspath(outputPath + '/.git') + '" '
                
            self.includeGitDir = includeGitDir
            
            if self.includeGitDir:
                self.preamble.append(self.includeGitDir)
                
        def call(self, command, gitDir=True):
            if gitDir:
                tmp = ' '.join(self.preamble) + 'git ' + self.gitDir + ' ' + command + ' '.join(self.trailers)
            else:
                tmp = ' '.join(self.preamble) + 'git ' + command + ' '.join(self.trailers)
            print(tmp)
            proc = subprocess.Popen(
                            tmp 
                            ,shell=True
                            ,env=os.environ
                            ,cwd=self.absoluteOutputPath
                            )
            try:
                outs, errs = proc.communicate(timeout=15) 
            except subprocess.TimeoutExpired:
                proc.kill()
                outs, errs = proc.communicate()
            return self

        def pull(self):
            return self.call(' pull origin ' + self.branch + ' ')
            
        def clone(self, repoLocation):
            self.call(' clone ' + repoLocation + ' ' +  self.absoluteOutputPath, gitDir=False)
            return self.pull()
            
        def add(self,path='.'):
            return self.call(' add ' + path)
            
        def commit(self, message=''):
            if message:
                return self.call(' commit -m "' + message + ' ' + self.deployMessage + '"')
            else:
                return self.call(' commit -m "' + self.deployMessage + '"')
            
        def pushRemote(self):
            return self.call(' push origin ' + self.branch + ' ')

    def __init__(self,*args, **kwargs):
        super(shellProject, self).__init__(*args,**kwargs)
        self.type = "ssh_shell"
        
        self.gitControllerSession =  self.gitController(
                projectName=self.looker_project_name, 
                branch=self.branch, 
                deployMessage=self.commitMessage, 
                outputPath=self.outputPath
                )    
        self.path =  os.getcwd() + '/' + self.outputPath + '/' + self.looker_project_name + '/'
        assert(kwargs['git_url'] is not None)
        self.gitControllerSession.clone(kwargs['git_url'])

    def files(self,path=''):
        '''
        Iteratively returns all the lkml files at a path in the project

        :param path: directory you would like to return the files from
        :type arg1: str
        :return: generator of LookML file objects
        :rtype: generator of lookml File objects
        '''
        for root, dirs, files in os.walk(self.gitControllerSession.absoluteOutputPath + '/' + path, topdown=False):
            for name in files:
                if name.endswith('.lkml'):
                    yield file.File(os.path.join(root, name))

    def file(self,path):
        '''
        returns a single LookML file at the specified path.
        examples: 
        file('order_items.view.lkml')
        file('my_folder/users.view.lkml')

        :param path: path file location
        :type arg1: str
        :return: a single lookml File
        :rtype: File
        '''
        return file.File(self.gitControllerSession.absoluteOutputPath + '/' + path)

    def update(self,f):
        '''
        updates an existing file to git

        :param f: the file to update
        :type f: File
        :return: self (for method chaining)
        :rtype: self
        '''
        f.write()
        self.gitControllerSession.add().commit().pushRemote()
        return self

    def add(self,f):
        '''
        adds a new file to git

        :param f: the file to add
        :type f: File
        :return: self (for method chaining)
        :rtype: self
        '''
        f.setFolder(self.gitControllerSession.absoluteOutputPath)
        f.write()
        self.gitControllerSession.add().commit().pushRemote()
        return self

    def put(self,f):
        '''
        adds or updates file to git. Safe to use either use case

        :param f: the file to add/update
        :type f: File
        :return: self (for method chaining)
        :rtype: self
        '''
        if os.path.exists(f.path):
            self.update(f)
        else:
            self.add(f)
        
    def exists(self,f):
        '''
        returns a boolean if the file or file path exists

        :param f: the file or path
        :type f: File or str path
        :return: None
        :rtype: None
        '''
        if isinstance(f,file.File):
            return os.path.exists(f.path)
        elif isinstance(f,str):
            #Check a naked path first, then fall back on the user having provided the full project path
            if os.path.exists( self.path  + f):
                return os.path.exists( self.path  + f)
            else:
                return os.path.exists(f)

    def delete(self,f):
        '''
        deletes a file from a repository at a specific path

        :param f: the file or path
        :type f: File or str path
        :return: self
        :rtype: self
        '''
        if isinstance(f,str):
            os.remove(f)
        elif isinstance(f,file.File):
            os.remove(f.path)
        else:
            raise Exception('Not a File Insance or path')
        self.gitControllerSession.add().commit().pushRemote()
        return self
class githubProject(project):
    def __init__(self, *args, **kwargs):
        super(githubProject, self).__init__(*args,**kwargs)
        self.type = "github"
        self.gitsession = github.Github(kwargs['access_token'])
        self.repo = self.gitsession.get_repo(kwargs['repo'])

    def exists(self,f):
        '''
        returns a boolean if the file or file path exists

        :param f: the file or path
        :type f: File or str path
        :return: None
        :rtype: None
        '''
        def checkgithub(f0):
            try:
                self.repo.get_contents(f0)
                return True
            except github.GithubException as e:
                if e._GithubException__status == 404:
                    return False
        #P0: types are not aligned to the new types
        # if isinstance(f,file.File):
        # if isinstance(f,file.testClassgithub):
        return checkgithub(f.path)
        # elif isinstance(f,str):
        #     return checkgithub(f)


class f(object):
    def __init__(
         self
        ,path
        ,parent=None
    ):
        self.parent = parent

        self.path = path
        #lookml_path synonym for code clarity
        self.lookml_path = self.path
        #update the name to the last element of the split
        self.name = self.path.split('/')[-1]
        
        #get parent folder
        path_parts = path.split('/')
        if len(path_parts) > 1:
            folder = '/'.join(path_parts[:-1])
        else:
            folder = '.'

        #establish python path / pyshical path for write operations
        #vs lookml_path for includes operations
        if not path.startswith(self.parent._path):
            folder = self.parent._path + '/' + folder
            self.python_path = self.parent._path + '/' + path
        else:
            self.python_path = self.path

        self.lookml_folder = os.path.relpath(folder,self.parent._path)

        #update index
        if self.lookml_folder not in self.parent._index.keys():
            self.parent.check_folder_create(folder)
            self.parent._index[self.lookml_folder] = dict()
        self.parent._index[self.lookml_folder].update(
            {
                self.name: self
            })

        #P1 finish json, md and JS handlers
        self.extension = self.name.split('.')[-1]
        self.named_extension = self.name.split('.')[-2] + '.' + self.name.split('.')[-1]
        if self.extension == 'lkml':
            typ = self.name.split('.')[-2]
            if typ in ('model','manifest'):
                self.type = typ
            #views or naked are "partial models"
            else:
                self.type = 'partial_model'
        elif self.extension == 'json':
            self.type = 'json'
        elif self.extension == 'md':
            self.type = 'markdown'
        elif self.extension == 'lookml':
            typ = self.name.split('.')[-2]
            self.type = 'lookml_dashboard'

        # if os.path.exists(self.path):
        if os.path.exists(self.python_path):
            self.read()
        elif self.type in ('model','partial_model'):
            self.content = lookml.Model('',parent=self)
        elif self.type in ('manifest'):
            self.content = lookml.Manifest('',parent=self)
        elif self.type == 'lookml_dashboard':
            self.read()
        else:
            #P0 create other type initialization
            raise Exception('not implemented yet')

        #bound during the includes parsing of other stuff
        self.object_parent = None

        #
        self.includes = None

        #track if anything has changed in self.content
        self.has_changes = None

    def __getattr__(self,item):
        if item in self.__dict__.keys():
            return self.__dict__[item]
        elif item in self.content.__dict__.keys():
            return self.content.__dict__[item]
        else:
            return object.__getattr__(item)

    def __getitem__(self,item):
        if item in self.content.__dict__.keys():
            return self.content.__dict__[item]
        # elif item in self.__dict__.keys():
        #     return self.__dict__[item]

    def __add__(self,other):
        self.content + other
    def __sub__(self,other):
        self.content - other
    # def __setattr__(self, attr):
    #     super().__setattr__(attr)

    def read(self):
        if self.type in ('model','partial_model'):
            self.content = lookml.Model(lkml.load(open(self.python_path,encoding="utf-8")),parent=self)
        elif self.type == 'manifest':
            self.content = lookml.Manifest(lkml.load(open(self.python_path,encoding="utf-8")),parent=self)
        elif self.type == 'lookml_dashboard':
            # self.content = yaml.load(open(self.path,encoding="utf-8"))
            self.content = yaml_load(open(self.python_path,encoding="utf-8"))

    def write(self,overWriteExisting=True):
        ''' Checks to see if the file exists before writing'''
        # print("Writing to: %s" % (self.path) )
        if overWriteExisting:
            with open(self.python_path, 'w') as opened_file:
                try:
                    if self.type == 'lookml_dashboard':
                        warnings.warn('''LookML dashboards are currently read only, 
                        to be fixed in a future release''')
                        #P1 fix writing, currently lookml dashboards should be considered read only
                        # opened_file.write(yaml_dump(self.content))
                    else:
                        opened_file.write(self.__str__())
                except:
                    pass
        else:
            try:
                fh = open(self.python_path, 'r')
                fh.close()
            except FileNotFoundError:
                with open(self.python_path, 'w') as opened_file:
                    opened_file.write(self.__str__())

    def change_name(self):
        pass

    def move(self):
        pass

    def __str__(self): return str(self.content)

class _project(object):
    class gitController:
        def __init__(
                     self  
                    ,outputPath=''
                    ,projectName=''
                    ,branch='master'
                    ,deployMessage=''
                    ,exePath=''
                    ,includeGitDir=False
                ):
            self.platform = platform.system()
            self.preamble = []
            self.trailers = []
            if self.platform == 'Windows':
                self.exe = exePath + ' '
                self.preamble.append(self.exe)
                self.trailers.append(' & exit')
            else:
                self.exe = ''
            self.projectName = projectName

            #mkdir_force(outputPath)
            os.makedirs(outputPath,exist_ok=True)
            # os.mkdirs(outputPath,exist_ok=True)
            

            # self.outputPath = outputPath + '/' + self.projectName
            self.outputPath = outputPath
            self.absoluteOutputPath = os.path.abspath(self.outputPath)
            self.branch = branch
            self.deployMessage = deployMessage
            
            if os.path.exists(self.absoluteOutputPath):
                shutil.rmtree(self.absoluteOutputPath)

            # mkdir_force(self.absoluteOutputPath)
            os.makedirs(self.absoluteOutputPath,exist_ok=True)
            


            if self.projectName:
                self.gitDir = ' --git-dir="' + os.path.abspath(outputPath + '/' + self.projectName + '/.git') + '" '
            else:
                self.gitDir = ' --git-dir="' + os.path.abspath(outputPath + '/.git') + '" '
                
            self.includeGitDir = includeGitDir
            
            if self.includeGitDir:
                self.preamble.append(self.includeGitDir)
                
        def call(self, command, gitDir=True):
            if gitDir:
                tmp = ' '.join(self.preamble) + 'git ' + self.gitDir + ' ' + command + ' '.join(self.trailers)
            else:
                tmp = ' '.join(self.preamble) + 'git ' + command + ' '.join(self.trailers)
            print(tmp)
            proc = subprocess.Popen(
                            tmp 
                            ,shell=True
                            ,env=os.environ
                            ,cwd=self.absoluteOutputPath
                            )
            try:
                outs, errs = proc.communicate(timeout=15) 
            except subprocess.TimeoutExpired:
                proc.kill()
                outs, errs = proc.communicate()
            return self

        def pull(self):
            return self.call(' pull origin ' + self.branch + ' ')
            
        def clone(self, repoLocation):
            self.call(' clone ' + repoLocation + ' ' +  self.absoluteOutputPath, gitDir=False)
            return self.pull()
            
        def add(self,path='.'):
            return self.call(' add ' + path, gitDir=False)
            
        def commit(self, message=''):
            if message:
                return self.call(' commit -m "' + message + ' ' + self.deployMessage + '"', gitDir=False)
            else:
                return self.call(' commit -m "' + self.deployMessage + '"', gitDir=False)
            
        def pushRemote(self):
            return self.call(' push origin ' + self.branch + ' ', gitDir=False)

    def __init__(
         self
        ,local: bool=False
        ,path: str='.tmp'
        ,_looker_host: str=None
        ,_looker_project_name: str=None
        ,_git_url: str=''
        ,_branch: str='master'
        ,commit_message: str=''
        ):
        self._local = local
        self._path = path
        self.connection = None
        self._index = dict()
        self._looker_host = _looker_host
        self._looker_project_name = _looker_project_name
        self._git_url = _git_url
        self._branch = _branch
        self.commit_message = "PyLookML Auto Updated: " +\
             time.strftime('%h %d %Y @ %I:%M%p %Z') if not commit_message else commit_message
        if self._git_url:
            self._path = self._path + '/' + self._looker_project_name
            self._git = self.gitController(
                 outputPath=self._path
                ,projectName= self._looker_project_name
                ,branch=self._branch
                ,deployMessage=self.commit_message
            )
            self._git.clone(self._git_url)

        for root, dirs, files in os.walk(self._path, topdown=False):
            for name in files:
                if name.endswith('.lkml') or (name.endswith('.lookml') and LOOKML_DASHBOARDS):
                    folder = os.path.relpath(root,self._path)
                    if folder not in self._index.keys():
                        self._index[folder] = dict()
                    
                    self._index[folder].update(
                        {
                            name: f(
                                     os.path.join(
                                         folder, 
                                         name
                                         )
                                    ,parent=self
                                    )
                        }
                        )
    def commit(self):
        self._git.commit()

    def __getitem__(self, f):
        if len(f.split('/')) == 1:
            name = f
            folder = '.'
        else:
            name = f.split('/')[-1]
            folder = '/'.join(f.split('/')[:-1])
        if folder in self._index.keys():
            if name in self._index[folder].keys():
                return self._index[folder][name]
            else:
                raise Exception(f'{name} not found in {folder}')
        else:
            raise Exception(f'{folder} not found')

    def __iter__(self):
        self._valueiterator = iter(list(self.traverse(self._index)))
        return self

    def __next__(self):
        try:
            return next(self._valueiterator)
        except:
            raise StopIteration

    def traverse(self, tree):
        for k,v in tree.items():
            if isinstance(v,dict):
                for k1,v1 in v.items():
                    if isinstance(v1,dict):
                        self.traverse(v1)
                    else:
                        yield v1
            else:
                yield v
                
    def file(self,path:str):
        return self[path]
    
    def files(self):
        for f in self:
            yield f

    def view_files(self):
        for f in self:
            if f.named_extension == 'view.lkml':
                yield f

    def model_files(self):
        for f in self:
            if f.named_extension == 'model.lkml':
                yield f
    
    def manifest_files(self):
        for f in self:
            if f.named_extension == 'manifest.lkml':
                yield f
    
    def check_folder_create(self,dir: str=''):
        os.makedirs(dir,exist_ok=True)

    def new_file(self,path:str='') -> f:
        return f(path,parent=self)

    def dir_list(self):
        def traverse(tree,i=0):
            for k,v in tree.items():
                if type(v) == dict:
                    print('   folder: ',k)
                    traverse(v,i=i)
                else:
                    print(' '*6,v.name)
                    if v.type in ('partial_model','model'):
                        for vo in v.views:
                            print(' '*9,'view: ',vo.name)
                        for e in v.explores:
                            print(' '*9,'explore: ',e.name)
        print('project: ', self._path)
        traverse(self._index)

    def path_exists(self,path):
        return os.path.exists(path)

    def constructDeployUrl(self):
        '''
            Constructs a github deploy URL according to this pattern:
            https://prod.host.com/webhooks/projects/projectname/deploy
        '''
        #P0: the base url should not have had a trailing slash
        if self._looker_project_name and self._looker_host:
            self._deploy_url = \
                self._looker_host + 'webhooks/projects/' + self._looker_project_name + '/deploy'

    def deploy(self):
        #P3: check to see if project is on master, 
        # if not issue warning that changes won't show up
        if self._deploy_url:
            requests.get(self._deploy_url)

    def delete(self,fl):
        #P0: update the project index
        if isinstance(fl,str):
            os.remove(fl)
        elif isinstance(fl,f):
            os.remove(fl.python_path)
