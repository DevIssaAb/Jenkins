import requests
import json

username = "DevIssaAb"
repo ='Test101'
token='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'

data = {
        "name":"web",
        "active":True,
        "events":["push","pull_request"],
        "config":{"url":"https://example.com/webhook","content_type":"json","insecure_ssl":"0"
        },
}

r=requests.post(f' https://api.github.com/repos/{username}/{repo}/hooks', headers = {
        "Authorization": "Bearer   {0}".format(token),
        "Accept": "application/vnd.github+json" ,
        "X-GitHub-Api-Version": "2022-11-28"
        },data=json.dumps(data))


if not r.ok:
    print("Request Failed: {0}".format(r.text))
    print(r.content)
    #print (r.json())