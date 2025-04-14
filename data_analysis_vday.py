from data_analysis_functions import *

os.chdir("/home/delannoypavysol/Documents/time_series_analysis")

ds = xr.open_dataset("data_merged.nc")
shww = ds["shww"].values.tolist()
shww_data = [shww[i][0][0] for i in range(len(shww))]

# tous les mois ne font pas 31j

#for i in range(744, len(shww_data)+1, 744):
#    shww_by_month.append(sum(shww_data[i-744:i]) / 744)

start_date = "1940-01-01 00:00:00"
n_hours = len(shww_data)
date_range = pd.date_range(start=start_date, periods=n_hours, freq='H')

df = pd.DataFrame({'values': shww_data}, index=date_range)

# Calcul des moyennes mensuelles
dayly_means = df.resample('D').mean()

# Extraction du vecteur des moyennes
shww_by_day = dayly_means['values'].values
shww_by_day = np.log(shww_by_day )

num_forecast_steps = 365 #orcast final one year
shww_by_day_training_data = shww_by_day[:-num_forecast_steps]

shww_dates = np.arange("1940-01", "1969-01", dtype="datetime64[D]")
shww_loc = mdates.YearLocator(3)
shww_fmt = mdates.DateFormatter('%Y')

model = build_model(shww_by_day)

# Build the variational surrogate posteriors `qs`.
variational_posteriors = tfp.sts.build_factored_surrogate_posterior(
    model=model)
     

#@title Minimize the variational loss.

# Allow external control of optimization to reduce test runtimes.
num_variational_steps = 200 # @param { isTemplate: true}
num_variational_steps = int(num_variational_steps)

# Build and optimize the variational loss function.
elbo_loss_curve = tfp.vi.fit_surrogate_posterior(
    target_log_prob_fn=model.joint_distribution(
        observed_time_series=shww_by_day).log_prob,
    surrogate_posterior=variational_posteriors,
    optimizer=tf_keras.optimizers.Adam(learning_rate=0.1),
    num_steps=num_variational_steps,
    jit_compile=True)

plt.plot(elbo_loss_curve)
plt.show()

# Draw samples from the variational posterior.
q_samples = variational_posteriors.sample(50)

print("Inferred parameters:")
for param in model.parameters:
  print("{}: {} +- {}".format(param.name,
                              np.mean(q_samples[param.name], axis=0),
                              np.std(q_samples[param.name], axis=0)))

shww_forecast_dist = tfp.sts.forecast(
    model,
    observed_time_series=shww_by_day,
    parameter_samples=q_samples,
    num_steps_forecast=num_forecast_steps)



num_samples=10

shww_forecast_mean, shww_forecast_scale, shww_forecast_samples = (
    shww_forecast_dist.mean().numpy()[..., 0],
    shww_forecast_dist.stddev().numpy()[..., 0],
    shww_forecast_dist.sample(num_samples).numpy()[..., 0])


fig, ax = plot_forecast(
    shww_dates, shww_by_day[0:len(shww_dates)],
    shww_forecast_mean[0:len(shww_dates)], shww_forecast_scale[0:len(shww_dates)], shww_forecast_samples[0:len(shww_dates)],
    x_locator=shww_loc,
    x_formatter=shww_fmt,
    title="shww forecast")
ax.axvline(shww_dates[-num_forecast_steps], linestyle="--")
ax.legend(loc="upper left")
ax.set_ylabel("shww")
ax.set_xlabel("Year")
fig.autofmt_xdate()

fig.savefig("shww_forecast_day.png")


columns = [f"t+{i+1}" for i in range(shww_forecast_samples.shape[1])]
df = pd.DataFrame(np.exp(shww_forecast_samples), columns=columns)
df.to_csv("shww_forecast_samples.csv", index=False)
