import requests

data = '{"class_name": "Test", "token": "1234"}'

resp = requests.post("https://problemo.pro/api/new_client", data=data)

print(resp.status_code)
print(resp.text)
