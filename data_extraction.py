import os 

os.environ['HTTP_PROXY'] = 'http://SD55089T:Pruneauprun01r1@163.104.40.34:3128'
os.environ['HTTPS_PROXY'] = 'http://SD55089T:Pruneauprun01r1@163.104.40.34:3128'

# La hauteur des vagues est plus significatives pour les conditions de maintenance
# Pour les postes flottés, les contrats demandent que la plateforme soit accessible jusqu'à 1.5m - 2m de hauteur des vagues
# On regarde Significant height of combined wind waves and swell
# Swell = grands régimes de vagues // wind waves 

import cdsapi

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "significant_height_of_combined_wind_waves_and_swell"
    ],
    "year": ["2015", "2016", "2017",
        "2018", "2019", "2020",
        "2021", "2022", "2023",
        "2024", "2025"
    ],
    "month": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12"
    ],
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16", "17", "18",
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"
    ],
    "time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ],
    "data_format": "netcdf",
    "download_format": "zip",
    "area": [-2.56, 49, -2.5605, 49.0005]
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
