from multiprocessing.spawn import prepare
import string
import pandas as pd

def toInt(time: string) -> float:
    time = time.split(":")
    return float(time[0]) + float(time[1].split(".")[0])/60

def separate(df, ids):
    distinct = []
    for id in ids:
        distinct.append(df.loc[df['id'] == id])
    return distinct

def replace_timestamp(df):
    df['timestamp']=df['timestamp'].map(toInt)


def plot_buses(buses):
    ax = buses[0].plot(x='timestamp', y='value', xlabel="hour", ylabel="amount of people in a bus", legend=False)
    for bus in buses[1:-1]:
        ax = bus.plot(ax=ax, x='timestamp', y='value', legend=False)
    buses[-1].plot(ax=ax, x='timestamp', y='value', legend=False)

def prepare_data(df, ids):
    stops = separate(df, ids)
    for stop in stops:
        replace_timestamp(stop)
    stops = [stop for stop in stops if len(stop) > 2]
    stops = [stop.sort_values(by=['timestamp']) for stop in stops]
    return stops

def plot_stops(buses, stops_ids):
    for ind, bus in enumerate(buses):
        bus.rename(columns = {'value': stops_ids[ind]}, inplace = True)
    ax = buses[0].plot(x='timestamp', y=stops_ids[0], xlabel="hour", ylabel="amount of people on a bus stop")
    for ind, bus in enumerate(buses[1:-1]):
        ax = bus.plot(ax=ax, x='timestamp', y=stops_ids[ind + 1] )
    buses[-1].plot(ax=ax, x='timestamp', y=stops_ids[-1], )