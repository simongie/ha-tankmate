import aiohttp
import async_timeout

class TankMateApi:
    def __init__(self, api_key, uid):
        self._api_key = api_key
        self._uid = uid

    async def async_get_data(self):
        headers = {
            "accept": "application/json",
            "api-key": self._api_key,
        }

        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(15):
                async with session.get(
                    f"https://api.tankmate.app/status/?uid={self._uid}",
                    headers=headers,
                ) as resp:
                    resp.raise_for_status()
                    return await resp.json()
