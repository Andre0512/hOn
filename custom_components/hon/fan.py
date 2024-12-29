import logging
import math
from typing import Any

from homeassistant.components.fan import (
    FanEntityDescription,
    FanEntity,
    FanEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback, HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.percentage import (
    percentage_to_ranged_value,
    ranged_value_to_percentage,
)
from pyhon.appliance import HonAppliance
from pyhon.parameter.range import HonParameterRange

from .const import DOMAIN
from .entity import HonEntity

_LOGGER = logging.getLogger(__name__)


FANS: dict[str, tuple[FanEntityDescription, ...]] = {
    "HO": (
        FanEntityDescription(
            key="settings.windSpeed",
            name="Wind Speed",
            translation_key="air_extraction",
        ),
    ),
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    entities = []
    for device in hass.data[DOMAIN][entry.unique_id]["hon"].appliances:
        for description in FANS.get(device.appliance_type, []):
            if (
                description.key not in device.available_settings
                or device.get(description.key.split(".")[-1]) is None
            ):
                continue
            entity = HonFanEntity(hass, entry, device, description)
            entities.append(entity)
    async_add_entities(entities)


class HonFanEntity(HonEntity, FanEntity):
    entity_description: FanEntityDescription

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        device: HonAppliance,
        description: FanEntityDescription,
    ) -> None:
        self._attr_supported_features = FanEntityFeature.SET_SPEED
        self._wind_speed: HonParameterRange
        self._speed_range: tuple[int, int]
        self._command, self._parameter = description.key.split(".")

        super().__init__(hass, entry, device, description)
        self._handle_coordinator_update(update=False)

    @property
    def percentage(self) -> int | None:
        """Return the current speed."""
        value = self._device.get(self._parameter, 0)
        return ranged_value_to_percentage(self._speed_range, value)

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return len(self._wind_speed.values[1:])

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        mode = math.ceil(percentage_to_ranged_value(self._speed_range, percentage))
        self._device.settings[self.entity_description.key].value = mode
        await self._device.commands[self._command].send()
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool | None:
        """Return true if device is on."""
        if self.percentage is None:
            return False
        mode = math.ceil(percentage_to_ranged_value(self._speed_range, self.percentage))
        return bool(mode > self._wind_speed.min)

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn the entity on."""
        if percentage is None:
            percentage = ranged_value_to_percentage(
                self._speed_range, int(self._wind_speed.values[1])
            )
        await self.async_set_percentage(percentage)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self._device.settings[self.entity_description.key].value = 0
        await self._device.commands[self._command].send()
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self, update: bool = True) -> None:
        wind_speed = self._device.settings.get(self.entity_description.key)
        if isinstance(wind_speed, HonParameterRange) and len(wind_speed.values) > 1:
            self._wind_speed = wind_speed
            self._speed_range = (
                int(self._wind_speed.values[1]),
                int(self._wind_speed.values[-1]),
            )
            self._attr_percentage = self.percentage
        if update:
            self.schedule_update_ha_state()

    @property
    def available(self) -> bool:
        return super().available and len(self._wind_speed.values) > 1
