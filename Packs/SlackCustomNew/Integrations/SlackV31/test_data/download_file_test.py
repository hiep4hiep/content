import requests
import shutil

url = "https://files.slack.com/files-pri/T0326BQ6QHJ-F05LK09ATNJ/download/screenshot_2023-06-30_at_2.51.02_pm.png.zip"

payload = {}
headers = {
  'Authorization': 'Bearer xoxb-3074398228596-5675330395559-UBGBxyat7pLDkMk6YImaoyC2'
}

with requests.get(url, url, headers=headers, stream=True) as r:
    with open("downloaded_file", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

file