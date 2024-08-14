import http.client
import json

from models.ResponseRandom import ResponseRandom
import os
from dotenv import load_dotenv
load_dotenv()

def GetRandomString():
  conn = http.client.HTTPSConnection("api.random.org")
  payload = json.dumps({
    "jsonrpc": "2.0",
    "method": "generateStrings",
    "params": {
      "apiKey": os.getenv('API_KEY_RANDOM'), 
      "n": 1,
      "length": 32,
      "characters": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
      "replacement": True
    },
    "id": 0
  })
  headers = {
    'Content-Type': 'application/json'
  }
  
  try:
    conn.request("POST", "/json-rpc/4/invoke", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    jsonstring = json.loads(data.decode("utf-8"))
    root = ResponseRandom.from_dict(jsonstring)
    return root.result.random.data[0]
  except Exception as e:
    return e

