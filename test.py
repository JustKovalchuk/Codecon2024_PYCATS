import requests

url = 'https://volonter.org/dopomoga-volonterski-proekty'
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the content of the response
    print(response.text)
else:
    print('Failed to fetch data from', url)
