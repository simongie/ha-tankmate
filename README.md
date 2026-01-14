# ha-tankmate
Custom integration for Tankmate

# TankMate Home Assistant Integration

A custom Home Assistant integration for TankMate water tank sensors.

## Features
- Automatic tank discovery
- Battery voltage, volume, height, network, timestamps
- Proper Home Assistant devices & entities
- UI-based configuration (no YAML)
- One API call for all tanks

## Installation (HACS)
*Get your API details here: https://tankmate.gitbook.io/tankmate/app-user-guides/tankmate-api

1. Install HACS if you haven’t already
2. HACS → Integrations → Custom repositories
3. Add this repository:
https://github.com/simongie/ha-tankmate

4. Category: Integration
5. Install “TankMate”
6. Restart Home Assistant
7. Settings → Devices & Services → Add Integration → TankMate

## Configuration
You will need:
- TankMate API key
- TankMate UID

These are entered during setup.

## Entities
Each tank appears as a device with sensors including:
- Current Volume
- Percent Full
- Water Height
- Battery Voltage
- Network
- Last Reading

## Support
Please open an issue on GitHub for bugs or feature requests.
