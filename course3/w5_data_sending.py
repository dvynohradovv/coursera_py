import requests
from requests.auth import HTTPBasicAuth


def first_request():
    url = "https://datasend.webpython.graders.eldf.ru/submissions/1/"
    auth = HTTPBasicAuth('alladin', 'opensesame')
    r = requests.post(url, auth=auth)
    print(r.request.headers.get("Authorization"))
    print(r.json())


def secretlocation_request():
    url = "https://datasend.webpython.graders.eldf.ru/submissions/secretlocation/"
    auth = HTTPBasicAuth("alibaba", "40razboinikov")
    r = requests.put(url, auth=auth)
    print(r.json())


if __name__ == "__main__":
    first_request()
    secretlocation_request()
