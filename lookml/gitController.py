import subprocess, os, platform, logging
from datetime import datetime



import configparser as ConfigParser
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.read('settings/settings.ini')

# [git]
# #needs to be filled out on windows, can be left blank on unix like systems
# exePath = "C:\\Program Files\\Git\\git-cmd.exe"
# #refers to the folder holding the projects
# outputPath = output

CREATE_NEW_PROCESS_GROUP = 512



class gitController:
    def __init__(self, *args, **kwargs):
        self.platform = platform.system()
        self.preamble = []
        self.trailers = []
        if self.platform == 'Windows':
            self.exe = config.get('git', 'exePath') + ' '
            self.preamble.append(self.exe)
            self.trailers.append(' & exit')
        else:
            self.exe = ''
        self.projectName = kwargs.get('projectName','')
        self.outputPath = config.get('git', 'outputPath') + '/' + self.projectName
        self.absoluteOutputPath = os.path.abspath(self.outputPath)
        self.branch = kwargs.get('branch','master')
        
            
        self.deployMessage = kwargs.get('deployMessage','LookML Automated Deployment @' + datetime.now().strftime('%a %y-%m-%d %I:%M%p'))
        
        if not os.path.exists(self.absoluteOutputPath):
            os.mkdir(self.absoluteOutputPath,0o777)
        
        if self.projectName:
            self.gitDir = ' --git-dir="' + os.path.abspath(config.get('git', 'outputPath') + '/' + self.projectName + '/.git') + '" '
        else:
            self.gitDir = ' --git-dir="' + os.path.abspath(config.get('git', 'outputPath') + '/.git') + '" '
            
        self.includeGitDir = kwargs.get('includeGitDir', False)
        
        if self.includeGitDir:
            preamble.append(self.includeGitDir)
            
    def call(self, command, gitDir=True):
        if gitDir:
            tmp = ' '.join(self.preamble) + 'git ' + self.gitDir + ' ' + command + ' '.join(self.trailers)
        else:
            tmp = ' '.join(self.preamble) + 'git ' + command + ' '.join(self.trailers)
        # logging.info(tmp)
        print(tmp)
        # if self.platform == 'Windows':
        proc = subprocess.Popen(
                        tmp 
                        ,shell=True
                        ,env=os.environ
                        ,cwd=self.absoluteOutputPath
                        # ,creationflags=CREATE_NEW_PROCESS_GROUP
                        # ,stdout=subprocess.PIPE
                        # ,stderr=subprocess.PIPE
                        )
        # else:
                        # proc = subprocess.Popen(
                            # tmp 
                            # ,shell=False
                            # ,env=os.environ
                            # ,cwd=self.absoluteOutputPath
                            # ,stdout=subprocess.PIPE
                            # ,stderr=subprocess.PIPE
                            # )
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
        
    def add(self):
        return self.call(' add .')
        
    def commit(self, message=''):
        if message:
            return self.call(' commit -m "' + message + ' ' + self.deployMessage + '"')
        else:
            return self.call(' commit -m "' + self.deployMessage + '"')
        
    def pushRemote(self):
        return self.call(' push origin ' + self.branch + ' ')
        
        
        
        
        
        
        
        
        
        
            
        