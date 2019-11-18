# reported in this issue:
# https://github.com/substrate-developer-hub/substrate-node-template/issues/11

import requests # pip install requests

url = "https://dev-node.substrate.dev:9933/"
print ("All working on dev-node: ", url, "\n")

headers = {"Content-Type" : "application/json"}
payload = {"method": "state_getMetadata", "id":"1", "jsonrpc":"2.0"}

print ("Passing a dict as data payload:")
print ("payload:", payload)
r = requests.post(url, data=payload, headers=headers)
print (r.status_code, r.text)

print ("Turning the dict into a string first:")
payload_string = "%s" % payload
print ("payload_string:", payload_string)
r = requests.post(url, data=payload_string, headers=headers)
print (r.status_code, r.text)

print ("Manipulating that string to make substrate happy:")
payload_string_manipulated = payload_string.replace("'", '"')
print ("payload_string_manipulated:", payload_string_manipulated)
r = requests.post(url, data=payload_string_manipulated, headers=headers)
rj = r.json()
rj['result'] = rj['result'][:30] + "..."
print (r.status_code, rj)
