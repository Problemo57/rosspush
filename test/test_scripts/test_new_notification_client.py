import requests

resp = requests.post("https://problemo.pro/api", data={"Halo": "Welt"})

print(resp.status_code)
print(resp.text)
