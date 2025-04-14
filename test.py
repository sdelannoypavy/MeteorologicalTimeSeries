from data_analysis_functions import *

os.chdir("/home/delannoypavysol/Documents/time_series_analysis")

ds = xr.open_dataset("data_merged.nc")
shww = ds["shww"].values.tolist()
shww_data = [shww[i][0][0] for i in range(len(shww))]

shww_by_month = []

for i in range(744, len(shww_data)+1, 744):
    shww_by_month.append(sum(shww_data[i-744:i]) / 744)