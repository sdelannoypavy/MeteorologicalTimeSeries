import xarray as xr
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tensorflow_probability as tfp
import numpy as np
import pandas as pd
import tensorflow.compat.v2 as tf
import tf_keras
from tensorflow_probability import sts
import seaborn as sns
import collections
import calendar

tfd = tfp.distributions



from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

sns.set_context("notebook", font_scale=1.)
sns.set_style("whitegrid")

def plot_forecast(x, y,
                  forecast_mean, forecast_scale, forecast_samples,
                  title, x_locator=None, x_formatter=None):
    """Plot a forecast distribution against the 'true' time series."""
    colors = sns.color_palette()
    c1, c2 = colors[0], colors[1]
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 1, 1)

    num_steps = len(y)
    num_steps_forecast = forecast_mean.shape[-1]
    num_steps_train = num_steps - num_steps_forecast


    ax.plot(x, y, lw=2, color=c1, label='ground truth')

    forecast_steps = np.arange(
        x[num_steps_train],
        x[num_steps_train]+num_steps_forecast,
        dtype=x.dtype)

    ax.plot(forecast_steps, forecast_samples.T, lw=1, color=c2, alpha=0.1)

    ax.plot(forecast_steps, forecast_mean, lw=2, ls='--', color=c2,
            label='forecast')
    ax.fill_between(forecast_steps,
                    forecast_mean-2*forecast_scale,
                    forecast_mean+2*forecast_scale, color=c2, alpha=0.2)

    ymin, ymax = min(np.min(forecast_samples), np.min(y)), max(np.max(forecast_samples), np.max(y))
    yrange = ymax-ymin
    ax.set_ylim([ymin - yrange*0.1, ymax + yrange*0.1])
    ax.set_title("{}".format(title))
    ax.legend()

    if x_locator is not None:
        ax.xaxis.set_major_locator(x_locator)
        ax.xaxis.set_major_formatter(x_formatter)
        fig.autofmt_xdate()

    return fig, ax



def plot_components(dates,
                    component_means_dict,
                    component_stddevs_dict,
                    x_locator=None,
                    x_formatter=None):
    """Plot the contributions of posterior components in a single figure."""
    colors = sns.color_palette()
    c1, c2 = colors[0], colors[1]

    axes_dict = collections.OrderedDict()
    num_components = len(component_means_dict)
    fig = plt.figure(figsize=(12, 2.5 * num_components))
    for i, component_name in enumerate(component_means_dict.keys()):
        component_mean = component_means_dict[component_name]
        component_stddev = component_stddevs_dict[component_name]

        ax = fig.add_subplot(num_components,1,1+i)
        ax.plot(dates, component_mean, lw=2)
        ax.fill_between(dates,
                        component_mean-2*component_stddev,
                        component_mean+2*component_stddev,
                        color=c2, alpha=0.5)
        ax.set_title(component_name)
        if x_locator is not None:
            ax.xaxis.set_major_locator(x_locator)
            ax.xaxis.set_major_formatter(x_formatter)
        axes_dict[component_name] = ax
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig, axes_dict

def plot_one_step_predictive(dates, observed_time_series,one_step_mean, one_step_scale,x_locator=None, x_formatter=None):
    """Plot a time series against a model's one-step predictions."""

    colors = sns.color_palette()
    c1, c2 = colors[0], colors[1]

    fig=plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1,1,1)
    ax.plot(dates, observed_time_series, label="observed time series", color=c1)
    ax.plot(dates, one_step_mean, label="one-step prediction", color=c2)
    ax.fill_between(dates,
                    one_step_mean - one_step_scale,
                    one_step_mean + one_step_scale,
                    alpha=0.1, color=c2)
    ax.legend()

    if x_locator is not None:
        ax.xaxis.set_major_locator(x_locator)
        ax.xaxis.set_major_formatter(x_formatter)
        fig.autofmt_xdate()
    fig.tight_layout()
    return fig, ax

#def build_model(observed_time_series):
#    trend = sts.LocalLinearTrend(observed_time_series=observed_time_series)
#    seasonal = tfp.sts.Seasonal(
#        num_seasons=12, observed_time_series=observed_time_series)
#    model = sts.Sum([trend, seasonal], observed_time_series=observed_time_series)
#    return model




def build_model(observed_time_series):

# Générer les longueurs de mois pour les années 1940 à 1968
    years = list(range(1940, 1969))
    num_days_per_month = []

    for year in years:
        month_lengths = [calendar.monthrange(year, month)[1] for month in range(1, 13)]
        num_days_per_month.append(month_lengths)

    seasonal = tfp.sts.Seasonal(
        num_seasons=12,   
        num_steps_per_season=num_days_per_month,
        # drift_scale_prior=tfd.LogNormal(loc=-1., scale=0.1),
        # initial_effect_prior=tfd.Normal(loc=0., scale=5.),
        observed_time_series=observed_time_series)
    model = sts.Sum([seasonal], observed_time_series=observed_time_series)
    return model
