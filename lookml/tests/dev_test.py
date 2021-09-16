import lookml
import lookml.lkml as lkml
import unittest, copy, json
from pprint import pprint
import warnings
import configparser
import pprint, base64
from looker_sdk import models, methods, init40
import os
import github
from pathlib import Path

config = configparser.ConfigParser()
config.read('lookml/tests/.conf/api.ini')
githubConf = configparser.ConfigParser()
githubConf.read('lookml/tests/.conf/settings.ini')

class projectCreation(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_project_creation(self):
        #pygithub repo creation
        #project creation in looker
        #associate deploy key
        #sync
        pass

    def test_remote_project_creation(self):

        # connect to Looker
        os.environ['LOOKERSDK_BASE_URL'] = config['Looker']['base_url']
        os.environ['LOOKERSDK_CLIENT_ID'] =  config['Looker']['client_id']
        os.environ['LOOKERSDK_CLIENT_SECRET'] =  config['Looker']['client_secret']
        sdk = init40()
        sdk.update_session(body={ 'workspace_id': 'dev'})
        # connect to github
        _github = github.Github(githubConf['github']['access_token'])
        # create repo on github
        user = _github.get_user()
        # repo = user.create_repo('example_789')
        repo = user.get_repo('example_789')
        p = sdk.create_project({
                "id": "pylookml_testing_4",
                "name": "pylookml_testing_4",
                "uses_git": True,
                # "git_remote_url": repo.ssh_url,
                # "git_username": "string",
                # "git_password": "string",
                # "git_username_user_attribute": "string",
                # "git_password_user_attribute": "string",
                # "git_service_name": "string",
                # "git_application_server_http_port": 0,
                # "git_application_server_http_scheme": "string",
                # "deploy_secret": "string",
                # "unset_deploy_secret": true,
                # "pull_request_mode": "string",
                # "validation_required": true,
                # "git_release_mgmt_enabled": true,
                # "allow_warnings": true,
                # "is_example": true,
                # "dependency_status": "string"
            })
        x = sdk.create_git_deploy_key(p.id)
        sdk.update_project("pylookml_testing_4", {"git_remote_url": repo.ssh_url})
        print(x)
        repo.create_key(title='foo',key=x)
        print(repo)


        # Looker sdk.create_project()
        # sdk.create_project({
        #     "id": "foo_123",
        #     "name": "foo_123",
        #     "uses_git": True,
        #     "git_remote_url": "string",
        #     "git_username": "string",
        #     "git_password": "string",
        #     "git_username_user_attribute": "string",
        #     "git_password_user_attribute": "string",
        #     "git_service_name": "string",
        #     "git_application_server_http_port": 0,
        #     "git_application_server_http_scheme": "string",
        #     "deploy_secret": "string",
        #     # "unset_deploy_secret": true,
        #     # "pull_request_mode": "string",
        #     # "validation_required": true,
        #     # "git_release_mgmt_enabled": true,
        #     # "allow_warnings": true,
        #     # "is_example": true,
        #     # "dependency_status": "string"
        # })
        # Looker update_project? -> somehow get the deploy key
        # pygithub create_key(title, key, read_only=False) https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository.create_key
        # does the looker project then need to complete setup?
        # optional: retrieve the dev branch for a user
        # add a readme stating that the project was created programatically
        # optional -> start with a template
        # deploy to production
        pass


    def test_dense_lookml_option(self):
        lookml.lib.lang.ws.dense_children_threshold = 0
        # lookml.DENSE_LOOKML_THRESHOLD = 0
        print(lookml.Dimension('dimension: foo { hidden: yes sql: ${TABLE}.foo ;; }'))

    def test_branch_switch(self):
        pass

    def test_initialize_credentials(self):
        conf = configparser.ConfigParser()
        home = str(Path.home())
        # print(home)
        # print(os.path.abspath(f'{home}/pylookml.ini'))
        if os.path.exists(f'{home}/pylookml.ini'):
            conf.read(f'{home}/pylookml.ini')
            print(conf['dat.dev.looker']['base_url'])
        elif os.path.exists(f'{home}/.pylookml'):
            conf.read(f'{home}/.pylookml')
            print(conf)
        elif os.path.exists('.pylookml'):
            conf.read('.pylookml')
            print(conf)
        elif os.path.exists('pylookml.ini'):
            conf.read('pylookml.ini')
            print(conf)
        else:
            raise Exception('''pylookml.ini not found. Please add to ~/pylookml.ini or add pylookml.ini to the current working directory.
            file can also be named .pylookml to remain hidden
            ''')