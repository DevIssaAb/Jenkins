import requests
from pprint import pprint

import base64
from github import Github


# github username
username = "DevIssaAb"
# url to request
url = f"https://api.github.com/users/{username}"
# make the request and return the json
user_data = requests.get(url).json()
# pretty print JSON data
pprint(user_data)



# Github username
username = "DevIssaAb"
# pygithub object
g = Github()
# get that user by username
user = g.get_user(username)

for repo in user.get_repos():
    print(repo)

repo = g.get_repo("DevIssaAb/Jenkins")

body = '''
SUMMARY
Change HTTP library used to send requests

TESTS
  - [x] Send 'GET' request
  - [x] Send 'POST' request with/without body
'''
pr = repo.create_pull(title="Use 'requests' instead of 'httplib'", body=body, head="develop", base="master")
pr.PullRequest(title="Use 'requests' instead of 'httplib'", number=664)