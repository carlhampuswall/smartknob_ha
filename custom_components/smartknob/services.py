from homeassistant.core import HomeAssistant
from .logger import _LOGGER


class Services:
    """Handles services."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the Service Handler."""
        self.hass = hass

    async def async_switch(self, entity_id: str, turn_on: str):
        """Switch the entity on or off."""
        if turn_on == "1":
            await self.hass.services.async_call(
                "switch", "turn_on", {"entity_id": entity_id}
            )
        else:
            await self.hass.services.async_call(
                "switch", "turn_off", {"entity_id": entity_id}
            )

    async def async_light(
        self, entity_id: str, turn_on: bool, brightness=None, color=None
    ):
        """Switch the light on or off, and set its brightness and color."""
        if turn_on == "1":
            await self.hass.services.async_call(
                "light", "turn_on", {"entity_id": entity_id}
            )
        else:
            await self.hass.services.async_call(
                "light", "turn_off", {"entity_id": entity_id}
            )
