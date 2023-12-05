from ...http_client import HttpClient, Pagination
from ...models import City


class CityClient(HttpClient):
    """Client to interact with Cities"""

    def __init__(self, **kwargs):
        self._url = "/air/cities"
        super().__init__(**kwargs)

    def get(self, id_):
        """GET /air/cities/:id"""
        res = self.do_get(f"{self._url}/{id_}")
        if res is not None:
            return City.from_json(res["data"])

    def list(self, limit=50):
        """GET /air/cities"""
        return Pagination(self, City, {"limit": limit})
