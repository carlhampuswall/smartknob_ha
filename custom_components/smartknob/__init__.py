from .panel import (
    async_register_panel,
    async_unregister_panel,
)
from .logger import _LOGGER

import json

import homeassistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .websockets import async_register_websockets
from .store import async_get_registry

from homeassistant.const import SERVICE_TURN_ON, SERVICE_TURN_OFF
from homeassistant.components import panel_custom


from .const import (
    DOMAIN,
    TOPIC_TO_HASS,
    LIGHT_SWITCH,
    LIGHT_DIMMER,
)


async def async_setup(hass: HomeAssistant, config):
    _LOGGER.debug("async_setup")

    async def mqtt_message_recived(msg):
        try:
            payload = json.loads(msg.payload)
        except json.JSONDecodeError as e:
            _LOGGER.error("Error decoding JSON payload: %s", e)
            return

        if (
            "entity_id" not in payload
            or "app_slug" not in payload
            or "new_value" not in payload
        ):
            _LOGGER.error("Payload missing entity_id or app_slug or new_value")
            return

        entity_id = payload["entity_id"]
        app_slug = payload["app_slug"]
        new_value = payload["new_value"]

        if app_slug == LIGHT_SWITCH:
            _LOGGER.debug("Switch command executing")
            if new_value == 1.0:
                await hass.services.async_call(
                    "light", "turn_on", {"entity_id": entity_id}
                )

            elif new_value == 0.0:
                await hass.services.async_call(
                    "light", "turn_off", {"entity_id": entity_id}
                )

            else:
                _LOGGER.error("Not implemented command")

        elif app_slug == LIGHT_DIMMER:
            _LOGGER.debug("Light command executing")
            if new_value != None:
                await hass.services.async_call(
                    "light",
                    SERVICE_TURN_ON if new_value > 0.0 else SERVICE_TURN_OFF,
                    {"entity_id": entity_id, "brightness": new_value * 2.55}
                    if new_value > 0.0
                    else {"entity_id": entity_id},
                )
            else:
                _LOGGER.error("Not implemented command")

        else:
            _LOGGER.error("No implemented app_id")
            return

    await hass.components.mqtt.async_subscribe(TOPIC_TO_HASS, mqtt_message_recived, 0)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the Your Integration entry."""
    session = async_get_clientsession(hass)

    store = await async_get_registry(hass)
    coordinator = SmartknobCoordinator(hass, session, entry, store)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN] = {"coordinator": coordinator, "apps": []}

    if entry.unique_id is None:
        hass.config_entries.async_update_entry(entry, unique_id=coordinator.id, data={})

    await async_register_panel(hass)

    # Websocket support
    await async_register_websockets(hass)

    # LOAD CONFIG DATA
    coordinator.store.async_load()

    return True


async def async_remove_entry(hass, entry):
    async_unregister_panel(hass)
    coordinator = hass.data[DOMAIN]["coordinator"]
    await coordinator.async_delete_config()
    del hass.data[DOMAIN]


class SmartknobCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, session, entry, store):
        self.id = entry.entry_id
        self.hass = hass
        self.entry = entry
        self.store = store

        super().__init__(hass, _LOGGER, name=DOMAIN)

    async def async_update_app_config(self, data: dict = None):
        if self.store.async_get_app(data.get("app_id")):
            self.store.async_update_app(data.get("app_id"), data)

        self.store.async_create_app(data)

    async def async_unload(self):
        del self.hass.data[DOMAIN]["apps"]

    async def async_delete_config(self):
        await self.store.async_delete()
