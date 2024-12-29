from typing import Optional, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback, HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pyhon.appliance import HonAppliance

from .const import DOMAIN
from .typedefs import HonEntityDescription


class HonEntity(CoordinatorEntity[DataUpdateCoordinator[dict[str, Any]]]):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        device: HonAppliance,
        description: Optional[HonEntityDescription] = None,
    ) -> None:
        self.coordinator = hass.data[DOMAIN][entry.unique_id]["coordinator"]
        super().__init__(self.coordinator)
        self._hon = hass.data[DOMAIN][entry.unique_id]["hon"]
        self._hass = hass
        self._device: HonAppliance = device

        if description is not None:
            self.entity_description = description
            self._attr_unique_id = f"{self._device.unique_id}{description.key}"
        else:
            self._attr_unique_id = self._device.unique_id
        self._handle_coordinator_update(update=False)

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._device.unique_id)},
            manufacturer=self._device.get("brand", "").capitalize(),
            name=self._device.nick_name,
            model=self._device.model_name,
            sw_version=self._device.get("fwVersion", ""),
            hw_version=f"{self._device.appliance_type}{self._device.model_id}",
            serial_number=self._device.get("serialNumber", ""),
        )

    @callback
    def _handle_coordinator_update(self, update: bool = True) -> None:
        if update:
            self.async_write_ha_state()
