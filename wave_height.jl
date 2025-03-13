using Statistics
using Plots
using NCDatasets
using Random

Random.seed!(1234)

ds = Dataset("wave_height_40_49.nc", "r")

y = ds["swh"][:]



n = Int(length(y))
taille_bloc = 24 # modifier 365 en fonction de l'année
nb_blocs = floor(Int, n / taille_bloc)

daily_mean = Float64[]
# daily_max = Float64[]

#Ou pourrait aussi regarder le min par jour, ou les valeurs au pas de temps 1h

for i in 1:nb_blocs
    bloc = y[(i-1)*taille_bloc + 1:i*taille_bloc]
    push!(daily_mean, mean(bloc))
    # push!(daily_max, max(bloc))
end

log_daily_mean = log.(daily_mean)


#récupérer la moyenne en fonction des jours de l'année

idx_bissextile_years = [1, 5, 9]
for i in idx_bissextile_years
    deleteat!(daily_mean, (i-1)*365 + 60)
    deleteat!(log_daily_mean, (i-1)*365 + 60)
end


year_values = [] 
log_year_values = [] 

idx = 1

for year in 1940:1949

    new_line = daily_mean[idx:(idx + 364)]
    new_line_log = log_daily_mean[idx:(idx + 364)]
    global idx += 365

    push!(year_values, new_line)
    push!(log_year_values, new_line_log)

end

seasonal_mean = mean(year_values, dims=1)[1]
seasonal_mean_log = mean(log_year_values, dims=1)[1]


mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]

nb_val = length(seasonal_mean)
pas = Int(round(nb_val/12)) + 1

#plot(moyennes, xticks=(1:pas:nb_val, mois), titlefontsize=8, legend=false, ylabel = "m")
plot(seasonal_mean, xticks=(1:pas:nb_val, mois), titlefontsize=8, legend=false, ylabel = "m")

savefig("seasonal_mean.pdf")


seasonal_mean_duplicate = repeat(seasonal_mean, 10)
renormalized = daily_mean - seasonal_mean_duplicate

variance = var(renormalized)

println("La variance sans Box-Cox est $variance")

log_seasonal_mean_duplicate = repeat(seasonal_mean_log, 10)
renormalized_log = log_daily_mean - log_seasonal_mean_duplicate
variance_log = var(renormalized_log)

println("La variance avec Box-Cox est $variance_log")


#La variance sans Box-Cox est 0.19936569541829757
#La variance avec Box-Cox est 0.16995760951701722
# On ne fait pas de transformation Box-Cox


# on essaie de fitt
# il y a peut-être des packages qui font ça automatiquement 
# on prend le log pour éviter les valeurs négatives


lag0 = renormalized_log[2:365]
lag1 = renormalized_log[1:364]

mean_lag0 = mean(lag0)
mean_lag1 = mean(lag1)

gamma1 = sum((lag0 .- mean_lag0) .* (lag1 .- mean_lag1)) / (364)
gamma0 = sum((lag0 .- mean_lag0) .* (lag0 .- mean_lag0)) / (364)
rho1 = gamma1/gamma0

sigma = sqrt((1-rho1^2)*variance_log)


#on simule une année de la série temporelle

n = 365     

AR = [0.0 for i in 1:365]
AR[1] = randn() 

for t in 2:n
    AR[t] = rho1 * AR[t-1] + sigma*randn()  # AR(1) avec bruit blanc
end

simu = exp.(AR + seasonal_mean_log)

# Tracer la série temporelle
plot(simu, xticks=(1:pas:nb_val, mois), titlefontsize=8, legend=false, ylabel = "m")


savefig("Simulation.pdf")