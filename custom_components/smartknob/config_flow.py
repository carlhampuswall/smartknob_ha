import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow

from .const import (
    DOMAIN,
)


class SmartknobConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("host"): str,
                    }
                ),
            )
        return self.async_create_entry(title="My Integration", data=user_input)
