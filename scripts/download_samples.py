#!/usr/bin/env python3
"""
Downloader for small, publicly accessible sample datasets for the
data4sustainablecities project. These samples are intentionally small to keep
the repository light while providing working examples and folder structure.

Sources included:
 - NASA GIBS / Worldview: MODIS Terra Corrected Reflectance True Color (PNG)
 - NASA Earth Observatory: sample image (JPEG)
 - WRI Data Explorer: sample CSV (small)

Note: Some providers require logins or are large; for those, we add placeholders
and instructions rather than attempting automated downloads.
"""

from __future__ import annotations

import os
import sys
import json
import time
from pathlib import Path
from typing import Optional

try:
    import requests
except Exception as import_error:  # pragma: no cover
    print("The 'requests' package is required. Install with: pip install requests")
    raise


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def ensure_directory(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def http_download(url: str, out_path: Path, timeout_seconds: int = 60) -> bool:
    try:
        with requests.get(url, stream=True, timeout=timeout_seconds) as resp:
            resp.raise_for_status()
            ensure_directory(out_path.parent)
            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return True
    except Exception as e:  # pragma: no cover
        print(f"Failed to download {url}: {e}")
        return False


def save_metadata(path: Path, metadata: dict) -> None:
    ensure_directory(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, sort_keys=True)


def download_worldview_sample(date: str = "2020-01-01") -> Optional[Path]:
    """
    Download a small PNG from NASA GIBS WMS as a Worldview-like snapshot.
    We use a 512x512 tile over a small bbox to keep size modest.

    Layer: MODIS_Terra_CorrectedReflectance_TrueColor (EPSG:4326)
    """
    # WMS GetMap endpoint for GIBS (EPSG:4326)
    wms = (
        "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi"
        "?SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0"
        "&LAYERS=MODIS_Terra_CorrectedReflectance_TrueColor"
        "&STYLES=&FORMAT=image/png&TRANSPARENT=TRUE"
        "&HEIGHT=512&WIDTH=512&CRS=EPSG:4326"
        # Small bbox roughly around New York City
        "&BBOX=40.4,-74.4,41.0,-73.6"
        f"&TIME={date}"
    )
    out_dir = DATA_DIR / "worldview"
    ensure_directory(out_dir)
    out_path = out_dir / f"worldview_truecolor_{date}.png"
    ok = http_download(wms, out_path)
    if ok:
        save_metadata(
            out_dir / f"worldview_truecolor_{date}.json",
            {
                "source": "NASA GIBS / Worldview",
                "layer": "MODIS_Terra_CorrectedReflectance_TrueColor",
                "projection": "EPSG:4326",
                "bbox": [40.4, -74.4, 41.0, -73.6],
                "size": [512, 512],
                "format": "image/png",
                "url": wms,
                "license": "Publicly available imagery via NASA GIBS; see NASA usage policies",
            },
        )
        return out_path
    return None


def download_earth_observatory_sample() -> Optional[Path]:
    """
    Download a representative small JPEG from NASA Earth Observatory.
    We choose a known small preview-sized image to keep repository light.
    """
    # Use a known small image (thumbnail) from Earth Observatory.
    # Note: URLs can change; this is best-effort and safe to skip if unavailable.
    url = (
        "https://earthobservatory.nasa.gov/ContentFeature/BlueMarble/Images/land_ocean_ice_2048.jpg"
    )
    out_dir = DATA_DIR / "earth_observatory"
    ensure_directory(out_dir)
    out_path = out_dir / "sample_earth_observatory.jpg"
    ok = http_download(url, out_path)
    if ok:
        save_metadata(
            out_dir / "sample_earth_observatory.json",
            {
                "source": "NASA Earth Observatory",
                "title": "Blue Marble (sample image)",
                "url": url,
                "license": "Please see NASA Earth Observatory usage guidelines",
            },
        )
        return out_path
    return None


def download_wri_sample() -> Optional[Path]:
    """
    Download a small CSV from WRI Data Explorer (if available via direct link).
    If not available, create a placeholder README with instructions.
    """
    out_dir = DATA_DIR / "wri"
    ensure_directory(out_dir)

    # Example: WRI frequently uses Socrata or CKAN backends. A portable small CSV
    # that is generally available is hard to guarantee. We will try a known small
    # CSV from WRI's datasets portal. If it fails, we write instructions instead.
    candidates = [
        # Placeholder/example CSV; may change or redirect. Best effort.
        "https://datasets.wri.org/dataset/8f6b2c8e-e5b6-4c5e-8b7b-21f5b7a3b0ba/resource/8f37a987-b2e0-4a11-9d53-8b0d2050b1fe/download/sample.csv",
    ]

    for url in candidates:
        out_path = out_dir / "wri_sample.csv"
        if http_download(url, out_path):
            save_metadata(
                out_dir / "wri_sample.json",
                {
                    "source": "World Resources Institute (WRI) Data Explorer",
                    "url": url,
                    "notes": "Small sample CSV for demonstration; replace with a project-relevant dataset",
                },
            )
            return out_path

    # If none succeeded, create instructions file
    with open(out_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(
            "Could not fetch a small WRI CSV automatically.\n"
            "Please visit https://data.wri.org/ and download a small CSV, then place it here as wri_sample.csv.\n"
        )
    return None


def write_placeholders_for_sedac_worldpop_ghsl_copernicus_eotoolkit() -> None:
    placeholders = {
        "sedac": (
            "SEDAC datasets often require login. Create a free account at https://sedac.ciesin.columbia.edu/.\n"
            "Once downloaded, place a small sample file here and document it in a metadata JSON.\n"
        ),
        "worldpop": (
            "WorldPop provides country-level population rasters. Visit https://www.worldpop.org/ to download a small country tile.\n"
            "Place the file here and add a metadata JSON noting the source and license.\n"
        ),
        "ghsl": (
            "GHSL (EU Copernicus) provides population and built-up layers. Visit https://ghsl.jrc.ec.europa.eu/.\n"
            "Download a small tile (e.g., a small country or region) and place it here with metadata.\n"
        ),
        "eu_copernicus": (
            "Copernicus Services Catalogue contains many datasets. Visit https://www.copernicus.eu/en/access-data/copernicus-services-catalogue.\n"
            "Download a small, relevant sample and document license and attribution.\n"
        ),
        "eotoolkit": (
            "UN-Habitat Earth Observations Toolkit: https://eotoolkit.unhabitat.org/.\n"
            "Identify a relevant resource and place a small sample or a link with documentation here.\n"
        ),
    }

    for folder, text in placeholders.items():
        folder_path = DATA_DIR / folder
        ensure_directory(folder_path)
        readme_path = folder_path / "README.txt"
        if not readme_path.exists():
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(text)


def main() -> int:
    print("Downloading sample datasets...")
    successes = 0

    if download_worldview_sample():
        successes += 1
        print("- Worldview sample downloaded")
    else:
        print("- Worldview sample skipped (download failed)")

    if download_earth_observatory_sample():
        successes += 1
        print("- Earth Observatory sample downloaded")
    else:
        print("- Earth Observatory sample skipped (download failed)")

    if download_wri_sample():
        successes += 1
        print("- WRI sample downloaded")
    else:
        print("- WRI sample skipped (no direct small CSV found; added instructions)")

    write_placeholders_for_sedac_worldpop_ghsl_copernicus_eotoolkit()
    print("- Placeholders written for SEDAC, WorldPop, GHSL, Copernicus, and EO Toolkit")

    print(f"Completed with {successes} successful downloads")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

