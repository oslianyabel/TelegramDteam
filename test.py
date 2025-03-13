import os

import requests

if __name__ == "__main__":
    data = {"thread_id": "1", "message": "hola"}
    response = requests.post(os.getenv("URL_API"), json=data)
    print(response.status_code)
    ans = response.json()
    print(ans["thread_id"])
    print(ans["message"])
