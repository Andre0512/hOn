import logging
from typing import Any

from homeassistant.components.light import (
    LightEntityDescription,
    LightEntity,
    ColorMode,
    ATTR_BRIGHTNESS,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback, HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pyhon.appliance import HonAppliance
from pyhon.parameter.range import HonParameterRange

from .const import DOMAIN
from .entity import HonEntity

_LOGGER = logging.getLogger(__name__)


LIGHTS: dict[str, tuple[LightEntityDescription, ...]] = {
    "WC": (
        LightEntityDescription(
            key="settings.lightStatus",
            name="Light",
            translation_key="light",
        ),
    ),
    "HO": (
        LightEntityDescription(
            key="settings.lightStatus",
            name="Light status",
            translation_key="light",
        ),
    ),
    "AP": (
        LightEntityDescription(
            key="settings.lightStatus",
            name="Light status",
            translation_key="light",
        ),
    ),
    "DW": (
        LightEntityDescription(
            key="settings.lightStatus",
            name="Light status",
            translation_key="light",
        ),
    ),
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    entities = []
    for device in hass.data[DOMAIN][entry.unique_id]["hon"].appliances:
        for description in LIGHTS.get(device.appliance_type, []):
            if (
                description.key not in device.available_settings
                or device.get(description.key.split(".")[-1]) is None
            ):
                continue
            entity = HonLightEntity(hass, entry, device, description)
            entities.append(entity)
    async_add_entities(entities)


class HonLightEntity(HonEntity, LightEntity):
    entity_description: LightEntityDescription

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        device: HonAppliance,
        description: LightEntityDescription,
    ) -> None:
        light = device.settings.get(description.key)
        if not isinstance(light, HonParameterRange):
            raise ValueError()
        self._light_range = (light.min, light.max)
        self._attr_supported_color_modes: set[ColorMode] = set()
        if len(light.values) == 2:
            self._attr_supported_color_modes.add(ColorMode.ONOFF)
        else:
            self._attr_supported_color_modes.add(ColorMode.BRIGHTNESS)
        self._command, self._parameter = description.key.split(".")
        super().__init__(hass, entry, device, description)
        self._handle_coordinator_update(update=False)

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return bool(self._device.get(self.entity_description.key.split(".")[-1]) > 0)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on or control the light."""
        light = self._device.settings.get(self.entity_description.key)
        if not isinstance(light, HonParameterRange):
            raise ValueError()
        if ColorMode.BRIGHTNESS in self._attr_supported_color_modes:
            percent = int(100 / 255 * kwargs.get(ATTR_BRIGHTNESS, 128))
            light.value = round(light.max / 100 * percent)
            if light.value == light.min:
                self._attr_is_on = False
            self._attr_brightness = self.brightness
        else:
            light.value = light.max
        await self._device.commands[self._command].send()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        light = self._device.settings.get(self.entity_description.key)
        if not isinstance(light, HonParameterRange):
            raise ValueError()
        light.value = light.min
        await self._device.commands[self._command].send()
        self.async_write_ha_state()

    @property
    def brightness(self) -> int | None:
        """Return the brightness of the light."""
        light = self._device.settings.get(self.entity_description.key)
        if not isinstance(light, HonParameterRange):
            raise ValueError()
        if light.value == light.min:
            return None
        return int(255 / light.max * float(light.value))

    @callback
    def _handle_coordinator_update(self, update: bool = True) -> None:
        self._attr_is_on = self.is_on
        self._attr_brightness = self.brightness
        if update:
            self.schedule_update_ha_state()

    @property
    def available(self) -> bool:
        if (entity := self._device.settings.get(self.entity_description.key)) is None:
            return False
        return super().available and len(entity.values) > 1
