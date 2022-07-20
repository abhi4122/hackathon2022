import requests
import json
from bs4 import BeautifulSoup

url = "https://delphix-hackathon.atlassian.net/wiki/rest/api/content"
token = "Basic YWJoaWFnYXJ3YWw0MUBnbWFpbC5jb206ZHJUcXZwVEF6ZUxqM2cxV1h3aG4yQkU3"


def get_page_id(page_name):
    """
    Method to fetch page id based on given
    page name

    :param page_name : Name of the page to fetch
        page id for
    :type page_name : ```str```
    """
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
    """
    Method to update page contents

    :param page_name : Title to create new page with
    :type page_name : ```str```
    """
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
    """
    Method to fetch current page version

    :param page_id : id of the page to fetch version for
    :type page_id : ```str```
    """
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


def _create_body(to_append, category, page_id=None):
    """
    Method to create payload for create and update
    page operations

    :param to_append : message to be appended to Newsletter
    :type to_append: ```str```
    :param category : category for message to be appended to
    :type category : ```str```
    :param page_id : id of the page to be updated
    :type page_id : ```str```
    """

    get_page_content_url = f"{url}/{page_id}"
    headers = {
        "Accept": "application/json",
        "Authorization": token,
    }
    params = {"expand": "body.storage"}

    response = requests.request("GET", get_page_content_url, headers=headers, params=params)
    html_text = str(json.loads(response.text)['body']['storage']['value'])
    soup = BeautifulSoup(html_text, 'html.parser')

    final_append = "<li><p>" + to_append + "</p></li>"
    child = BeautifulSoup(final_append, 'html.parser')

    for value in soup.find_all():
        if value.text.strip() == category:
            if 'li' in str(value.next_sibling):
                value.next_sibling.append(child)
            else:
                value.insert(child)
            break

    return str(soup)


def update_page(page_id, message_to_append, category):
    """
    Method to update page contents

    :param page_id : id of the page to be updated
    :type page_id : ```str```
    :param message_to_append : message to be appended to
        Newsletter
    :type message_to_append : ```str```
    :param category : category for message to be appended to
    :type category : ```str```
    """
    curr_version, title = get_page_version(page_id)
    update_url = f"{url}/{page_id}"

    body = _create_body(
        message_to_append,
        category,
        page_id=page_id
    )

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
          "value": body,
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
