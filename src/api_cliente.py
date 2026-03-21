import requests

url = "https://swapi.dev/api/people/"

for people in range(1, 5):
    response = requests.get(url + str(people))
    personajes = response.json()

    print(personajes["name"])
    print("\n")