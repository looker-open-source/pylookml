
from lookml import core as lookml
from lookml import lkml
import time, subprocess, os
import github
import base64
import requests
import re, shutil
import warnings
import collections
from typing import NewType, Any, Generator, Union, Tuple, Type
# import platform
# import pprint

#P1 simplify code with pathlib
# import pathlib

LOOKML_DASHBOARDS = False
#import marko

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

class File(object):
    def __init__(self, path: str,):
        self.path = path

        self.lookml_path = self.path

        self.name = self.path.split('/')[-1]

        self._paths_build()

        self._type_determination()

        self.read()

    def _type_determination(self):
        # P1 finish json, md and JS handlers
        self.extension = self.name.split('.')[-1]
        self.named_extension =\
            self.name.split('.')[-2] + '.' + self.name.split('.')[-1]
        if self.extension == 'lkml':
            typ = self.name.split('.')[-2]
            if typ in ('model', 'manifest'):
                self.type = typ
            # views or naked are "partial models"
            else:
                self.type = 'partial_model'
        elif self.extension == 'json':
            self.type = 'json'
        elif self.extension == 'md':
            self.type = 'markdown'
        elif self.extension == 'lookml':
            typ = self.name.split('.')[-2]
            self.type = 'lookml_dashboard'

    def _paths_build(self, creates_folder: bool=True):
        self.python_path = self.path


    def __getattr__(self, item):
        if item in self.__dict__.keys():
            return self.__dict__[item]
        elif item in self.content.__dict__.keys():
            return self.content.__dict__[item]
        else:
            raise Exception(f'{item} not in file type {self.type}')

    def __getitem__(self, item):
        if item in self.content.__dict__.keys():
            return self.content.__dict__[item]

    def __contains__(self, item):
        return item in self.content

    def __add__(self, other):
        self.content + other

    def __sub__(self, other):
        self.content - other

    def read(self):
        if os.path.exists(self.python_path):
            if self.type in ('model', 'partial_model'):
                self.content = lookml.Model(
                    lkml.load(open(self.python_path, encoding="utf-8")), parent=self)
            elif self.type == 'manifest':
                self.content = lookml.Manifest(
                    lkml.load(open(self.python_path, encoding="utf-8")), parent=self)
            elif self.type == 'lookml_dashboard':
                self.content = yaml_load(open(self.python_path,encoding="utf-8"))
                self.content = yaml_load(
                    open(self.python_path, encoding="utf-8"))
        # blank openers for new file
        elif self.type in ('model', 'partial_model'):
            self.content = lookml.Model('', parent=self)
        elif self.type in ('manifest'):
            self.content = lookml.Manifest('', parent=self)
        elif self.type == 'lookml_dashboard':
            self.content = yaml_load(open(self.python_path, encoding="utf-8"))
        else:
            # P1 create other type initialization
            raise Exception('not implemented yet')

    def write(self, overWriteExisting=True):
        """
        Write the file (will write to filesystem or github). It does not write to the remote until 
        .commit() in SSH mode

        Args:
            overWriteExisting (bool, optional): [description]. Defaults to True.
        """
        # print("Writing to: %s" % (self.path) )
        if overWriteExisting:
            with open(self.python_path, 'w') as opened_file:
                try:
                    if self.type == 'lookml_dashboard':
                        warnings.warn('''LookML dashboards are currently read only, 
                        to be fixed in a future release''')
                        # P1 fix writing, currently lookml dashboards should be considered read only
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
        """
        Not implemented yet
        """
        #P1: not implemented
        pass

    def move(self):
        """
        Not implemented yet
        """
        #P1: not implemented
        pass

    def delete(self):
        """
        deletes the file from the filesystem
        """
        os.remove(self.python_path)

    def __str__(self): return str(self.content)

class f(File):
    def __init__(
         self 
        ,path: str 
        ,parent=None 
        ,new: bool = True
    ):
        self.parent = parent
        self.path = path
        # lookml_path synonym for code clarity
        self.lookml_path = self.path
        # update the name to the last element of the split
        self.name = self.path.split('/')[-1]

        self._paths_build()
        if new:
            if self.lookml_folder not in self.parent._index.keys():
                self.parent._index[self.lookml_folder] = dict()
            else:
                self.parent._index[self.lookml_folder].update(
                    {
                        self.name: self
                    })
        self._type_determination()

        self.read()

    def _paths_build(self, creates_folder: bool=True):
        # get parent folder
        path_parts = self.path.split('/')
        if len(path_parts) > 1:
            folder = '/'.join(path_parts[:-1])
        else:
            folder = '.'

        # establish python path / pyshical path for write operations
        # vs lookml_path for includes operations
        if not self.path.startswith(self.parent._path):
            folder = self.parent._path + '/' + folder
            self.python_path = self.parent._path + '/' + self.path
        else:
            self.python_path = self.path

        self.lookml_folder = os.path.relpath(folder, self.parent._path)

        # update index
        if self.lookml_folder not in self.parent._index.keys():
            if creates_folder:
                self.parent.check_folder_create(folder)
            self.parent._index[self.lookml_folder] = dict()

    def delete(self):
        # de-ref from index
        del self.parent._index[self.lookml_folder][self.name]
        # perform deletion on filesystem / github
        os.remove(self.python_path)

class f_github(f):
    def __init__(self, githubFile, parent=None, new=False):
        self._github_file = githubFile
        self.parent = parent
        self.path = self._github_file.path
        # lookml_path synonym for code clarity
        self.lookml_path = self.path
        # update the name to the last element of the split
        self.name = self.path.split('/')[-1]

        self._paths_build(creates_folder=False)
        if new:
            if self.lookml_folder not in self.parent._index.keys():
                self.parent._index[self.lookml_folder] = dict()
            else:
                self.parent._index[self.lookml_folder].update(
                    {
                        self.name: self
                    })
        self._type_determination()

        self.read()

    def read(self):
        if isinstance(self._github_file, github.ContentFile.ContentFile):
            if self.type in ('model', 'partial_model'):
                self.content = lookml.Model(lkml.load(base64.b64decode(self._github_file.content).decode('utf-8')), parent=self)
            elif self.type == 'manifest':
                self.content = lookml.Manifest(lkml.load(base64.b64decode(
                    self._github_file.content).decode('utf-8')), parent=self)
            elif self.type == 'lookml_dashboard':
                self.content = yaml_load(base64.b64decode(
                    self._github_file.content).decode('utf-8'))
        # elif isinstance(self._github_file.path, str):
        else:
            if self.type in ('model', 'partial_model'):
                self.content = lookml.Model('', parent=self)
            elif self.type == 'manifest':
                self.content = lookml.Manifest('', parent=self)
            elif self.type == 'lookml_dashboard':
                self.content = yaml_load('')

    def write(self):
        """
        write the file to github

        Raises:
            Exception: if file not in github
        """
        if isinstance(self._github_file.path, str):
            if not self.exists():
                self._github_file = self.parent._git_connection.create_file(
                    self.path,
                    self.parent._commit_message,
                    str(self.content),
                    branch=self.parent._branch
                )
                self._github_file = self._github_file['content']
            else:
                tmp = self.parent._git_connection.get_contents(self.path,ref=self.parent._branch)
                self._github_file = self.parent._git_connection.update_file(
                    self.path,
                    self.parent._commit_message,
                    str(self.content),
                    sha=tmp.sha,
                    branch=self.parent._branch
                )['content']

        elif isinstance(self._github_file, github.ContentFile.ContentFile):
            if self.exists():
                self.parent._git_connection.update_file(
                    self.path,
                    self.parent._commit_message,
                    str(self),
                    sha=self._github_file.sha,
                    branch=self.parent._branch)
        else:
            raise Exception('file was not bound to github or sting path')

    def delete(self):
        """
        Deletes the file from github
        """
        # de-ref from index
        del self.parent._index[self.lookml_folder][self.name]
        # perform deletion on filesystem / github
        tmp = self.parent._git_connection.get_contents(self.path,ref=self.parent._branch)
        self.parent._git_connection.delete_file(
            self.path, self.parent._commit_message, tmp.sha, self.parent._branch
        )

    def exists(self):
        def checkgithub(f0):
            try:
                self.parent._git_connection.get_contents(f0,ref=self.parent._branch)
                return True
            except github.GithubException as e:
                if e._GithubException__status == 404:
                    return False
        return checkgithub(self.path)

class Project(object):
    def __new__(cls, *args, **kwargs):
        # factory sytle routing within class
        if ('repo' in kwargs.keys()) and ('access_token' in kwargs.keys()):
            return super(Project, cls).__new__(ProjectGithub)
        elif ('git_url' in kwargs.keys()):
            return super(Project, cls).__new__(ProjectSSH)
        elif ('path' in kwargs.keys()):
            return super(Project, cls).__new__(cls)

    def __init__(
        self, path: str = '.tmp', 
        git_url: str = '', 
        branch: str = 'master', 
        commitMessage: str = ''
    ):
        self._path = path
        self._index = dict()
        self._build_index()

    def _build_index(self):
        for root, dirs, files in os.walk(self._path, topdown=False):
            for name in files:
                if name.endswith('.lkml') or (name.endswith('.lookml') and LOOKML_DASHBOARDS):
                    folder = os.path.relpath(root, self._path)
                    if folder not in self._index.keys():
                        self._index[folder] = dict()

                    self._index[folder].update(
                        {
                            name: f(
                                os.path.join(
                                    folder,
                                    name
                                ), parent=self, new=False
                            )
                        }
                    )
    @staticmethod
    def _folder_split(f:str):
        Folder = collections.namedtuple('folder',['folder','name','path'])
        if len(f.split('/')) == 1:
            me = Folder(folder='.',name=f,path=f)
        else:
            me = Folder(
                     folder='/'.join(f.split('/')[:-1])
                    ,name=f.split('/')[-1]
                    ,path=f
                    )
        return me

    def __getitem__(self, f):
        f = self._folder_split(f)
        if f.folder in self._index.keys():
            if f.name in self._index[f.folder].keys():
                return self._index[f.folder][f.name]
            else:
                raise Exception(f'{f.name} not found in {f.folder}')
        else:
            raise Exception(f'{f.folder} not found')
    # base

    def __iter__(self):
        self._valueiterator = iter(list(self.traverse(self._index)))
        return self
    # base

    def __next__(self):
        try:
            return next(self._valueiterator)
        except:
            raise StopIteration
    # base

    def traverse(self, tree):
        for k, v in tree.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    if isinstance(v1, dict):
                        self.traverse(v1)
                    else:
                        yield v1
            else:
                yield v
    # base

    def put(self, file: File):
        """
        writes a file to your project. synonym of myFile.write()

        Args:
            file (File): the file object to be written

.. code-block:: python

        myFile = lookml.File('foo.view.lkml')
        proj.put(myFile)

        """
        file.write()

    def delete(self, file: File):
        """
        Delete a file from the project

        Args:
            file (File): pass the file object to delete

.. code-block:: python

        myFile = proj.new_file('foo.view.lkml')
        proj.delete(myFile)
        """
        file.delete()

    def file(self, path: str) -> f:
        """
        Return a file for the lookml project file path

        Args:
            path (str): string to the path of the file i.e 'views/order_items.view.lkml'

        Returns:
            file: the pylookml file type
        """
        return self[path]

    def files(self) -> Generator:
        """
        Iterate over the project files

        Yields:
            Generator: file objects
        """
        for f in self:
            yield f

    def view_files(self):
        """
        Iterate over the project view files

        Yields:
            Generator: file objects
        """
        for f in self:
            if f.named_extension == 'view.lkml':
                yield f

    def model_files(self):
        """
        Iterate over the project model files

        Yields:
            Generator: file objects
        """
        for f in self:
            if f.named_extension == 'model.lkml':
                yield f

    def manifest_files(self):
        """
        Iterate over the project manifest files
        (there should only be one per project)

        Yields:
            Generator: file objects
        """
        for f in self:
            if f.named_extension == 'manifest.lkml':
                yield f

    def check_folder_create(self, dir: str = ''):
        os.makedirs(dir, exist_ok=True)

    def new_file(self, path: str = '') -> f:
        """
        Create a new file of any type: view, model etc

        Args:
            path (str, optional): lookml project path you'd like the file created at

        Returns:
            f: returns the new file object

.. code-block:: python

        myFile = proj.new_file('foo.view.lkml')
        myFile + 'view: foo {}'

        """
        return f(path, parent=self)

    def dir_list(self):
        def traverse(tree, i=0):
            for k, v in tree.items():
                if type(v) == dict:
                    print('   folder: ', k)
                    traverse(v, i=i)
                else:
                    print(' '*6, v.name)
                    if v.type in ('partial_model', 'model'):
                        for vo in v.views:
                            print(' '*9, 'view: ', vo.name)
                        for e in v.explores:
                            print(' '*9, 'explore: ', e.name)
        print('project: ', self._path)
        traverse(self._index)
    # filesystem

    def path_exists(self, path):
        return os.path.exists(path)
    # base
    # filesystem

    def delete_file(self, path:str):
        """
        Delete a file by providing the path (vs delete() which takes a file obj)

        Args:
            fl (str): the path within the project of the file to be deleted

.. code-block:: python

        myFile = proj.new_file('foo.view.lkml')
        proj.delete_file(path='foo.view.lkml')

        """
        self[fl].delete()

#P1: build the ability to delete folders from filesystem & github
class ProjectGithub(Project):
    def __init__(
         self
        ,repo: str = ''
        ,access_token: str = ''
        ,commitMessage: str = ''
        ,branch: str = 'master'
        ,index_whole: bool = False
        ,looker_host: str = ''
        ,looker_project_name: str = ''
        ):
        self._repo = repo
        self._path = self._repo
        self._access_token = access_token
        self._branch = branch
        self._commit_message = "PyLookML Auto Updated: " +\
            time.strftime(
                '%h %d %Y @ %I:%M%p %Z') if not commitMessage else commitMessage
        self.gitsession = github.Github(self._access_token)
        self._git_connection = self.gitsession.get_repo(self._repo)
        self._looker_host = looker_host
        self._looker_project_name = looker_project_name
        self.constructDeployUrl()
        self._index = dict()
        self._index_whole = index_whole
        self._built = False
        if self._index_whole:
            self._build_index()

    def _build_index(self):
        contents = self._git_connection.get_contents('',ref=self._branch)
        while contents:
            file_content = contents.pop(0)
            folder = '/'.join(file_content.path.split('/')[:-1])
            if not folder:
                folder = '.'
            if file_content.type == "dir":
                contents.extend(
                    self._git_connection.get_contents(file_content.path,ref=self._branch))
            else:
                if file_content.name.endswith('.lkml') or \
                        (file_content.name.endswith('.lookml') and LOOKML_DASHBOARDS):
                    if folder not in self._index.keys():
                        self._index[folder] = dict()
                    if file_content.name not in self._index[folder].keys():
                        # self._index[folder][file_content.name] = file_content
                        self._index[folder][file_content.name] = f_github(
                            file_content, parent=self, new=False)
        self._built = True

    def __getitem__(self, f):
        f = self._folder_split(f)
        if f.folder in self._index.keys():
            if f.name in self._index[f.folder].keys():
                return self._index[f.folder][f.name]
            else:
                if not self._built:
                    return f_github(
                        self._git_connection.get_contents(f.path,ref=self._branch), 
                        parent=self, 
                        new=True
                        )
                else:
                    raise Exception(f'{f.name} not found in {f.folder}')
        else:
            if not self._built:
                return f_github(
                    self._git_connection.get_contents(f.path,ref=self._branch), 
                    parent=self, 
                    new=True
                    )
            else:
                raise Exception(f'{f.folder} not found')

    def _exists(self,p:str):
        try:
            self._git_connection.get_contents(p, ref=self._branch)
            return True
        except github.GithubException as e:
            if e._GithubException__status == 404:
                return False

    def new_file(self, path: str = '') -> f:
        path = self._folder_split(path)
        if not self._exists(path.path):
            if path.folder not in self._index.keys():
                self._index[path.folder] = dict()
            if path.name not in self._index[path.folder].keys():
                # self._index[path.folder][path.name] = f_github(path, parent=self, new=True)
                self._index[path.folder][path.name] = f_github(path, parent=self, new=False)
        else:
            raise Exception(f'File {path} already exists,'
                            f' call proj.file("{path}") to modify it'
                            f' or call proj.delete("{path}") to delete it'
                                )
        return self._index[path.folder][path.name]
    def constructDeployUrl(self):
        '''
            Constructs a github deploy URL according to this pattern:
            https://prod.host.com/webhooks/projects/projectname/deploy
        '''
        # P1: the base url should not have had a trailing slash
        if self._looker_project_name and self._looker_host:
            self._deploy_url = \
                self._looker_host + 'webhooks/projects/' + self._looker_project_name + '/deploy'
        else:
            self._deploy_url = ''
    # base
    def put(self, f):
        if type(f) == File:
            new = self.new_file(f.path)
            new.write()
        if isinstance(f,f_github):
            f.write()

    def deploy(self):
        """
        Issues a webhook to have looker sync with your project remote

.. note:: this will only result in changes being displayed if you are deploying to master

.. note:: this will only work if you provided the looker_project_name and looker_host arguments when you initialized the project

        """
        # P3: check to see if project is on master,
        # if not issue warning that changes won't show up
        if self._deploy_url:
            requests.get(self._deploy_url)

class ProjectSSH(Project):
    class gitController:
        def __init__(
            self, outputPath='', projectName='', branch='master', deployMessage='', exePath='', includeGitDir=False
        ):
            # self.platform = platform.system()
            self.platform = 'linux'
            self.preamble = []
            self.trailers = []
            if self.platform == 'Windows':
                self.exe = exePath + ' '
                self.preamble.append(self.exe)
                self.trailers.append(' & exit')
            else:
                self.exe = ''
            self.projectName = projectName

            os.makedirs(outputPath, exist_ok=True)

            self.outputPath = outputPath
            self.absoluteOutputPath = os.path.abspath(self.outputPath)
            self.branch = branch
            self.deployMessage = deployMessage

            if os.path.exists(self.absoluteOutputPath):
                shutil.rmtree(self.absoluteOutputPath)

            os.makedirs(self.absoluteOutputPath, exist_ok=True)

            if self.projectName:
                self.gitDir = ' --git-dir="' + \
                    os.path.abspath(outputPath + '/' +
                                    self.projectName + '/.git') + '" '
            else:
                self.gitDir = ' --git-dir="' + \
                    os.path.abspath(outputPath + '/.git') + '" '

            self.includeGitDir = includeGitDir

            if self.includeGitDir:
                self.preamble.append(self.includeGitDir)

        def call(self, command, gitDir=True):
            if gitDir:
                tmp = ' '.join(self.preamble) + 'git ' + self.gitDir + \
                    ' ' + command + ' '.join(self.trailers)
            else:
                tmp = ' '.join(self.preamble) + 'git ' + \
                    command + ' '.join(self.trailers)
            print(tmp)
            proc = subprocess.Popen(
                tmp, shell=True, env=os.environ, cwd=self.absoluteOutputPath
            )
            try:
                outs, errs = proc.communicate(timeout=15)
            except subprocess.TimeoutExpired:
                proc.kill()
                outs, errs = proc.communicate()
            return self

        def pull(self):
            return self.call(' pull origin ' + self.branch + ' ', gitDir=False)

        def clone(self, repoLocation):
            self.call(' clone ' + repoLocation + ' ' +
                      self.absoluteOutputPath, gitDir=False)
            return self.pull()

        def add(self, path='.'):
            return self.call(' add ' + path, gitDir=False)

        def commit(self, message=''):
            if message:
                return self.call(' commit -m "' + message + ' ' + self.deployMessage + '"', gitDir=False)
            else:
                return self.call(' commit -m "' + self.deployMessage + '"', gitDir=False)

        def pushRemote(self):
            return self.call(' push origin ' + self.branch + ' ', gitDir=False)

    def __init__(
        self,
        git_url: str,
        looker_project_name: str, 
        path: str = '.tmp', 
        looker_host: str = None,  
        branch: str = 'master', 
        commitMessage: str = ''
        ):
        self._path = path
        self._index = dict()
        self._looker_host = looker_host
        self._looker_project_name = looker_project_name
        self.constructDeployUrl()
        self._git_url = git_url
        self._branch = branch
        self._commit_message = "PyLookML Auto Updated: " +\
            time.strftime(
                '%h %d %Y @ %I:%M%p %Z') if not commitMessage else commitMessage
        if self._git_url:
            self._path = self._path + '/' + self._looker_project_name
            self._git = self.gitController(
                outputPath=self._path, 
                projectName=self._looker_project_name, 
                branch=self._branch, 
                deployMessage=self._commit_message
            )
            self._git.clone(self._git_url)
        self._build_index()
    # shell
    def commit(self):
        """
        git commit and git push changes to remote in SSH mode
        """
        self._git.commit()
        self._git.pushRemote()

    def constructDeployUrl(self):
        '''
            Constructs a github deploy URL according to this pattern:
            https://prod.host.com/webhooks/projects/projectname/deploy
        '''
        # P1: the base url should not have had a trailing slash
        if self._looker_project_name and self._looker_host:
            self._deploy_url = \
                self._looker_host + 'webhooks/projects/' + self._looker_project_name + '/deploy'
        else:
            self._deploy_url = ''
    # base

    def deploy(self):
        """
        Issues a webhook to have looker sync with your project remote

.. note:: this will only result in changes being displayed if you are deploying to master

.. note:: this will only work if you provided the looker_project_name and looker_host arguments when you initialized the project

        """
        if self._deploy_url:
            requests.get(self._deploy_url)
