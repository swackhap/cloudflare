import os
import sys
import json
import glob
import time
import getpass
import argparse
import requests

#Input arguments
parser = argparse.ArgumentParser()
parser.add_argument('-email', help='Email address)', required=True, metavar='')
parser.add_argument('-key', help='API key', required=True, metavar='')
parser.add_argument('-org', help='Organization ID (Optional)', required=False, metavar='')
args = parser.parse_args()

#Parse arguments
if args.email:
	email = args.email
else:
    email = raw_input('Email Address: ')
if args.key:
	key = args.key
else:
    key = getpass.getpass('API Key:')
if args.org:
    org = args.org

# Cloudflare API v4 endpoint.
cfApi = 'https://api.cloudflare.com/client/v4/'

# Declare API session, supply credentials.
apiSession = requests.Session()
apiSession.headers.update({'X-Auth-Email': '%s' % email,
						   'X-Auth-Key': '%s' % key})

# Get list of BIND files in current OS directory (ex: 'domain.com.txt').
bindFiles = glob.glob('*.txt')

# Create a zone by supplying a zone name.
def createZone(zoneName):
    print 'Creating zone:  %s' % zoneName
    if args.org:
        values = {'name':zoneName,'jump_start':False,'organization':{'id':org,'status':'active','permissions':['#analytics:read', '#app:edit', '#billing:edit', '#billing:read', '#cache_purge:edit', '#dns_records:edit', '#dns_records:read', '#lb:edit', '#lb:read', '#logs:read', '#member:edit', '#member:read', '#organization:edit', '#organization:read', '#ssl:edit', '#ssl:read', '#waf:edit', '#waf:read', '#zone:edit', '#zone:read', '#zone_settings:edit', '#zone_settings:read']}}
    else:
        values={'jump_start':False, 'name': zoneName}
    headers = {'content-type': 'application/json'}
    createResult = apiSession.post( cfApi + 'zones', data=json.dumps(values), headers=headers)
    createJson = json.loads(createResult.content)
    if createJson['success'] == True:
        print '  Zone created.'
        time.sleep(1)
        return createJson['result']['id']
    elif createJson['success'] == False:
        print '  Error creating zone:' + str(createJson['errors'])
        print '\n\n'
        return None
        
# Upload a BIND file to the zone created with createZone().
def uploadBind(fileName,zoneID):
    print 'Uploading BIND file %s' % fileName
    files = {'file': (str(fileName), open(str(fileName), 'rb+'), 'multipart/form-data')}
    uploadResult = apiSession.post(cfApi + 'zones/' + zoneID + '/dns_records/import', files=files)
    uploadJson = json.loads(uploadResult.content)
    if uploadJson['success'] == True:
        print '  BIND file uploaded.\n\n'
    elif uploadJson['success'] == False:
        print '  Error uploading BIND file.'
        print uploadJson
    return uploadJson['result']

# Parse zone files in directory, create a zone for each, and upload the file.
for bindFile in bindFiles:
    zoneName = bindFile[:-4]
    fileName = bindFile
    zoneID = createZone(zoneName)
    if zoneID != None:
        bindUpload = uploadBind(fileName,zoneID)