"""Button entity definitions for Delonghi Primadonna."""

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .base_entity import DelonghiDeviceEntity
from .const import BEVERAGE_NONE, DOMAIN
from .device import DelongiPrimadonna


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Set up button entities for a config entry."""

    delongh_device: DelongiPrimadonna = hass.data[DOMAIN][entry.unique_id]
    async_add_entities(
        [
            DelongiPrimadonnaPowerButton(delongh_device, hass),
            DelongiPrimadonnaMakeBeverageButton(delongh_device, hass),
            DelongiPrimadonnaCancelBeverageButton(delongh_device, hass),
        ]
    )
    return True


class DelongiPrimadonnaPowerButton(DelonghiDeviceEntity, ButtonEntity):
    """This button turns on the device"""

    _attr_translation_key = 'power_on'

    async def async_press(self):
        self.hass.async_create_task(self.device.power_on())


class DelongiPrimadonnaMakeBeverageButton(DelonghiDeviceEntity, ButtonEntity):
    """Brew the beverage currently chosen in the beverage select."""

    _attr_translation_key = 'make_beverage'
    _attr_icon = 'mdi:coffee-maker'

    async def async_press(self):
        beverage = self.device.selected_beverage
        if beverage and beverage != BEVERAGE_NONE:
            self.hass.async_create_task(
                self.device.beverage_start(beverage)
            )


class DelongiPrimadonnaCancelBeverageButton(DelonghiDeviceEntity, ButtonEntity):
    """Cancel the beverage currently being prepared."""

    _attr_translation_key = 'cancel_beverage'
    _attr_icon = 'mdi:stop'

    async def async_press(self):
        self.hass.async_create_task(self.device.beverage_cancel())
