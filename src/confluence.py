import requests
import json

url = "https://delphix-hackathon.atlassian.net/wiki/rest/api/content"

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json",
   "Authorization": "Basic YWJoaWFnYXJ3YWw0MUBnbWFpbC5jb206ZHJUcXZwVEF6ZUxqM2cxV1h3aG4yQkU3"
}
payload = json.dumps({"type":"page","title":"new page",
"space":{"key":"HACKATHON"},"body":{"storage":{"value":"<p>This is <br/> a new page</p>","representation":
"storage"}}})

response = requests.request(
   "POST",
   url,
   data=payload,
   headers=headers
)
print(f"status code: {response.status_code}")
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))