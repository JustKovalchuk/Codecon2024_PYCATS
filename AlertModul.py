import requests

url = "https://ubilling.net.ua/aerialalerts/"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()["states"]
    print(data)

except requests.RequestException as e:
    print("Помилка при виконанні запиту:", e)
