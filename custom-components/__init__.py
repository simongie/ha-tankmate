from .const import DOMAIN, PLATFORMS
from .api import TankMateApi
from .coordinator import TankMateCoordinator

async def async_setup_entry(hass, entry):
    api = TankMateApi(
        entry.data["api_key"],
        entry.data["uid"],
    )

    coordinator = TankMateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass, entry):
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
