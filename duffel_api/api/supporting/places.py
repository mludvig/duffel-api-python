from ...http_client import HttpClient
from ...models import Place


class PlaceClient(HttpClient):
    """Client to interact with Places"""

    def __init__(self, **kwargs):
        self._url = "/places/suggestions"
        super().__init__(**kwargs)

    def suggestions(self, name=None, radius_km=None, latitude=None, longitude=None):
        """GET /places/suggestions"""
        if name:
            if radius_km or latitude or longitude:
                raise ValueError(
                    "You can only pass name or radius_km, latitude and longitude"
                )
            query_params = {"name": name}
        elif radius_km and latitude and longitude:
            query_params = {
                "rad": radius_km * 1000,    # rad is in meters
                "lat": latitude,
                "lng": longitude,
            }
        else:
            raise ValueError(
                "You must pass name or radius_km, latitude and longitude"
            )

        res = self.do_get(self._url, query_params=query_params)
        places = []
        if res is not None:
            for place in res["data"]:
                places.append(Place.from_json(place))
        return places
