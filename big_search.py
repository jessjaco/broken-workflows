"""Use case: For the coastlines work we need to search all for all landsat images 
in arbitrary bounding boxes to calculate tide averages."""

from pystac_client import Client
from pystac_client.stac_api_io import StacApiIO
from typer import run
from urllib3 import Retry

# roughly the size of a dep tile
SEARCH_AREA = (148, -6, 149, -5)
CATALOG = "https://earth-search.aws.element84.com/v1"
RETRY = False
DATETIME = "2020"


def big_search(catalog: str = CATALOG, retry: str = "yes", datetime: str = DATETIME):
    if retry == "yes":
        max_retries = Retry(
            total=20,
            backoff_factor=1,
            status_forcelist=[403, 502, 503, 504],
            allowed_methods=None,
        )
        stac_api_io = StacApiIO(max_retries=max_retries)
        client = Client.open(catalog, stac_io=stac_api_io)
    else:
        client = Client.open(catalog)

    items = client.search(
        bbox=SEARCH_AREA, collections=["landsat-c2-l2"], datetime=datetime
    ).items()
    print(list(items))


if __name__ == "__main__":
    run(big_search)
