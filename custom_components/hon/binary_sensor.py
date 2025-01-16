import logging
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorEntityDescription,
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback, HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import HonEntity
from .util import unique_entities

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class HonBinarySensorEntityDescription(BinarySensorEntityDescription):
    on_value: str | float = ""


BINARY_SENSORS: dict[str, tuple[HonBinarySensorEntityDescription, ...]] = {
    "WM": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Remote Control",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            icon="mdi:remote",
            translation_key="remote_control",
        ),
        HonBinarySensorEntityDescription(
            key="doorLockStatus",
            name="Door Lock",
            device_class=BinarySensorDeviceClass.LOCK,
            on_value=0,
            translation_key="door_lock",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatus",
            name="Door",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value=1,
            translation_key="door_open",
        ),
        HonBinarySensorEntityDescription(
            key="prewash",
            icon="mdi:tshirt-crew",
            name="Pre Wash",
            translation_key="prewash",
        ),
        HonBinarySensorEntityDescription(
            key="extraRinse1",
            icon="mdi:numeric-1-box-multiple-outline",
            name="Extra Rinse 1",
            translation_key="extra_rinse_1",
        ),
        HonBinarySensorEntityDescription(
            key="extraRinse2",
            icon="mdi:numeric-2-box-multiple-outline",
            name="Extra Rinse 2",
            translation_key="extra_rinse_2",
        ),
        HonBinarySensorEntityDescription(
            key="extraRinse3",
            icon="mdi:numeric-3-box-multiple-outline",
            name="Extra Rinse 3",
            translation_key="extra_rinse_3",
        ),
        HonBinarySensorEntityDescription(
            key="goodNight",
            icon="mdi:weather-night",
            name="Good Night Mode",
            translation_key="good_night",
        ),
        HonBinarySensorEntityDescription(
            key="acquaplus",
            icon="mdi:water-plus",
            name="Acqua Plus",
            translation_key="acqua_plus",
        ),
    ),
    "TD": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            translation_key="connection",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatus",
            name="Door",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value=1,
            translation_key="door_open",
        ),
        HonBinarySensorEntityDescription(
            key="anticrease",
            name="Anti-Crease",
            icon="mdi:iron",
            translation_key="anti_crease",
        ),
    ),
    "OV": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            icon="mdi:wifi",
            translation_key="connection",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.parameters.onOffStatus",
            name="On",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value=1,
            icon="mdi:power-cycle",
            translation_key="on",
        ),
    ),
    "IH": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            icon="mdi:wifi",
            translation_key="connection",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.parameters.onOffStatus",
            name="On",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value=1,
            icon="mdi:power-cycle",
            translation_key="on",
        ),
        HonBinarySensorEntityDescription(
            key="hotStatus",
            name="Hot Status",
            device_class=BinarySensorDeviceClass.HEAT,
            on_value=1,
            translation_key="still_hot",
        ),
        HonBinarySensorEntityDescription(
            key="panStatus",
            name="Pan Status",
            on_value=1,
            icon="mdi:pot-mix",
            translation_key="pan_status",
        ),
        HonBinarySensorEntityDescription(
            key="hobLockStatus",
            name="Hob Lock",
            device_class=BinarySensorDeviceClass.LOCK,
            on_value=0,
            translation_key="child_lock",
        ),
    ),
    "DW": (
        HonBinarySensorEntityDescription(
            key="saltStatus",
            name="Salt",
            device_class=BinarySensorDeviceClass.PROBLEM,
            on_value=1,
            icon="mdi:shaker-outline",
            translation_key="salt_level",
        ),
        HonBinarySensorEntityDescription(
            key="rinseAidStatus",
            name="Rinse Aid",
            device_class=BinarySensorDeviceClass.PROBLEM,
            on_value=1,
            icon="mdi:spray-bottle",
            translation_key="rinse_aid",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            translation_key="connection",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatus",
            name="Door",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value=1,
            translation_key="door_open",
        ),
    ),
    "AC": (
        HonBinarySensorEntityDescription(
            key="filterChangeStatusLocal",
            name="Filter Replacement",
            device_class=BinarySensorDeviceClass.PROBLEM,
            on_value=1,
            translation_key="filter_replacement",
        ),
        HonBinarySensorEntityDescription(
            key="ch2oCleaningStatus",
            name="Ch2O Cleaning",
            on_value=1,
        ),
    ),
    "REF": (
        HonBinarySensorEntityDescription(
            key="quickModeZ1",
            name="Super Cool",
            icon="mdi:snowflake",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value=1,
            translation_key="super_cool",
        ),
        HonBinarySensorEntityDescription(
            key="quickModeZ2",
            name="Super Freeze",
            icon="mdi:snowflake-variant",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value=1,
            translation_key="super_freeze",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatusZ1",
            name="Door1 Status Fridge",
            device_class=BinarySensorDeviceClass.DOOR,
            icon="mdi:fridge-top",
            on_value=1,
            translation_key="fridge_door",
        ),
        HonBinarySensorEntityDescription(
            key="door2StatusZ1",
            name="Door2 Status Fridge",
            icon="mdi:fridge-top",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value=1,
            translation_key="fridge_door",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatusZ2",
            name="Door1 Status Freezer",
            icon="mdi:fridge-bottom",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value=1,
            translation_key="freezer_door",
        ),
        HonBinarySensorEntityDescription(
            key="door2StatusZ2",
            name="Door2 Status Freezer",
            icon="mdi:fridge-bottom",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value=1,
            translation_key="freezer_door",
        ),
        HonBinarySensorEntityDescription(
            key="intelligenceMode",
            name="Auto-Set Mode",
            icon="mdi:thermometer-auto",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value=1,
            translation_key="auto_set",
        ),
        HonBinarySensorEntityDescription(
            key="holidayMode",
            name="Holiday Mode",
            icon="mdi:palm-tree",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value=1,
            translation_key="holiday_mode",
        ),
    ),
    "AP": (
        HonBinarySensorEntityDescription(
            key="attributes.parameters.onOffStatus",
            name="On",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value="1",
            icon="mdi:power-cycle",
            translation_key="on",
        ),
    ),
    "FRE": (
        HonBinarySensorEntityDescription(
            key="quickModeZ1",
            name="Super Cool",
            icon="mdi:snowflake",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value=1,
            translation_key="super_cool",
        ),
        HonBinarySensorEntityDescription(
            key="quickModeZ2",
            name="Super Freeze",
            icon="mdi:snowflake-variant",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value=1,
            translation_key="super_freeze",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatusZ2",
            name="Door Status",
            icon="mdi:fridge",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value=1,
            translation_key="door_open",
        ),
    ),
}

BINARY_SENSORS["WD"] = unique_entities(BINARY_SENSORS["WM"], BINARY_SENSORS["TD"])


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    entities = []
    for device in hass.data[DOMAIN][entry.unique_id]["hon"].appliances:
        for description in BINARY_SENSORS.get(device.appliance_type, []):
            if device.get(description.key) is None:
                continue
            entity = HonBinarySensorEntity(hass, entry, device, description)
            entities.append(entity)
    async_add_entities(entities)


class HonBinarySensorEntity(HonEntity, BinarySensorEntity):
    entity_description: HonBinarySensorEntityDescription

    @property
    def is_on(self) -> bool:
        return bool(
            self._device.get(self.entity_description.key, "")
            == self.entity_description.on_value
        )

    @callback
    def _handle_coordinator_update(self, update: bool = True) -> None:
        self._attr_native_value = (
            self._device.get(self.entity_description.key, "")
            == self.entity_description.on_value
        )
        if update:
            self.schedule_update_ha_state()
