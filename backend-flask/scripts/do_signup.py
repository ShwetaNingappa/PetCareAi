import sys
import json
import urllib.request

email = sys.argv[1]
password = sys.argv[2]
url = 'http://127.0.0.1:5000/signup'
req = urllib.request.Request(url, data=json.dumps({'email': email, 'password': password}).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode('utf-8')
        print('STATUS', resp.status)
        print(body)
except Exception as e:
    print('ERROR', e)
