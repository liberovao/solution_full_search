import requests


def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        json_response = response.json()
        features = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        return features if features else None


def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    span = "{dx},{dy}".format(**locals())
    return (ll, span)


def get_nearest_object(point, kind):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "kind": kind,
        "geocode": ",".join(map(str, point)),
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {status} ({reason})""".format(status=response.status_code, reason=response.reason))

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"]
    geo_object = toponym[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
    return geo_object
