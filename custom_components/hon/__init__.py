import logging
from datetime import timedelta
from pathlib import Path
from typing import Any

import voluptuous as vol  # type: ignore[import-untyped]

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv, aiohttp_client
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pyhon import Hon

from .const import DOMAIN, PLATFORMS, MOBILE_ID, CONF_REFRESH_TOKEN

_LOGGER = logging.getLogger(__name__)

HON_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema(vol.All(cv.ensure_list, [HON_SCHEMA]))},
    extra=vol.ALLOW_EXTRA,
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hon from a config entry."""
    session = aiohttp_client.async_get_clientsession(hass)

    try:
        # Initialize Hon instance in executor
        def init_hon():
            """Initialize Hon instance."""
            return Hon(
                email=entry.data[CONF_EMAIL],
                password=entry.data[CONF_PASSWORD],
                mobile_id=MOBILE_ID,
                session=session,
                test_data_path=Path(hass.config.config_dir),
                refresh_token=entry.data.get(CONF_REFRESH_TOKEN, ""),
            )

        # Create Hon instance in executor
        hon = await hass.async_add_executor_job(init_hon)
        # Create and initialize
        hon = await hon.create()

    except Exception as exc:
        _LOGGER.error("Error creating Hon instance: %s", exc)
        raise

    async def async_update_data() -> dict[str, Any]:
        """Fetch data from API."""
        try:
            for appliance in hon.appliances:
                await appliance.update()
            return {"last_update": hon.api.auth.refresh_token}
        except Exception as exc:
            _LOGGER.error("Error updating Hon data: %s", exc)
            raise

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=60),
    )

    def _handle_mqtt_update(_: Any) -> None:
        """Handle MQTT updates."""
        try:
            coordinator.async_set_updated_data({"last_update": hon.api.auth.refresh_token})
        except Exception as exc:
            _LOGGER.error("Error handling MQTT update: %s", exc)

    def handle_update(msg: Any) -> None:
        """Handle updates from MQTT subscription in a thread-safe way."""
        try:
            hass.loop.call_soon_threadsafe(_handle_mqtt_update, msg)
        except Exception as exc:
            _LOGGER.error("Error scheduling MQTT update: %s", exc)

    # Subscribe to MQTT updates with error handling
    try:
        hon.subscribe_updates(handle_update)
    except Exception as exc:
        _LOGGER.error("Error subscribing to MQTT updates: %s", exc)

    # Initial data fetch
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as exc:
        _LOGGER.error("Error during initial refresh: %s", exc)
        raise

    # Save the new refresh token
    hass.config_entries.async_update_entry(
        entry, data={**entry.data, CONF_REFRESH_TOKEN: hon.api.auth.refresh_token}
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.unique_id] = {"hon": hon, "coordinator": coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    try:
        hon = hass.data[DOMAIN][entry.unique_id]["hon"]

        # Store refresh token
        refresh_token = hon.api.auth.refresh_token

        # Unsubscribe from updates
        try:
            hon.subscribe_updates(None)  # Remove subscription
        except Exception as exc:
            _LOGGER.warning("Error unsubscribing from updates: %s", exc)

        # Update entry with latest refresh token
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, CONF_REFRESH_TOKEN: refresh_token}
        )

        # Unload platforms
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
        if unload_ok:
            hass.data[DOMAIN].pop(entry.unique_id)

        return unload_ok
    except Exception as exc:
        _LOGGER.error("Error unloading entry: %s", exc)
        return False
