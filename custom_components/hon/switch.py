import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components.switch import SwitchEntityDescription, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback, HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pyhon.parameter.base import HonParameter
from pyhon.parameter.range import HonParameterRange

from .const import DOMAIN
from .entity import HonEntity
from .util import unique_entities

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class HonControlSwitchEntityDescription(SwitchEntityDescription):
    turn_on_key: str = ""
    turn_off_key: str = ""


@dataclass(frozen=True)
class HonSwitchEntityDescription(SwitchEntityDescription):
    pass


@dataclass(frozen=True)
class HonConfigSwitchEntityDescription(SwitchEntityDescription):
    entity_category: EntityCategory = EntityCategory.CONFIG


SWITCHES: dict[str, tuple[SwitchEntityDescription, ...]] = {
    "WM": (
        HonControlSwitchEntityDescription(
            key="active",
            name="Washing Machine",
            icon="mdi:washing-machine",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
            translation_key="washing_machine",
        ),
        HonControlSwitchEntityDescription(
            key="pause",
            name="Pause Washing Machine",
            icon="mdi:pause",
            turn_on_key="pauseProgram",
            turn_off_key="resumeProgram",
            translation_key="pause",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.delayStatus",
            name="Delay Status",
            icon="mdi:timer-check",
            translation_key="delay_time",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.haier_SoakPrewashSelection",
            name="Soak Prewash Selection",
            icon="mdi:tshirt-crew",
            translation_key="prewash",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.prewash",
            name="Prewash",
            icon="mdi:tshirt-crew",
            translation_key="prewash",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.permanentPressStatus",
            name="Keep Fresh",
            icon="mdi:refresh-circle",
            translation_key="keep_fresh",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.autoSoftenerStatus",
            name="Auto Dose Softener",
            icon="mdi:teddy-bear",
            translation_key="auto_dose_softener",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.autoDetergentStatus",
            name="Auto Dose Detergent",
            icon="mdi:cup",
            translation_key="auto_dose_detergent",
        ),
        HonSwitchEntityDescription(
            key="autoSoftenerStatus",
            name="Auto Dose Softener",
            icon="mdi:teddy-bear",
            translation_key="auto_dose_softener",
        ),
        HonSwitchEntityDescription(
            key="autoDetergentStatus",
            name="Auto Dose Detergent",
            icon="mdi:cup",
            translation_key="auto_dose_detergent",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.acquaplus",
            name="Acqua Plus",
            icon="mdi:water-plus",
            translation_key="acqua_plus",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.extraRinse1",
            name="Extra Rinse 1",
            icon="mdi:numeric-1-box-multiple-outline",
            translation_key="extra_rinse_1",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.extraRinse2",
            name="Extra Rinse 2",
            icon="mdi:numeric-2-box-multiple-outline",
            translation_key="extra_rinse_2",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.extraRinse3",
            name="Extra Rinse 3",
            icon="mdi:numeric-3-box-multiple-outline",
            translation_key="extra_rinse_3",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.goodNight",
            name="Good Night",
            icon="mdi:weather-night",
            translation_key="good_night",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.hygiene",
            name="Hygiene",
            icon="mdi:lotion-plus",
            translation_key="hygiene",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.anticrease",
            name="Anti-Crease",
            icon="mdi:iron",
            translation_key="anti_crease",
        ),
    ),
    "TD": (
        HonControlSwitchEntityDescription(
            key="active",
            name="Tumble Dryer",
            icon="mdi:tumble-dryer",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
            translation_key="tumble_dryer",
        ),
        HonControlSwitchEntityDescription(
            key="pause",
            name="Pause Tumble Dryer",
            icon="mdi:pause",
            turn_on_key="pauseProgram",
            turn_off_key="resumeProgram",
            translation_key="pause",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.sterilizationStatus",
            name="Sterilization",
            icon="mdi:lotion-plus",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.tumblingStatus",
            name="Tumbling",
            icon="mdi:refresh-circle",
            translation_key="keep_fresh",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.antiCreaseTime",
            name="Anti-Crease",
            icon="mdi:iron",
            translation_key="anti_crease",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.anticrease",
            name="Anti-Crease",
            icon="mdi:iron",
            translation_key="anti_crease",
        ),
    ),
    "OV": (
        HonControlSwitchEntityDescription(
            key="active",
            name="Oven",
            icon="mdi:toaster-oven",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
            translation_key="oven",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.preheatStatus",
            name="Preheat",
            icon="mdi:thermometer-chevron-up",
            translation_key="preheat",
        ),
    ),
    "WD": (
        HonControlSwitchEntityDescription(
            key="active",
            name="Washer Dryer",
            icon="mdi:washing-machine",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
            translation_key="washer_dryer",
        ),
        HonControlSwitchEntityDescription(
            key="pause",
            name="Pause Washer Dryer",
            icon="mdi:pause",
            turn_on_key="pauseProgram",
            turn_off_key="resumeProgram",
            translation_key="pause",
        ),
    ),
    "DW": (
        HonControlSwitchEntityDescription(
            key="active",
            name="Dish Washer",
            icon="mdi:dishwasher",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
            translation_key="dish_washer",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.extraDry",
            name="Extra Dry",
            icon="mdi:hair-dryer",
            translation_key="extra_dry",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.halfLoad",
            name="Half Load",
            icon="mdi:fraction-one-half",
            translation_key="half_load",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.openDoor",
            name="Open Door",
            icon="mdi:door-open",
            translation_key="open_door",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.threeInOne",
            name="Three in One",
            icon="mdi:numeric-3-box-outline",
            translation_key="three_in_one",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.ecoExpress",
            name="Eco Express",
            icon="mdi:sprout",
            translation_key="eco",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.addDish",
            name="Add Dish",
            icon="mdi:silverware-fork-knife",
            translation_key="add_dish",
        ),
        HonSwitchEntityDescription(
            key="buzzerDisabled",
            name="Buzzer Disabled",
            icon="mdi:volume-off",
            translation_key="buzzer",
        ),
        HonConfigSwitchEntityDescription(
            key="startProgram.tabStatus",
            name="Tab Status",
            icon="mdi:silverware-clean",
            # translation_key="buzzer",
        ),
    ),
    "AC": (
        HonSwitchEntityDescription(
            key="10degreeHeatingStatus",
            name="10° Heating",
            icon="mdi:heat-wave",
            translation_key="10_degree_heating",
        ),
        HonSwitchEntityDescription(
            key="echoStatus",
            name="Echo",
            icon="mdi:account-voice",
        ),
        HonSwitchEntityDescription(
            key="ecoMode",
            name="Eco Mode",
            icon="mdi:sprout",
            translation_key="eco_mode",
        ),
        HonSwitchEntityDescription(
            key="healthMode",
            name="Health Mode",
            icon="mdi:medication-outline",
        ),
        HonSwitchEntityDescription(
            key="muteStatus",
            name="Silent Mode",
            icon="mdi:volume-off",
            translation_key="silent_mode",
        ),
        HonSwitchEntityDescription(
            key="rapidMode",
            name="Rapid Mode",
            icon="mdi:run-fast",
            translation_key="rapid_mode",
        ),
        HonSwitchEntityDescription(
            key="screenDisplayStatus",
            name="Screen Display",
            icon="mdi:monitor-small",
        ),
        HonSwitchEntityDescription(
            key="selfCleaning56Status",
            name="Self Cleaning 56",
            icon="mdi:air-filter",
            translation_key="self_clean_56",
        ),
        HonSwitchEntityDescription(
            key="selfCleaningStatus",
            name="Self Cleaning",
            icon="mdi:air-filter",
            translation_key="self_clean",
        ),
        HonSwitchEntityDescription(
            key="silentSleepStatus",
            name="Night Mode",
            icon="mdi:bed",
            translation_key="night_mode",
        ),
    ),
    "REF": (
        HonSwitchEntityDescription(
            key="intelligenceMode",
            name="Auto-Set Mode",
            icon="mdi:thermometer-auto",
            translation_key="auto_set",
        ),
        HonSwitchEntityDescription(
            key="quickModeZ2",
            name="Super Freeze",
            icon="mdi:snowflake-variant",
            translation_key="super_freeze",
        ),
        HonSwitchEntityDescription(
            key="quickModeZ1",
            name="Super Cool",
            icon="mdi:snowflake",
            translation_key="super_cool",
        ),
    ),
    "WC": (
        HonSwitchEntityDescription(
            key="sabbathStatus",
            name="Sabbath Mode",
            icon="mdi:palm-tree",
            translation_key="holiday_mode",
        ),
    ),
    "HO": (
        HonControlSwitchEntityDescription(
            key="onOffStatus",
            name="Hood",
            icon="mdi:hvac",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
            translation_key="hood",
        ),
    ),
    "AP": (
        HonSwitchEntityDescription(
            key="touchToneStatus",
            name="Touch Tone",
            icon="mdi:account-voice",
            translation_key="touch_tone",
        ),
    ),
    "FRE": (
        HonSwitchEntityDescription(
            key="quickModeZ2",
            name="Super Freeze",
            icon="mdi:snowflake-variant",
            translation_key="super_freeze",
        ),
        HonSwitchEntityDescription(
            key="quickModeZ1",
            name="Super Cool",
            icon="mdi:snowflake",
            translation_key="super_cool",
        ),
    ),
}

SWITCHES["WD"] = unique_entities(SWITCHES["WD"], SWITCHES["WM"])
SWITCHES["WD"] = unique_entities(SWITCHES["WD"], SWITCHES["TD"])


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    entities = []
    entity: HonConfigSwitchEntity | HonControlSwitchEntity | HonSwitchEntity
    for device in hass.data[DOMAIN][entry.unique_id]["hon"].appliances:
        for description in SWITCHES.get(device.appliance_type, []):
            if isinstance(description, HonConfigSwitchEntityDescription):
                if description.key not in device.available_settings:
                    continue
                entity = HonConfigSwitchEntity(hass, entry, device, description)
            elif isinstance(description, HonControlSwitchEntityDescription):
                if not (
                    device.get(description.key) is not None
                    or description.turn_on_key in list(device.commands)
                    or description.turn_off_key in list(device.commands)
                ):
                    continue
                entity = HonControlSwitchEntity(hass, entry, device, description)
            elif isinstance(description, HonSwitchEntityDescription):
                if f"settings.{description.key}" not in device.available_settings:
                    continue
                entity = HonSwitchEntity(hass, entry, device, description)
            else:
                continue
            entities.append(entity)

    async_add_entities(entities)


class HonSwitchEntity(HonEntity, SwitchEntity):
    entity_description: HonSwitchEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return True if entity is on."""
        return self._device.get(self.entity_description.key, 0) == 1

    async def async_turn_on(self, **kwargs: Any) -> None:
        setting = self._device.settings[f"settings.{self.entity_description.key}"]
        if type(setting) == HonParameter:
            return
        setting.value = setting.max if isinstance(setting, HonParameterRange) else 1
        self.async_write_ha_state()
        await self._device.commands["settings"].send()
        self.coordinator.async_set_updated_data({})

    async def async_turn_off(self, **kwargs: Any) -> None:
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
        if not super().available:
            return False
        if not self._device.get("remoteCtrValid", 1) == 1:
            return False
        if self._device.get("attributes.lastConnEvent.category") == "DISCONNECTED":
            return False
        setting = self._device.settings[f"settings.{self.entity_description.key}"]
        if isinstance(setting, HonParameterRange) and len(setting.values) < 2:
            return False
        return True

    @callback
    def _handle_coordinator_update(self, update: bool = True) -> None:
        self._attr_is_on = self.is_on
        if update:
            self.schedule_update_ha_state()


class HonControlSwitchEntity(HonEntity, SwitchEntity):
    entity_description: HonControlSwitchEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return True if entity is on."""
        return self._device.get(self.entity_description.key, False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        self._device.sync_command(self.entity_description.turn_on_key, "settings")
        self.coordinator.async_set_updated_data({})
        await self._device.commands[self.entity_description.turn_on_key].send()
        self._device.attributes[self.entity_description.key] = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        self._device.sync_command(self.entity_description.turn_off_key, "settings")
        self.coordinator.async_set_updated_data({})
        await self._device.commands[self.entity_description.turn_off_key].send()
        self._device.attributes[self.entity_description.key] = False
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and int(self._device.get("remoteCtrValid", 1)) == 1
            and self._device.connection
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the optional state attributes."""
        result = {}
        if remaining_time := self._device.get("remainingTimeMM", 0):
            delay_time = self._device.get("delayTime", 0)
            result["start_time"] = datetime.now() + timedelta(minutes=delay_time)
            result["end_time"] = datetime.now() + timedelta(
                minutes=delay_time + remaining_time
            )
        return result


class HonConfigSwitchEntity(HonEntity, SwitchEntity):
    entity_description: HonConfigSwitchEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return True if entity is on."""
        setting = self._device.settings[self.entity_description.key]
        return (
            setting.value != setting.min
            if hasattr(setting, "min")
            else setting.value == "1"
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        setting = self._device.settings[self.entity_description.key]
        if type(setting) == HonParameter:
            return
        setting.value = setting.max if isinstance(setting, HonParameterRange) else "1"
        self.coordinator.async_set_updated_data({})
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        setting = self._device.settings[self.entity_description.key]
        if type(setting) == HonParameter:
            return
        setting.value = setting.min if isinstance(setting, HonParameterRange) else "0"
        self.coordinator.async_set_updated_data({})
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self, update: bool = True) -> None:
        self._attr_is_on = self.is_on
        if update:
            self.schedule_update_ha_state()
