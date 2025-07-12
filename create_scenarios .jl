using NCDatasets
using Dates
using DataFrames
using Statistics
using DelimitedFiles

# Ouvrir le fichier NetCDF
ds = Dataset("Documents/data_merged.nc", "r")

# Extraire la variable "shww"
shww = ds["shww"][:]

# Récupérer les données comme vecteur 1D (équivalent du [i][0][0] en Python)
shww_data = [shww[i, 1, 1] for i in 1:size(shww, 1)]

# Créer la plage temporelle
start_date = DateTime("1940-01-01T00:00:00")
n_hours = length(shww_data)
date_range = start_date:Hour(1):(start_date + Hour(n_hours - 1))

# Créer un DataFrame
df = DataFrame(timestamp = date_range, values = shww_data)


# Extraire la date (sans l'heure) pour grouper par jour
df.day = Date.(df.timestamp)

# Grouper par jour et calculer la moyenne des valeurs
daily_means = combine(groupby(df, :day), :values => mean => :daily_mean)

scenarios_shww = fill(-1.0, 10, 6, 62)

for S in 1:10
    for T in 1:6
        month_list = [(T-1)*2 + 1, (T-1)*2 + 2]   
        y = 1939 + S

        subset = filter(row -> year(row.day) == y && month(row.day) in month_list, daily_means)
        shww_by_day_subset = subset.daily_mean

        l = length(shww_by_day_subset)
        scenarios_shww[S,T,1:l] = shww_by_day_subset
    end
end

function Production(shww)

    if shww == -1
        return -1
    else
        wind_speed = -1 + sqrt(1+(0.016/0.406^2)*4shww)
        return min(2000*wind_speed^3,100)
    end
end

threshold = 1.0
scenarios_h = Int.(scenarios_shww .< threshold)
scenarios_p = Production.(scenarios_shww)

for j in 1:6
    # Extraire le "slice" A[:, j, :] → une matrice 10x62
    slice_h = scenarios_h[:, j, :]
    # Sauvegarder dans un fichier, ex: "scenarios_part2.txt"
    writedlm("C:/Users/sodel/Documents/scenarios_h$(j).txt", slice_h)
        # Extraire le "slice" A[:, j, :] → une matrice 10x62
    slice_p = scenarios_p[:, j, :]
    # Sauvegarder dans un fichier, ex: "scenarios_part2.txt"
    writedlm("C:/Users/sodel/Documents/scenarios_p$(j).txt", slice_p)
end

scenarios_h_reconstructed = Array{Float64}(undef, 10, 6, 62)
scenarios_p_reconstructed = Array{Float64}(undef, 10, 6, 62)

for j in 1:6
    # Lire la matrice 10x62 depuis le fichier
    slice_h = readdlm("C:/Users/sodel/Documents/scenarios_h$(j).txt")
    # Remettre dans le bon endroit
    scenarios_h_reconstructed[:, j, :] = slice_h
    for j in 1:6
    # Lire la matrice 10x62 depuis le fichier
    slice_p = readdlm("C:/Users/sodel/Documents/scenarios_p$(j).txt")
    # Remettre dans le bon endroit
    scenarios_p_reconstructed[:, j, :] = slice_p
end
end
