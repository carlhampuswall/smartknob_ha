# from homeassistant.components import panel_custom
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, TOPIC_INIT
from .logger import _LOGGER
from .mqtt import MqttHandler
from .panel import async_register_panel, async_unregister_panel
from .store import async_get_registry
from .websockets import async_register_websockets


async def async_setup(hass: HomeAssistant, config):
    _LOGGER.debug("async_setup")
    """
    hass: HomeAssistant = request.app["hass"]
    coordinator = hass.data[DOMAIN]["coordinator"]
    apps = coordinator.store.async_get_apps()

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

    async def async_init_received(msg):
        _LOGGER.error("MQTT MESSAGE RECIVED")
        _LOGGER.error(msg)

    await hass.components.mqtt.async_subscribe(TOPIC_TO_HASS, mqtt_message_recived, 0)
    await hass.components.mqtt.async_subscribe(TOPIC_INIT, async_init_received, 0)
    """

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup Smartknob integration."""
    hass.data.setdefault(DOMAIN, {})
    session = async_get_clientsession(hass)

    store = await async_get_registry(hass)
    coordinator = SmartknobCoordinator(hass, session, entry, store)

    hass.data[DOMAIN] = {"coordinator": coordinator, "apps": []}

    if entry.unique_id is None:
        hass.config_entries.async_update_entry(entry, unique_id=coordinator.id, data={})

    await async_register_panel(hass)

    # Register Websockets
    await async_register_websockets(hass)

    # Load Config Data
    await coordinator.store.async_load()

    # TODO THIS IS FOR TESTING
    coordinator = hass.data[DOMAIN]["coordinator"]
    # TODO THIS IS FOR TESTING

    return True


async def async_remove_entry(hass, entry):
    async_unregister_panel(hass)
    coordinator = hass.data[DOMAIN]["coordinator"]
    await coordinator.async_delete_config()
    del hass.data[DOMAIN]


class SmartknobCoordinator(DataUpdateCoordinator):
    """Smartknob DataUpdateCoordinator."""  # TODO ADD BETTER COORDINATOR DESC

    def __init__(self, hass, session, entry, store) -> None:
        """Initialize the coordinator."""
        self.id = entry.entry_id
        self.hass = hass
        self.entry = entry
        self.store = store

        self.hass.data[DOMAIN]["mqtt_handler"] = MqttHandler(self.hass)

        super().__init__(hass, _LOGGER, name=DOMAIN)

    async def async_update_app_config(self, data: dict = None):
        """Update config for app."""
        if self.store.async_get_app(data.get("app_id")):
            self.store.async_update_app(data)
            return

        self.store.async_create_app(data)

    async def async_unload(self):
        """Unload coordinator."""
        del self.hass.data[DOMAIN]["apps"]

    async def async_delete_config(self):
        """Delete config."""
        await self.store.async_delete()
