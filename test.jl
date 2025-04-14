using Statistics
using Plots
using NCDatasets
using Random

Random.seed!(1234)

ds = Dataset("data/fichier0.nc", "r")




n = Int(length(y))
taille_bloc = 24 # modifier 365 en fonction de l'année
nb_blocs = floor(Int, n / taille_bloc)

daily_mean = Float64[]
daily_max = Float64[]

#Ou pourrait aussi regarder le min par jour, ou les valeurs au pas de temps 1h

for i in 1:nb_blocs
    bloc = y[(i-1)*taille_bloc + 1:i*taille_bloc]
    push!(daily_mean, mean(bloc))
    push!(daily_max, maximum(bloc))
end

mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]

nb_val = length(daily_mean)
pas = Int(round(nb_val/12)) + 1

#plot(moyennes, xticks=(1:pas:nb_val, mois), titlefontsize=8, legend=false, ylabel = "m")
plot(daily_mean, xticks=(1:pas:nb_val, mois), titlefontsize=8, legend=false, ylabel = "m")

savefig("seasonal_mean.pdf")