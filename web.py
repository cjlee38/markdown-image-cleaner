import requests

class Requester :

    @staticmethod
    def is_alive(url) :
        resp = requests.get(url)
        return resp.ok