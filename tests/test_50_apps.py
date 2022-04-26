import pathlib

import dask
import py
import xarray as xr
import pytest

from sarsen import apps

dask.config.set(scheduler="single-threaded")

DATA_FOLDER = pathlib.Path(__file__).parent / "data"

GRD_IW = (
    DATA_FOLDER
    / "S1B_IW_GRDH_1SDV_20211223T051122_20211223T051147_030148_039993_5371.SAFE"
)
DEM_RASTER = DATA_FOLDER / "Rome-30m-DEM.tif"


@pytest.mark.xfail
def test_terrain_correction_gtc(tmpdir: py.path.local) -> None:
    out = str(tmpdir.join("GTC.tif"))
    res = apps.terrain_correction(
        str(GRD_IW),
        "IW/VV",
        str(DEM_RASTER),
        output_urlpath=out,
        chunks={"slant_range_time": 1000, "azimuth_time": 1000},
    )

    assert isinstance(res, xr.DataArray)


@pytest.mark.xfail
def test_terrain_correction_fast_rtc(tmpdir: py.path.local) -> None:
    out = str(tmpdir.join("RTC.tif"))

    res = apps.terrain_correction(
        str(GRD_IW),
        "IW/VV",
        str(DEM_RASTER),
        correct_radiometry="gamma_nearest",
        output_urlpath=out,
        chunks={"slant_range_time": 1000, "azimuth_time": 1000},
    )

    assert isinstance(res, xr.DataArray)


@pytest.mark.xfail
def test_terrain_correction_rtc(tmpdir: py.path.local) -> None:
    out = str(tmpdir.join("RTC.tif"))

    res = apps.terrain_correction(
        str(GRD_IW),
        "IW/VV",
        str(DEM_RASTER),
        correct_radiometry="gamma_bilinear",
        output_urlpath=out,
        chunks={"slant_range_time": 1000, "azimuth_time": 1000},
    )

    assert isinstance(res, xr.DataArray)