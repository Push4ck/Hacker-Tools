import requests
from itertools import cycle

ip_list = ['1.1.1.1', '2.2.2.2', '3.3.3.3']

for ip in cycle(ip_list):

    proxies = {'http': f'http://{ip}', 'https': f'https://{ip}'}

    response = requests.get('http://example.com', proxies=proxies)

    print(response.status_code)
