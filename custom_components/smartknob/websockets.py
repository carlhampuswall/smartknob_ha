from homeassistant.core import HomeAssistant, callback
from .logger import _LOGGER
from homeassistant.components.websocket_api import async_register_command
from homeassistant.components import websocket_api
from homeassistant.components.http.data_validator import RequestDataValidator
import voluptuous as vol
import json

from .const import APP_SLUGS, DOMAIN
from homeassistant.components.http import HomeAssistantView


async def async_register_websockets(hass):
    hass.http.register_view(SmartknobConfigView)
    hass.http.register_view(SmartknobAppsView)
    hass.http.register_view(SmartknobAppSlugsView)


class SmartknobConfigView(HomeAssistantView):
    url = "/api/smartknob/config"
    name = "api:smartknob:config"

    async def post(self, request, data):
        return self.json({"success": False, "error": "Not implemented"})

    async def get(self, request):
        return self.json({"success": False, "error": "Not implemented"})


class SmartknobAppsView(HomeAssistantView):
    url = "/api/smartknob/apps"
    name = "api:smartknob:apps"

    @RequestDataValidator(
        vol.Schema(
            {
                vol.Required("apps"): [
                    {
                        vol.Required("app_id"): str,
                        vol.Required("app_slug_id"): str,
                        vol.Required("entity_id"): str,
                        vol.Required("friendly_name"): str,
                    }
                ],
            }
        )
    )
    async def post(self, request, data: dict):
        hass: HomeAssistant = request.app["hass"]
        coordinator = hass.data[DOMAIN]["coordinator"]
        apps = data.get("apps")

        if len(apps) > 1:
            await coordinator.store.async_update_apps(apps)
        await coordinator.async_update_app_config(data.get("apps")[0])

        return self.json({"success": True})  # TODO return actual success or error

    async def get(self, request):
        hass: HomeAssistant = request.app["hass"]
        coordinator = hass.data[DOMAIN]["coordinator"]
        apps = coordinator.store.async_get_apps()
        return self.json(
            {"success": True, "apps": apps}
        )  # TODO return actual success or error


class SmartknobAppSlugsView(HomeAssistantView):
    url = "/api/smartknob/app_slugs"
    name = "api:smartknob:app_slugs"

    async def get(self, request):
        # hass: HomeAssistant = request.app["hass"]
        # coordinator = hass.data[DOMAIN]["coordinator"]

        return self.json({"success": True, "app_slugs": APP_SLUGS})
