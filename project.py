import time
import subprocess, os, platform, shutil
import lookml
import github
import base64
import requests
import re
import file

def mkdir_force(dir):
    if not os.path.exists(dir):
        os.mkdir(dir,0o777)

def Project(repo='',access_token='',branch="master",git_url="",commitMessage="",looker_host="",looker_project_name="",outputPath='.tmp'):
    '''
        A LookML Project at a GitHub location or location on the filesytem [Factory Function]
        see _Project for subclass details
        '''
    if access_token and repo:
        return githubProject(repo=repo,access_token=access_token,branch=branch,git_url=git_url,commitMessage=commitMessage,looker_host=looker_host,looker_project_name=looker_project_name,outputPath=outputPath)
    elif git_url:
        return shellProject(repo=repo,access_token=access_token,branch=branch,git_url=git_url,commitMessage=commitMessage,looker_host=looker_host,looker_project_name=looker_project_name,outputPath=outputPath)

class project:
    '''
        A LookML Project at a GitHub location or location on the filesytem
        '''

    def __init__(self,repo='',access_token='',branch="master",git_url="",commitMessage="",looker_host="",looker_project_name="",outputPath='.tmp'):
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
            yield lookml.File(f)

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
        
        self.gitControllerSession =  self.gitController(projectName=self.looker_project_name, branch=self.branch, deployMessage=self.commitMessage, outputPath=self.outputPath)    
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
                    yield lookml.File(os.path.join(root, name))

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
        return lookml.File(self.gitControllerSession.absoluteOutputPath + '/' + path)

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
        if isinstance(f,lookml.File):
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
        elif isinstance(f,lookml.File):
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
        if isinstance(f,lookml.File):
            return checkgithub(f.path)
        elif isinstance(f,str):
            return checkgithub(f)
