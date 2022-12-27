import requests

BASE = 'http://127.0.0.1:5000'

data = [
    {'likes': 800, 'name': 'Make thing good', 'views': 35},
    {'likes': 80000, 'name': 'Go go gadgeto texte', 'views': 200000},
    {'likes': 9528461, 'name': 'Bonjour frolo', 'views': 800000}
]
for i in range(len(data)):
    response = requests.put(f'''{BASE}/video/{i}''', data[i])
    print(response.json())
input()
response = requests.get(f'''{BASE}/video/1''')
print(response.json())
input()
response = requests.get(f'''{BASE}/video/6''')
print(response.json())
response = requests.patch(f'''{BASE}/video/2''', {'views': 99, 'likes': 101})
print(response.json())