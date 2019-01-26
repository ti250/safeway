import requests
import json

quiz = {"origin": {"latitude": 50.39, "longitude": 40.31},
              "destination": {"latitude": 20.39, "longitude": 10.31},
              "arrive_by": {"hour": 12, "minute": 34, "timezone": -1},
              "safety_priority": 1.2}

url = "http://127.0.0.1:8000/safeway/route"
request = requests.post(url, data=json.dumps(quiz))
# request = requests.post(url, data=quiz)
print(request)
print(request.text)
