import requests
import json

url = "https://delphix-hackathon.atlassian.net/wiki/rest/api/content"
token = "Basic YWJoaWFnYXJ3YWw0MUBnbWFpbC5jb206ZHJUcXZwVEF6ZUxqM2cxV1h3aG4yQkU3"


def get_page_id(page_name):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": token
    }
    response = requests.request(
        "GET",
        url,
        headers=headers
    )
    print(f"get page status code: {response.status_code}")
    data = json.loads(response.text)
    for result in data["results"]:
        if result["title"] == page_name:
            return result["id"]
    return None


def create_page(page_name):
    parent_page_id = get_page_id("Newsletter")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": token
    }
    payload = json.dumps({"type": "page", "title": page_name,
                          "space": {"key": "HACKATHON"}, "ancestors": [{"id": parent_page_id}],
                          "body": {"storage": {"value": "<p></p>", "representation":
                              "storage"}}})

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers
    )
    print(f"create page status code: {response.status_code}")
    data = json.loads(response.text)
    return data["id"]

# page_id = get_page_id("August2022")
# print(page_id)
#
# if page_id is None:
#     create_page("August2022")
