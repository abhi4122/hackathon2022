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

    value = "<h2>Recognitions</h2><h2>Work " \
            "Anniversaries</h2><h2>Release Updates</h2><h2>Project " \
            "Updates</h2><h2>Initiatives</h2><h2>Ted Talks - Python</h2><h2>Fun Activities and " \
            "Events</h2><h2>Miscellaneous</h2><h2>New Joiners</h2> "

    payload = json.dumps({
        "space": {"key": "HACKATHON"},
        "ancestors": [{"id": parent_page_id}],
        "title": page_name,
        "type": "page",
        "body": {
            "storage": {
                "value": value,
                "representation": "storage"
            },
        }
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers
    )
    print(f"create page status code: {response.status_code}")
    data = json.loads(response.text)
    return data["id"]


def get_page_version(page_id):
    updated_url = f"{url}/{page_id}"

    headers = {
        "Accept": "application/json",
        "Authorization": token
    }
    response = requests.request(
        "GET",
        updated_url,
        headers=headers
    )
    print(f"get page version status code: {response.status_code}")
    data = json.loads(response.text)
    return data["version"]["number"], data["title"]


def update_page(page_id, message):
    curr_version, title = get_page_version(page_id)
    update_url = f"{url}/{page_id}"

    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json",
       "Authorization": token
    }

    payload = json.dumps({
      "version": {
        "number": curr_version + 1
      },
      "title": title,
      "type": "page",
      "body": {
        "storage": {
          "value": message,
          "representation": "storage"
        },
      }
    })

    response = requests.request(
       "PUT",
       update_url,
       data=payload,
       headers=headers
    )

    print(f"update page version status code: {response.status_code}")

# page_id = get_page_id("August2022")
# print(page_id)
#
# if page_id is None:
#     create_page("August2022")
