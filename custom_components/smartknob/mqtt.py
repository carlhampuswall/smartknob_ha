import json

from config.custom_components.smartknob.services import Services
from config.custom_components.smartknob.store import SmartknobConfig
from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, TOPIC_INIT, TOPIC_TO_KNOB
from .logger import _LOGGER


class MqttHandler:
    """Handles MQTT messages between HASS and Smartknob."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the MQTT handler."""
        self.hass = hass
        self.services = Services(hass)
        self._subscribed_topics = []
        self._subscriptions = []

        self.hass.async_add_job(self._async_subscribe_to_init())
        self.hass.async_add_job(self._async_subscribe_to_knobs())

    # @callback
    async def async_entity_state_changed(
        self,
        knobs_needing_update: list[dict],
        app_id,
        old_state,
        new_state,
    ):
        """Handle entity state changes."""
        _LOGGER.error("STATE CHANGE CALLBACK")
        _LOGGER.error(knobs_needing_update)
        _LOGGER.error("")
        for knob in knobs_needing_update:
            new_bool_state = new_state.state == "on"
            await mqtt.async_publish(
                self.hass,
                "smartknob/" + knob["mac_address"] + "/from_hass",
                json.dumps(
                    {"app_id": app_id[0], "new_state": new_bool_state}
                ),  # app_id[0] is for testing now TODO NEEDS NEW IMPLEMENTATION
                retain=True,
            )
            # self.hass.async_add_job(
            #     mqtt.async_publish(
            #         self.hass,
            #         "smartknob/" + knob["mac_address"] + "/from_hass",
            #         new_state,
            #         retain=True,
            #     )
            # )

    # @callback
    # def async_entity_state_changed(area_id: str, old_state: str, new_state: str):

    #     # if not self._config[ATTR_MQTT][const.ATTR_ENABLED] or not new_state:
    #     #     return

    #     topic = self._config[ATTR_MQTT][CONF_STATE_TOPIC]

    #     if not topic:  # do not publish if no topic is provided
    #         return

    #     if area_id and len(self.hass.data[const.DOMAIN]["areas"]) > 1:
    #         # handle the sending of a state update for a specific area
    #         area = self.hass.data[const.DOMAIN]["areas"][area_id]
    #         topic = topic.rsplit('/', 1)
    #         topic.insert(1, slugify(area.name))
    #         topic = "/".join(topic)

    #     payload_config = self._config[ATTR_MQTT][const.ATTR_STATE_PAYLOAD]
    #     if new_state in payload_config and payload_config[new_state]:
    #         message = payload_config[new_state]
    #     else:
    #         message = new_state

    #     hass.async_create_task(mqtt.async_publish(self.hass, topic, message, retain=True))
    #     _LOGGER.debug("Published state '{}' on topic '{}'".format(message, topic))

    # self._subscriptions.append(
    #     async_dispatcher_connect(self.hass, "alarmo_state_updated", async_alarm_state_changed)
    # )

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
                    if app["app_slug_id"] == "light_switch":
                        await self.services.async_light(app["entity_id"], state)
                    elif app["app_slug_id"] == "switch":
                        await self.services.async_switch(app["entity_id"], state)
                    else:
                        _LOGGER.error("Not implemented command")
                    # knob.async_update(msg.payload)
                    _LOGGER.error("KNOB GOT")
                    _LOGGER.error(app)

        except ValueError:
            _LOGGER.error("Error decoding JSON payload")
            return


"""


"knobs": [
      {
        "mac_address": "1C:9D:C2:FD:ED:50",
        "apps": [
          {
            "app_id": "light_switch-light.virtual_light_1",
            "app_slug_id": "light_switch",
            "entity_id": "light.virtual_light_1",
            "friendly_name": "Light 1"
          }
        ]
      }
    ]

"""
