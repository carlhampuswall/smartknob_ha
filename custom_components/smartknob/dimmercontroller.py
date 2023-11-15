import logging

from .const import LIGHT_DIMMER

from .controller import Controller
from homeassistant.const import SERVICE_TURN_ON, SERVICE_TURN_OFF

_LOGGER = logging.getLogger(__name__)


class DimmerController(Controller):
    def __init__(self, hass, entity_id):
        super().__init__(hass, entity_id, LIGHT_DIMMER)

    async def async_set_value(self, new_value):
        if new_value != None:
            is_on = new_value > 0.0
            await self.hass.services.async_call(
                "light",
                SERVICE_TURN_ON if is_on else SERVICE_TURN_OFF,
                {"entity_id": self.entity_id, "brightness": new_value * 2.55}
                if is_on
                else {"entity_id": self.entity_id},
            )
