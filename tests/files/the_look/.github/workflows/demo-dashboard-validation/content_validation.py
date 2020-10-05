import looker_sdk
import argparse
import os
import re
import requests
import json
import os.path
from os import path

#parse inputs
arguments = argparse.ArgumentParser()
arguments.add_argument('--dev-base-url',type=str)
arguments.add_argument('--dev-client-id',type=str)
arguments.add_argument('--dev-client-secret',type=str)
arguments.add_argument('--googledemo-client-id',type=str)
arguments.add_argument('--googledemo-client-secret',type=str)
arguments.add_argument('--project-name',type=str)
arguments.add_argument('--repo-path',type=str)

args = arguments.parse_args()

googledemo_base_url = 'https://googledemo.looker.com'
project_name = args.project_name
repo_path = args.repo_path

#create sdk connection to googledemo in order to find the dashboards 
os.environ['LOOKERSDK_BASE_URL']=googledemo_base_url+str(':19999')
os.environ['LOOKERSDK_CLIENT_ID']=args.googledemo_client_id
os.environ['LOOKERSDK_CLIENT_SECRET']=args.googledemo_client_secret
sdk = looker_sdk.init31()

#get the dashboards
dashboards = json.loads(sdk.run_look('44',result_format='json'))
dashboards_dict = {}
for dash in dashboards:
    if dash['core_demos.lookml_project_name'] == project_name:
        dashboards_dict[dash['demo_dashboards.development_dashboard_id']] = dash
dashboard_ids = dashboards_dict.keys()
sdk.logout()

#run content validator on dev
os.environ['LOOKERSDK_BASE_URL']=args.dev_base_url+str(':19999')
os.environ['LOOKERSDK_CLIENT_ID']=args.dev_client_id
os.environ['LOOKERSDK_CLIENT_SECRET']=args.dev_client_secret
sdk = looker_sdk.init31()

print('Running Content Validation')
results = sdk.content_validation()

broken_dashboards = [content.dashboard.id for content in results.content_with_errors if content.dashboard and content.dashboard.id in dashboard_ids]
with open(os.path.join(repo_path,'.github',"dashboard_errors.txt"),"w") as f:
    for i,dash in enumerate(broken_dashboards):
        if dash != broken_dashboards[0]:
            if i > 0:
                f.write(', ')
            f.write('<{} | {}>'.format(args.dev_base_url+'/dashboards/'+str(dash_id), dashboard_title))
        #f.write('\n' + args.dev_base_url +'/dashboards/'+str(dash))
    f.close()

def prepend_line(file_name, line):
    """ Insert given string as a new line at the beginning of a file """
    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

# for each dashboard get the lookml 
dash_to_import = []
#erase contents of the dashboard
open(os.path.join(repo_path,'.github',"new_dashboards.txt"),"w").close()
blank = 0
dash_path = os.path.join(repo_path,'dashboards')
if not path.exists(dash_path):
    os.mkdir(dash_path)
    #add include on all model files
    for root, dirs, files in os.walk(repo_path):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            if ".model" in file:
                if root == repo_path:
                    prepend_line(os.path.join(root, file), 'include: "dashboards/*.lookml"')
                else:
                    prepend_line(os.path.join(root, file), 'include: "/dashboards/*.lookml"')

def get_dashboard_path(filename):
    #check to see if dashboard exists in subfolder in /dashboards
    path = os.path.join(dash_path,filename)
    for root, dirs, files in os.walk(dash_path):
        for file in files:
            if filename == file:
                return os.path.join(root, file)
    return path
    

for dash_id in list(dashboard_ids):
    s_dash = sdk.dashboard(str(dash_id))
    dashboard_title = s_dash.title
    #dont import broken content
    if dash_id not in broken_dashboards:
        #check if the dashboard lookml file already exists
        # d_filename = re.sub('[^a-zA-Z0-9 \n\.]', '_', dashboard_title).replace(' ','_').lower()+'.dashboard.lkml'
        d_filename = dashboards_dict[dash_id]['demo_dashboards.lookml_dashboard_id'].split('::')[1]+'.dashboard.lookml'
        # dashboards_dict[dash_id]['filename'] = d_filename
        d_file_path = get_dashboard_path(d_filename)
        if os.path.exists(d_file_path):
            print(str(dash_id), ' dashboard already exists, reading lookml')
            with open(d_file_path,"r") as f:
                existing_dash = f.read()
        else:
            existing_dash = ''
            #if it does not exist add it to new dashboards text
            with open(os.path.join(repo_path,'.github',"new_dashboards.txt"),"a") as f:
                # f.write('\n' + dashboard_title + ': ' + args.dev_base_url+'/dashboards/'+str(dash_id))
                if blank != 0:
                    f.write(', ')
                f.write('<{} | {}>'.format(args.dev_base_url+'/dashboards/'+str(dash_id), dashboard_title))
                blank +=1
        
        new_dash = sdk.dashboard_lookml(str(dash_id)).lookml
        if existing_dash != new_dash:
            print(str(dash_id) + ' dashboard doesnt exist or has changed, lookml is being updated')
            dash_to_import.append(dash_id)
            #overwrite file with new contents
            with open(d_file_path,"w+") as f:
                f.seek(0)
                f.write(new_dash)
                f.truncate()
sdk.logout() 

                
