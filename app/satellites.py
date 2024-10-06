import csv
from skyfield.api import EarthSatellite, load, wgs84

name = 'satellites.csv'
satellite_download_url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=csv'


def download_satellite_csv_data(max_days=7):
    if not load.exists(name) or load.days_old(name) >= max_days:
        try:
            load.download(satellite_download_url, filename=name)
            return

        except Exception as e:
            print(f"Error retrieving position: {e}")
            return None


def load_satellite_csv_data():
    with load.open('satellites.csv', mode='r') as f:
        data = list(csv.DictReader(f))

    ts = load.timescale()
    return [EarthSatellite.from_omm(ts, fields) for fields in data]


def calculate_passes(latitude, longitude, min_elevation=30, utc_offset=0, start_datetime=None, end_datetime=None):

    satellites = load_satellite_csv_data()
    location = wgs84.latlon(latitude, longitude)

    ts = load.timescale()

    if start_datetime is None:
        start_datetime = ts.now() + (utc_offset / 24)
    if end_datetime is None:
        end_datetime = start_datetime + .5/24
    event_names = 'rise above 30°', 'culminate', 'set below 30°'

    passes = []
    for sat in satellites:
        # Calcul des événements de passage des satellites
        times, events = sat.find_events(location, start_datetime, end_datetime, altitude_degrees=min_elevation)
        for ti, event in zip(times, events):
            topocentric = (sat - location).at(ti)
            altitude, azimuth, distance = topocentric.altaz()
            passes.append({
                'satellite_name': sat.name,
                'satellite_id': sat.model.satnum,
                'time': ti.utc_iso(),
                'event': event_names[event],
                'altitude': altitude,
                'azimuth': azimuth,
                'distance': int(distance.km)
            })

    return passes
