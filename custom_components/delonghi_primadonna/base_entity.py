from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN
from .device import DelongiPrimadonna, signal_update


class DelonghiDeviceEntity:
    """Entity class for the Delonghi devices"""

    _attr_has_entity_name = True

    def __init__(self, delongh_device, hass: HomeAssistant):
        """Init entity with the device"""
        self._attr_unique_id = (
            f'{delongh_device.mac}_'
            f'{self.__class__.__name__}'
        )
        self.device: DelongiPrimadonna = delongh_device
        self.hass = hass

    async def async_added_to_hass(self) -> None:
        """Subscribe to real-time device updates (push, not 30s poll)."""
        parent = getattr(super(), 'async_added_to_hass', None)
        if parent is not None:
            await parent()
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                signal_update(self.device.mac),
                self.async_write_ha_state,
            )
        )

    @property
    def device_info(self):
        """Shared device info information"""
        return {
            'identifiers': {(DOMAIN, self.device.mac)},
            'connections': {(dr.CONNECTION_NETWORK_MAC, self.device.mac)},
            'name': self.device.name,
            'manufacturer': 'Delonghi',
            'model': self.device.model,
        }
