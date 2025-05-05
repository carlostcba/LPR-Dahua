
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
import os

def fetch_last_snapshot(config):
    url = f"http://{config['ip']}/cgi-bin/snapshot.cgi"
    response = requests.get(url, auth=HTTPDigestAuth(config['user'], config['password']), stream=True)

    if response.status_code == 200:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not os.path.exists(config['snapshot_path']):
            os.makedirs(config['snapshot_path'])
        filename = os.path.join(config['snapshot_path'], f"lpr_{now}.jpg")
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return filename
    else:
        print(f"Error al obtener imagen: {response.status_code}")
        return None
