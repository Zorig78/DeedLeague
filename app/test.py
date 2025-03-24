import requests

BASE="http://127.0.0.1:5000/"

response=requests.put(BASE+"video/1", json={"name":"Masterboy","views":2300,"likes":10})
print(response.json())
input()
response=requests.get(BASE+"video/1")

print(response.json())

