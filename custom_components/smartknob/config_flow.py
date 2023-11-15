import logging
from xml.etree.ElementInclude import include
import voluptuous as vol
from homeassistant.core import callback
from homeassistant.data_entry_flow import RESULT_TYPE_FORM
from homeassistant.helpers import entity, selector
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import SUPPORT_BRIGHTNESS, LightEntityFeature

from homeassistant.helpers import area_registry, entity_registry
from homeassistant import config_entries

from .dimmercontroller import DimmerController


from .const import DOMAIN, APP_SLUGS, LIGHT_DIMMER

_LOGGER = logging.getLogger(__name__)


class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    # async def async_step_init(self, user_input=None):
    #     return await self.async_step_app()

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_menu(
                step_id="user",
                menu_options={
                    "app_type": "Add app",
                    "list_apps": "List apps",
                    "remove_app": "Remove app",
                    "configure": "Configure Smartknob",
                },
            )

    async def async_step_app_type(self, user_input=None):
        if user_input is None:
            app_slugs = {}
            for app_slug in APP_SLUGS:
                app_slugs[app_slug["app_slug"]] = app_slug["friendly_name"]

            schema = vol.Schema(
                {
                    vol.Required("app_slug"): vol.In(app_slugs),
                },
                required=False,
            )

            return self.async_show_form(
                step_id="app_type",
                data_schema=schema,
            )

        return await self.async_step_app_entity(app_type_input=user_input)

    async def async_step_app_entity(
        self, user_input=None, app_type_input=None
    ):  # TODO app_type_input is None after submit
        _LOGGER.error(user_input)
        app_slug = app_type_input["app_slug"]
        domain = "light"  # TODO get domain from app_slug

        if user_input is None:
            entities = self.hass.states.async_entity_ids(domain)

            if app_slug == LIGHT_DIMMER:
                _LOGGER.error("LIGHT_DIMMER")
                entities = [
                    entity
                    for entity in entities
                    if self.hass.states.get(entity).attributes.get(
                        "supported_features", 0
                    )
                    & SUPPORT_BRIGHTNESS
                ]

            schema = vol.Schema(
                {
                    vol.Required("entity"): selector.EntitySelector(
                        selector.EntitySelectorConfig(include_entities=entities)
                    ),
                }
            )

            return self.async_show_form(
                step_id="app_entity",
                data_schema=schema,
            )

        entity_id = user_input["entity"]
        if domain == "light":
            if app_slug == LIGHT_DIMMER:
                light = DimmerController(self.hass, entity_id)
                _LOGGER.error(light)

        pass
