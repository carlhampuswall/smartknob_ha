from .const import LIGHT_SWITCH
from .controller import Controller


class SwitchController(Controller):
    def __init__(self, hass, entity_id):
        super().__init__(hass, entity_id, LIGHT_SWITCH)

    async def async_set_value(self, new_value):
        if new_value == 1.0:
            await self.hass.services.async_call(
                "light", "turn_on", {"entity_id": self.entity_id}
            )

        elif new_value == 0.0:
            await self.hass.services.async_call(
                "light", "turn_off", {"entity_id": self.entity_id}
            )
