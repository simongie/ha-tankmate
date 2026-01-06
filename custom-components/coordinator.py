import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class TankMateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api):
        super().__init__(
            hass,
            _LOGGER,
            name="TankMate",
            update_interval=timedelta(minutes=5),
        )
        self.api = api

    async def _async_update_data(self):
        try:
            return await self.api.async_get_data()
        except Exception as err:
            raise UpdateFailed(f"TankMate error: {err}")
