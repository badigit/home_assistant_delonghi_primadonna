"""Button entity definitions for Delonghi Primadonna."""

import datetime

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .base_entity import DelonghiDeviceEntity
from .const import BEVERAGE_NONE, DOMAIN
from .device import DelongiPrimadonna
from .model import get_machine_model


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Set up button entities for a config entry."""

    delongh_device: DelongiPrimadonna = hass.data[DOMAIN][entry.unique_id]
    model = get_machine_model(delongh_device.product_code)

    buttons = [
        DelongiPrimadonnaPowerButton(delongh_device, hass),
        DelongiPrimadonnaMakeBeverageButton(delongh_device, hass),
        DelongiPrimadonnaCancelBeverageButton(delongh_device, hass),
    ]

    # Setting the clock is a one-shot action, so it's a button, not a
    # toggle. Only offered on machines whose model exposes a clock.
    if model and model.time_settings:
        buttons.append(DelongiPrimadonnaTimeSyncButton(delongh_device, hass))

    async_add_entities(buttons)
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


class DelongiPrimadonnaTimeSyncButton(DelonghiDeviceEntity, ButtonEntity):
    """Set the machine clock to Home Assistant's current time."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_translation_key = 'time_sync'
    _attr_icon = 'mdi:clock-time-eight-outline'

    async def async_press(self):
        self.hass.async_create_task(
            self.device.set_time(datetime.datetime.now())
        )
