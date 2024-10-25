"""Use case: For the coastlines work we need to search all for all landsat images 
in arbitrary bounding boxes to calculate tide averages."""

from pystac_client import Client
from pystac_client.stac_api_io import StacApiIO
from urllib3 import Retry

# roughly the size of a dep tile
SEARCH_AREA = (148, -6, 149, -5)
CATALOG = "https://earth-search.aws.element84.com/v1"
RETRY = True


def big_search():
    if RETRY:
        retry = Retry(
            total=20,
            backoff_factor=1,
            status_forcelist=[403, 502, 503, 504],
            allowed_methods=None,
        )
        stac_api_io = StacApiIO(max_retries=retry)
        client = Client.open(CATALOG, stac_io=stac_api_io)
    else:
        client = Client.open(CATALOG)

    items = client.search(
        bbox=SEARCH_AREA, collections=["landsat-c2-l2"], datetime="1984/2024"
    ).items()
    return list(items)


if __name__ == "__main__":
    items = big_search()
    print(items)
