# Gas Prices (Unofficial) – Home Assistant Integration

⚠️ **Disclaimer**  
This is a **temporary integration for personal use only**.  
It is not an official or stable Home Assistant integration, and it may break at any time.  
Data is fetched from the **unofficial Waze fuel API**, which could change without notice.  

---

## Features
- Configurable via the Home Assistant UI (Config Flow):
  - Latitude & Longitude
  - Search radius (km)
  - Fuel type (e.g. 95, 98, Diesel)
  - Number of top stations to display
- Entities created:
  - `sensor.best_gas_price` → Cheapest station (with name, coords, brand, etc.)
  - `sensor.top_gas_prices` → List of top N stations (as attributes)
  - `sensor.gas_prices_last_update` → Last refresh timestamp

---

## Installation (via HACS)
1. Add this repo as a **custom repository** in HACS:  
   - HACS → Integrations → Custom Repositories → Paste repo URL  
   - Category: Integration
2. Install → Restart Home Assistant
3. Go to **Settings → Devices & Services → Add Integration → Gas Prices**
4. Configure your location, radius, fuel type, and how many stations to show

---

## Example Output

`sensor.best_gas_price`:
```yaml
state: 1.74
attributes:
  station: "Avia Zürich"
  brand: "Avia"
  price: 1.74
  lat: 47.378
  lon: 8.540
