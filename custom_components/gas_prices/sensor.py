from homeassistant.components.sensor import SensorEntity
from datetime import datetime
from .const import DOMAIN
import requests
import logging


_LOGGER = logging.getLogger(__name__)

def fetch_gas_prices(lat, lon, radius, fuel):
    url = f"https://www.waze.com/live-map/api/fuel_prices?lat={lat}&lon={lon}&radius={radius}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        stations = []
        for station in data.get("stations", []):
            prices = station.get("fuel_prices", [])
            for p in prices:
                if p.get("fuel_type") == fuel:
                    stations.append({
                        "station": station.get("name"),
                        "brand": station.get("brand"),
                        "price": p.get("price"),
                        "lat": station.get("lat"),
                        "lon": station.get("lon")
                    })
        return stations

    except Exception as e:
        _LOGGER.error("Failed to fetch gas prices: %s", e)
        return []

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    if discovery_info is None:
        return

    lat = discovery_info["latitude"]
    lon = discovery_info["longitude"]
    radius = discovery_info["radius"]
    fuel = discovery_info["fuel"]
    top_n = discovery_info["top"]

    add_entities([
        GasPriceBestSensor(lat, lon, radius, fuel),
        GasPriceListSensor(lat, lon, radius, fuel, top_n),
        GasPriceUpdateSensor()
    ])

class GasPriceBestSensor(SensorEntity):
    def __init__(self, lat, lon, radius, fuel):
        self._attr_name = "Best Gas Price"
        self._state = None
        self._attrs = {}
        self._lat = lat
        self._lon = lon
        self._radius = radius
        self._fuel = fuel

    def update(self):
        stations = fetch_gas_prices(self._lat, self._lon, self._radius, self._fuel)
        best = min(stations, key=lambda x: x["price"])
        self._state = best["price"]
        self._attrs = best

    @property
    def native_value(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attrs

class GasPriceListSensor(SensorEntity):
    def __init__(self, lat, lon, radius, fuel, top_n):
        self._attr_name = "Top Gas Prices"
        self._state = None
        self._attrs = {}
        self._lat = lat
        self._lon = lon
        self._radius = radius
        self._fuel = fuel
        self._top_n = top_n

    def update(self):
        stations = fetch_gas_prices(self._lat, self._lon, self._radius, self._fuel)
        sorted_stations = sorted(stations, key=lambda x: x["price"])
        top_list = sorted_stations[:self._top_n]
        self._state = top_list[0]["price"] if top_list else None
        self._attrs = {"stations": top_list}

    @property
    def native_value(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attrs

class GasPriceUpdateSensor(SensorEntity):
    def __init__(self):
        self._attr_name = "Gas Prices Last Update"
        self._state = None

    def update(self):
        self._state = datetime.now().isoformat()

    @property
    def native_value(self):
        return self._state
