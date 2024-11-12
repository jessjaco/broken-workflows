import boto3
import odc.stac
from odc.geo.xr import write_cog
from pystac_client import Client
from dask.distributed import Client as DDClient
from typer import run

# roughly the size of a dep tile
SEARCH_AREA = (148, -6, 149, -5)
CATALOG = "https://earth-search.aws.element84.com/v1"
DATETIME = "2021"


def main(datetime: str = DATETIME):
    client = Client.open(CATALOG)

    items = client.search(
        bbox=SEARCH_AREA, collections=["landsat-c2-l2"], datetime=datetime
    ).items()

    ds = odc.stac.load(
        items,
        chunks=dict(time=1, x=1024, y=1024),
        bands=["nir08", "swir16", "swir22", "red", "blue", "green"],
    )
    median = ds.median(dim="time")
    for var in ds:
        print(var)
        write_cog(median[var], "temp.tif")


if __name__ == "__main__":
    odc.stac.configure_s3_access(cloud_defaults=True, requester_pays=True)
    with DDClient():
        run(main)
