# COS301-Broadsword-Users

## Final demo submission

### Angular-Mean
- npm install express, mongojs, bodyy-parser, multer, csvjson, xls-to-json, xlsx-to-json
- with running mongo instances:
  - node server.js 8080
  
### Python
- pip install pynsq, pymongo
- with runnning mongo instances:
  - nsqlookupd.exe "&"> nsqlookupd.log
  - nsqd.exe  --lookupd-tcp-address=127.0.0.1:4160 "&"> nsqd.log
  - curl -X POST http://127.0.0.1:4161/channel/create?topic=users"&"channel=navup
  - python reader.py
