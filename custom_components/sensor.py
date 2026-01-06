from __future__ import annotations

from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.util import dt as dt_util

from .const import DOMAIN


SENSOR_MAP = {
    "currentLevel": {
        "name": "Water Height",
        "unit": "m",
        "device_class": "distance",
    },
    "currentVolume": {
        "name": "Current Volume (TankMate)",
        "unit": "L",
        "device_class": "volume_storage",
    },
    "currentPercent": {
        "name": "Percent Full (TankMate)",
        "unit": "%",
    },
    "maxVolume": {
        "name": "Max Volume",
        "unit": "L",
        "device_class": "volume_storage",
    },
    "maximumHeight": {
        "name": "Maximum Height",
        "unit": "m",
        "device_class": "distance",
    },
    "outletHeight": {
        "name": "Outlet Height",
        "unit": "m",
        "device_class": "distance",
    },
    "overflowHeight": {
        "name": "Overflow Height",
        "unit": "m",
        "device_class": "distance",
    },
    "tankArea": {
        "name": "Tank Area",
        "unit": "m²",
    },
    "tankName": {
        "name": "Tank Name",
    },
    "network": {
        "name": "Network",
    },
    "lastReading": {
        "name": "Last Reading",
        "device_class": "timestamp",
    },
    "batVoltage": {
        "name": "Battery Voltage",
        "unit": "V",
        "device_class": "battery",
        "scale": 0.001,
    },
}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[TankMateSensor] = []

    for device_id, tank in coordinator.data.items():
        for key, meta in SENSOR_MAP.items():
            if key not in tank:
                continue

            entities.append(
                TankMateSensor(
                    coordinator=coordinator,
                    entry_id=entry.entry_id,
                    device_id=device_id,
                    key=key,
                    meta=meta,
                )
            )

    async_add_entities(entities)


class TankMateSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id, device_id, key, meta):
        super().__init__(coordinator)

        self._device_id = device_id
        self._key = key
        self._meta = meta

        tank = coordinator.data.get(device_id, {})
        tank_name = tank.get("tankName", device_id)

        self._attr_name = f"{tank_name} {meta['name']}"
        self._attr_unique_id = f"{entry_id}_{device_id}_{key}"

        self._attr_unit_of_measurement = meta.get("unit")
        self._attr_device_class = meta.get("device_class")

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=tank_name,
            manufacturer="TankMate",
            model="Tank Sensor",
        )

    @property
    def native_value(self):
        value = self.coordinator.data[self._device_id].get(self._key)

        if value is None:
            return None

        # Battery scaling (mV → V)
        if "scale" in self._meta:
            try:
                return round(value * self._meta["scale"], 2)
            except Exception:
                return None

        # Timestamp handling (this fixes "Unavailable")
        if self._meta.get("device_class") == "timestamp":
            try:
                # Epoch seconds or milliseconds
                if isinstance(value, (int, float)):
                    if value > 1e12:  # ms
                        return dt_util.utc_from_timestamp(value / 1000)
                    return dt_util.utc_from_timestamp(value)

                # ISO or parseable string
                if isinstance(value, str):
                    parsed = dt_util.parse_datetime(value)
                    if parsed:
                        return parsed

            except Exception:
                return None

        return value
