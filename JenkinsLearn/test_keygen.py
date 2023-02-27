import requests 
import json
import glob
import os
import pathlib
import argparse
import sys

account = 'waylandadditive'
token = 'admin-1a253dc012318b12154e40ae05dc3505d8ba9b7efe0094068a1b775317b7e16bv3'
product_id = '5e47de47-d2da-4844-a9ec-17ea765bba40' # Prep
repository_path = 'C:/development/installer_repo/master'

def upload_artifact(release_id, filename, filetype, physical_path):
  # First create the artifact
  res = requests.post(
    'https://api.keygen.sh/v1/accounts/'+account+'/artifacts',
    headers={
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Prefer': 'no-redirect',
      'Authorization': 'Bearer ' + token
    },
    data=json.dumps({
      'data': {
        'type': 'artifact',
        'attributes': {
          'filename': filename,
          'filetype': filetype
        },
        'relationships': {
          'release': {
            'data': {
              'type': 'release',
              'id': release_id
            }
          }
        }
      }
    })
  )

  if res.status_code == 422:
    print ('File already uploaded!')

  if res.status_code == 200:
    print ('Redirect found')
    url = res.json()['data']['links']['redirect']

    
    # Upload to AWS servers using PUT
    mode = 'rb'
    content_type = 'application/octet-stream'

    if (filetype == 'xml'):
      mode = 'r'
      content_type = 'application/xml'
    
    file = open(physical_path, mode) # where r = reading, b = binary

    res = requests.put(
      url,
      headers={
        'Content-Type': content_type,
        'Accept': '*/*'
      },
      data = file.read()
    )
    print('Response from AWS S3: ' + str(res.status_code) + ', ' +  res.reason)

def ReadVersion():
  WaylandDir = os.environ['WAYLAND_BUILD']
  with open(WaylandDir+"\src\core\eb_version.h", "r+") as f:
      lines = f.readlines()
  for line in lines:
      if "EB_VERSION_MAJOR " in line:
          x1 = line.split(" ")[2].split("\n")[0]
      if "EB_VERSION_MINOR " in line:
          x2 = line.split(" ")[2].split("\n")[0]
      if "EB_VERSION_BID " in line:
          x3 = line.split(" ")[2].split("\n")[0]
  Version = x1 + "." + x2 + "." + x3
  return Version

#------------------------------------------------------------------------------------------------------------------
# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('channel', help='Channel type of the new release')
args = parser.parse_args()

channel = "dev" # default as development channel
if(args.channel != ""):
    channel = args.channel

version = ReadVersion() # read version from eb_version.h
if channel != "stable":
  version += "-" + channel 

name = "Release " + version

#------------------------------------------------------------------------------------------------------------------
# Remove latest tag from release
releases = requests.get(
  "https://api.keygen.sh/v1/accounts/"+account+"/releases/",
  headers={
    "Authorization": "Bearer " + token,
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json"
  }
).json()

duplicate = False
for release in releases['data']:
  release_version = release['attributes']['version']
  if(release_version == version):
     duplicate = True

if(duplicate == True):
  print("ERROR: Release already exists")
  sys.exit(1)

res = requests.get(
  "https://api.keygen.sh/v1/accounts/"+account+"/releases/latest",
  headers={
    "Authorization": "Bearer " + token,
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json"
  }
)

if(res.ok):
  v = res.json()['data']['attributes']['version']
  res = requests.patch(
    "https://api.keygen.sh/v1/accounts/"+account+"/releases/latest",
    headers={
      "Authorization": "Bearer " + token,
      "Content-Type": "application/vnd.api+json",
      "Accept": "application/vnd.api+json"
    },
    data=json.dumps({
      "data": {
        "type": "releases",
        "attributes": {
          "tag": v
        }
      }
    })
  ).json()

# Create new release with latest tag
res = requests.post(
  "https://api.keygen.sh/v1/accounts/"+account+"/releases",
  headers={
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json",
    "Authorization": "Bearer " + token
  },
  data=json.dumps({
    "data": {
      "type": "release",
      "attributes": {
        "name": name,
        "version": version,
        "channel": channel,
        "tag": "latest"
      },
      "relationships": {
        "product": {
          "data": {
            "type": "product",
            "id": product_id
          }
        }
      }
    }
  })
).json()

new_release_id = res['data']['id']

#------------------------------------------------------------------------------------------------------------------
# Loop through repository folder
for filename in glob.iglob(repository_path + '**/**', recursive=True):
    filename = pathlib.PureWindowsPath(filename).as_posix()
    short = filename[len(repository_path)+1::]
    short = os.path.join('repo',short)
    short = pathlib.PureWindowsPath(short).as_posix()
    name = os.path.basename(filename)
    extension = os.path.splitext(filename)[1][1::]
    if(extension):
      print(short +" : "+ name + " : " + extension)
      upload_artifact(new_release_id, short, extension, filename)
