import base64
import zlib
import datetime

template = [
    {
      "created":"2023-10-10T02:40:06.393687Z",
      "description":"n/a",
      "id":"artifact--44c558a6-8a10-5e28-9628-51b1540fb5b7",
      "labels":[
         "admiralty-scale:information-credibility=\"4\""
        ],
      "object_marking_refs":[
          "marking-definition--f88d31f6-486f-44dab317-01333bde0b82"
        ],
      "modified":"2023-10-10T02:40:06.393687Z",
      "payload_bin":"somethingsomething",
      "memie_type":"image/jpeg",
      "spec_version":"2.1",
      "type":"artifact",
      "valid_from":"2023-10-10T02:40:46.540264Z"
   }
]

def get_file_data(file_path, zip=False):
    with open(file_path, 'rb') as f:
        data = f.read()
        if zip:
            data = zlib.compress(data)

    return base64.b64encode(data).decode('utf-8')


def main():
    entry_id = demisto.args()['entryId']
    res = demisto.getFilePath(entry_id)
    if not res:
        return_error("Entry {} not found".format(entry_id))
    file_path = res['path']
    file_name = res['name']
    file_base64 = get_file_data(file_path, False)
    data = [
      {
      "created": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
      "description":"n/a",
      "id":"artifact--44c558a6-8a10-5e28-9628-51b1540fb5b7",
      #"labels":[
      #   "admiralty-scale:information-credibility=\"4\""
      #  ],
      "object_marking_refs":[
          "marking-definition--f88d31f6-486f-44dab317-01333bde0b82"
        ],
      "modified": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
      "payload_bin": file_base64,
      "mime_type":"image/" + file_name.split(".")[-1],
      "spec_version":"2.1",
      "type":"artifact",
      "valid_from":"2023-10-10T02:40:46.540264Z"
      }
    ]


if __name__ in ('__main__', '__builtin__', 'builtins'):
    
    main()