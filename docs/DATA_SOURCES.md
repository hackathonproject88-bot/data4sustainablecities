## Data Sources and Samples

This repository integrates small, redistributable samples and placeholders from major Earth observation sources relevant to sustainable cities. For full-resolution datasets, follow provider links and terms.

- **NASA Earthdata Worldview (GIBS)**
  - Sample: `data/worldview/worldview_truecolor_2020-01-01.png`
  - Metadata: `data/worldview/worldview_truecolor_2020-01-01.json`
  - Links: homepage [`https://worldview.earthdata.nasa.gov/`](https://worldview.earthdata.nasa.gov/), docs [`https://earthdata.nasa.gov/data/gibs/overview`](https://earthdata.nasa.gov/data/gibs/overview)

- **NASA Earth Observatory**
  - Sample image: `data/earth_observatory/sample_earth_observatory.jpg`
  - Note: For usage, see NASA Earth Observatory guidelines.

- **WRI Data Explorer**
  - Placeholder: `data/wri/README.txt` (add a small CSV manually from [`https://data.wri.org/`](https://data.wri.org/))

- **NASA SEDAC**
  - Placeholder: `data/sedac/README.txt` (login may be required: [`https://sedac.ciesin.columbia.edu/`](https://sedac.ciesin.columbia.edu/))

- **EU Copernicus GHSL**
  - Placeholder: `data/ghsl/README.txt` (browse tiles at [`https://ghsl.jrc.ec.europa.eu/`](https://ghsl.jrc.ec.europa.eu/))

- **WorldPop**
  - Placeholder: `data/worldpop/README.txt` (download small country raster: [`https://www.worldpop.org/`](https://www.worldpop.org/))

- **EU Copernicus Services Catalogue**
  - Placeholder: `data/eu_copernicus/README.txt` (search datasets: [`https://www.copernicus.eu/en/access-data/copernicus-services-catalogue`](https://www.copernicus.eu/en/access-data/copernicus-services-catalogue))

- **Earth Observations Toolkit**
  - Placeholder: `data/eotoolkit/README.txt` (browse resources: [`https://eotoolkit.unhabitat.org/`](https://eotoolkit.unhabitat.org/))

### Usage

Run the sample downloader (requires Python 3 and `requests`):

```bash
python3 scripts/download_samples.py
```

This will fetch small samples where possible and write placeholders with instructions for the rest.

### Notes on Licensing

Respect each provider's terms of use and attribution requirements. Do not commit large datasets to git; prefer using external storage or Git LFS when necessary.

