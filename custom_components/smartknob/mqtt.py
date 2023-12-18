import json

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, TOPIC_INIT
from .logger import _LOGGER


class MqttHandler:
    """Handles MQTT messages between HASS and Smartknob."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the MQTT handler."""
        self.hass = hass
        self._subscribed_topics = []
        self._subscriptions = []

        self.hass.async_add_job(self._async_subscribe_to_init())
        self.hass.async_add_job(self._async_subscribe_to_knobs())

    async def _async_subscribe_to_init(self):
        """Subscribe to init topic."""
        try:
            _LOGGER.error("SUBSCRIBING TO INIT")
            await mqtt.async_subscribe(self.hass, TOPIC_INIT, self.async_init_received)

        except Exception as e:
            _LOGGER.error(e)

    async def _async_subscribe_to_knobs(self):
        """Subscribe to knob topics."""
        try:
            _LOGGER.error("SUBSCRIBING TO KNOBS")
            coordinator = self.hass.data[DOMAIN]["coordinator"]
            knobs = coordinator.store.knobs
            for mac_address in knobs:
                _LOGGER.error(mac_address)
                topic = f"smartknob/{mac_address}/from_knob"
                await mqtt.async_subscribe(
                    self.hass, topic, self.async_message_received
                )

        except Exception as e:
            _LOGGER.error(e)

    @callback
    async def async_init_received(self, msg):
        """Handle init message from Smartknob."""
        # mac_address = None
        try:
            payload = json.loads(msg.payload)

            if "mac_address" in payload:
                mac_address = payload["mac_address"]
                coordinator = self.hass.data[DOMAIN]["coordinator"]
                coordinator.store.async_init_knob(
                    {"mac_address": mac_address, "apps": []}
                )

        except ValueError:
            _LOGGER.error("Error decoding JSON payload")
            return

    @callback
    async def async_message_received(self, msg):
        """Handle messages from Smartknob."""
        try:
            payload = json.loads(msg.payload)
            _LOGGER.error("PAYLOAD")
            _LOGGER.error(msg.payload)
            if "mac_address" in payload:
                mac_address = payload["mac_address"]
                app_id = payload["app_id"]
                state = payload["state"]
                coordinator = self.hass.data[DOMAIN]["coordinator"]

                # knob = coordinator.store.async_get_knob(mac_address)
                app = await coordinator.store.async_get_app(mac_address, app_id)
                if app is not None:
                    if state == "0":
                        await self.hass.services.async_call(
                            "light", "turn_off", {"entity_id": app["entity_id"]}
                        )
                    elif state == "1":
                        await self.hass.services.async_call(
                            "light", "turn_on", {"entity_id": app["entity_id"]}
                        )

                    else:
                        _LOGGER.error("Not implemented command")
                    # knob.async_update(msg.payload)
                    _LOGGER.error("KNOB GOT")
                    _LOGGER.error(app)

        except ValueError:
            _LOGGER.error("Error decoding JSON payload")
            return
