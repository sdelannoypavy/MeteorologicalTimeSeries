import os 

os.environ['HTTP_PROXY'] = 'http://SD55089T:Pruneauprun01r1@163.104.40.34:3128'
os.environ['HTTPS_PROXY'] = 'http://SD55089T:Pruneauprun01r1@163.104.40.34:3128'

# Le paramètre significatif pour les conditions de maintenance est wind weight height
# Pour les postes flottés, les contrats demandent que la plateforme soit accessible jusqu'à Hs = 1.5m
# Pour Saint Nazaire, l'exigence a été baissée à 1m car tout le monde étatit alade à 1m
# Un seuil de Hs (hauteur significative) correspond à un seuil de winfd speed
# On regarde Significant height of combined wind waves and swell
# Swell = grands régimes de vagues influencés par la gravité = swell // wind waves 

import cdsapi

# la lattitude et la longitude ont une résolution 0.5, donc poue avoir une seule donnée il faut un pas de 0.4

year_list = [["2022"], ["2023"], ["2024"]]

for i in range(len(year_list)):


    dataset = "reanalysis-era5-single-levels"
    request = {
        "product_type": ["reanalysis"],
        "year": year_list[i],
        "month": [
            "01"
        ],
        "day": [
            "01"
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
        "download_format": "unarchived",
        "variable": ["significant_height_of_wind_waves"],
        "area": [49.4, -2.56, 49, -2.16]
    }

    target = f'data/fichier{i}.nc'

    client = cdsapi.Client()
    client.retrieve(dataset, request, target)
