from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.entity_component import async_update_entity

DOMAIN = "gas_prices"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Gas Prices integration."""

    async def handle_refresh(call: ServiceCall):
        """Handle the manual refresh service."""
        for entity_id in hass.states.async_entity_ids(DOMAIN):
            await async_update_entity(hass, entity_id)

    hass.services.async_register(DOMAIN, "refresh", handle_refresh)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Gas Prices from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    hass.async_create_task(
        async_load_platform(hass, "sensor", DOMAIN, entry.data, entry)
    )
    return True
