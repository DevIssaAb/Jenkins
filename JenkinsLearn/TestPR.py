import requests
import json

username = "DevIssaAb"
repo ='Jenkins'
token='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'

data = {
        'owner': username,
        'repo': repo,
        "title": "Amazing new feature",
        "body": "Please pull these awesome changes in!",
        "head": "issa",
        "base": "main",
}

r=requests.post(f'https://api.github.com/repos/{username}/{repo}/pulls',    headers = {
        "Authorization": "Bearer   {0}".format(token),
        "Accept": "application/vnd.github+json" ,
        "X-GitHub-Api-Version": "2022-11-28"
        },data=json.dumps(data))


if not r.ok:
    print("Request Failed: {0}".format(r.text))
    print(r.content)
    #print (r.json())