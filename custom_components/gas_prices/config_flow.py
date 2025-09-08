import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from .const import DOMAIN, DEFAULT_RADIUS, DEFAULT_FUEL, DEFAULT_TOP

CONF_RADIUS = "radius"
CONF_FUEL = "fuel"
CONF_TOP = "top"

class GasPricesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Gas Prices", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): float,
            vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): float,
            vol.Required(CONF_RADIUS, default=DEFAULT_RADIUS): int,
            vol.Required(CONF_FUEL, default=DEFAULT_FUEL): str,
            vol.Required(CONF_TOP, default=DEFAULT_TOP): int,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
