import logging
from pathlib import Path

from homeassistant.components import persistent_notification
from homeassistant.components.button import ButtonEntityDescription, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from pyhon.appliance import HonAppliance

from .const import DOMAIN
from .entity import HonEntity
from .typedefs import HonButtonType

_LOGGER = logging.getLogger(__name__)

BUTTONS: dict[str, tuple[ButtonEntityDescription, ...]] = {
    "IH": (
        ButtonEntityDescription(
            key="startProgram",
            name="Start Program",
            icon="mdi:pot-steam",
            translation_key="induction_hob",
        ),
    ),
    "REF": (
        ButtonEntityDescription(
            key="startProgram",
            name="Program Start",
            icon="mdi:play",
            translation_key="start_program",
        ),
        ButtonEntityDescription(
            key="stopProgram",
            name="Program Stop",
            icon="mdi:stop",
            translation_key="stop_program",
        ),
    ),
    "FRE": (
        ButtonEntityDescription(
            key="startProgram",
            name="Program Start",
            icon="mdi:play",
            translation_key="start_program",
        ),
        ButtonEntityDescription(
            key="stopProgram",
            name="Program Stop",
            icon="mdi:stop",
            translation_key="stop_program",
        ),
    ),
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    entities: list[HonButtonType] = []
    for device in hass.data[DOMAIN][entry.unique_id]["hon"].appliances:
        for description in BUTTONS.get(device.appliance_type, []):
            if not device.commands.get(description.key):
                continue
            entity = HonButtonEntity(hass, entry, device, description)
            entities.append(entity)
        entities.append(HonDeviceInfo(hass, entry, device))
        entities.append(HonDataArchive(hass, entry, device))
    async_add_entities(entities)


class HonButtonEntity(HonEntity, ButtonEntity):
    entity_description: ButtonEntityDescription

    async def async_press(self) -> None:
        await self._device.commands[self.entity_description.key].send()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and int(self._device.get("remoteCtrValid", "1")) == 1
            and self._device.connection
        )


class HonDeviceInfo(HonEntity, ButtonEntity):
    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, device: HonAppliance
    ) -> None:
        super().__init__(hass, entry, device)

        self._attr_unique_id = f"{super().unique_id}_show_device_info"
        self._attr_icon = "mdi:information"
        self._attr_name = "Show Device Info"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_entity_registry_enabled_default = False

    async def async_press(self) -> None:
        title = f"{self._device.nick_name} Device Info"
        persistent_notification.create(
            self._hass, f"````\n```\n{self._device.diagnose}\n```\n````", title
        )
        _LOGGER.info(self._device.diagnose.replace(" ", "\u200B "))


class HonDataArchive(HonEntity, ButtonEntity):
    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, device: HonAppliance
    ) -> None:
        super().__init__(hass, entry, device)

        self._attr_unique_id = f"{super().unique_id}_create_data_archive"
        self._attr_icon = "mdi:archive-arrow-down"
        self._attr_name = "Create Data Archive"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_entity_registry_enabled_default = False

    async def async_press(self) -> None:
        if (config_dir := self._hass.config.config_dir) is None:
            raise ValueError("Missing Config Dir")
        path = Path(config_dir) / "www"
        data = await self._device.data_archive(path)
        title = f"{self._device.nick_name} Data Archive"
        text = (
            f'<a href="/local/{data}" target="_blank">{data}</a> <br/><br/> '
            f"Use this data for [GitHub Issues of Haier hOn](https://github.com/Andre0512/hon).<br/>"
            f"Or add it to the [hon-test-data collection](https://github.com/Andre0512/hon-test-data)."
        )
        persistent_notification.create(self._hass, text, title)
