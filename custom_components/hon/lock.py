import logging
from typing import Any

from homeassistant.components.lock import LockEntity, LockEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback, HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pyhon.parameter.base import HonParameter
from pyhon.parameter.range import HonParameterRange

from .const import DOMAIN
from .entity import HonEntity

_LOGGER = logging.getLogger(__name__)

LOCKS: dict[str, tuple[LockEntityDescription, ...]] = {
    "AP": (
        LockEntityDescription(
            key="lockStatus",
            name="Lock Status",
            translation_key="mode",
        ),
    ),
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    entities = []
    for device in hass.data[DOMAIN][entry.unique_id]["hon"].appliances:
        for description in LOCKS.get(device.appliance_type, []):
            if (
                f"settings.{description.key}" not in device.available_settings
                or device.get(description.key) is None
            ):
                continue
            entity = HonLockEntity(hass, entry, device, description)
            entities.append(entity)

    async_add_entities(entities)


class HonLockEntity(HonEntity, LockEntity):
    entity_description: LockEntityDescription

    @property
    def is_locked(self) -> bool | None:
        """Return a boolean for the state of the lock."""
        return bool(self._device.get(self.entity_description.key, 0) == 1)

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock method."""
        setting = self._device.settings.get(f"settings.{self.entity_description.key}")
        if type(setting) == HonParameter or setting is None:
            return
        setting.value = setting.max if isinstance(setting, HonParameterRange) else 1
        self.async_write_ha_state()
        await self._device.commands["settings"].send()
        self.coordinator.async_set_updated_data({})

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock method."""
        setting = self._device.settings[f"settings.{self.entity_description.key}"]
        if type(setting) == HonParameter:
            return
        setting.value = setting.min if isinstance(setting, HonParameterRange) else 0
        self.async_write_ha_state()
        await self._device.commands["settings"].send()
        self.coordinator.async_set_updated_data({})

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and int(self._device.get("remoteCtrValid", 1)) == 1
            and self._device.connection
        )

    @callback
    def _handle_coordinator_update(self, update: bool = True) -> None:
        self._attr_is_locked = self.is_locked
        if update:
            self.async_write_ha_state()
