import logging

from homeassistant import config_entries

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


# TODO tell user to go to Smartknob panel after submit
class SmartknobConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
            )

        _LOGGER.debug("Creating config entry for Smartknob")
        return self.async_create_entry(title="Smartknob", data=user_input)
