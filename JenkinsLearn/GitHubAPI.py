import requests
from pprint import pprint

import base64
from github import *
import json
import urllib



def create_pull_request(project_name, repo_name, title, description, head_branch, base_branch, git_token):
    """Creates the pull request for the head_branch against the base_branch"""
    #git_pulls_api = "https://github.com/api/v3/repos/{0}/{1}/pulls".format(project_name,repo_name)
    git_pulls_api = "https://github.com/repos/{0}/{1}/pulls".format(project_name,repo_name)
    headers = {
        "Authorization": "Bearer   {0}".format(git_token),
        #"Content-Type": "application/json"
        "Accept": "application/vnd.github+json" ,
        "X-GitHub-Api-Version": "2022-11-28"
        }

    payload = {
        'owner': project_name,
        'repo': repo_name,
        "title": title,
        "body": description,
        "head": head_branch,
        "base": base_branch,
       
    }

    s = requests.Session()

    # github username
    username = "x4nth055"
    # url to request
    url = f"https://api.github.com/users/{username}"
    # make the request and return the json
    user_data = requests.get(url).json()
    # pretty print JSON data
    pprint(user_data)


    #res = s.get('https://login.live.com')
    #cookies = dict(res.cookies)   

   
    #url = "https://api.github.com"
    #fields = {"issaab.dev@gmail.com": "@Beer1995Issa"}
    #string_query = urllib.urlencode(fields)
    #response = requests.get(url + '?' + string_query)
    #print (response.status_code)
    #print (response.content)

    token=(git_token)
    r = requests.post(
        git_pulls_api,headers=headers,
        data=json.dumps(payload))
#
    if not r.ok:
        print("Request Failed: {0}".format(r.text))
        print(r.content)
        #print (r.json())









# Github username
username = "DevIssaAb"
token='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'
allData = {
    'login': 'issaab.dev@gmail.com',
    'password': '@Beer1995Issa'
}

var ='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'
var2 ='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'

#create_pull_request(username,'Jenkins','Use instead of ','Hi issa branch','issa','main',var2)




#login into github account
login  = Github(var2)

#
##get the user
user  = login.get_user()
#
#repository_name= "Demo-Repo"
#
##create repository
#new_repo = user.create_repo(repository_name)
#
##create new file
#new_repo.create_file("New-File.txt", "new commit", "Data Inside the File")
repo = login.get_repo(f"{username}/Jenkins")
pr = repo.create_pull('Use instead of 19994', 'Hi issa branch19', head="issa", base="main")