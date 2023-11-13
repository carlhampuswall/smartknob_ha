import logging
import json

from homeassistant.const import STATE_ON, STATE_OFF

from .const import (
    DOMAIN,
    TOPIC_TO_KNOB,
    TOPIC_FROM_KNOB,
    SWITCH_ID,
    LIGHT_ID,
    SENSOR_ID,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    _LOGGER.debug("async_setup")
    # hass.async_create_task(hass.config_entries.flow.async_init(DOMAIN))

    async def mqtt_message_recived(msg):
        # _LOGGER.error("Message recived on topic %s: %s", msg.topic, msg.payload)

        try:
            payload = json.loads(msg.payload)
        except json.JSONDecodeError as e:
            _LOGGER.error("Error decoding JSON payload: %s", e)
            return

        if (
            "app_id" not in payload
            or "app_uid" not in payload
            or "command" not in payload
        ):
            _LOGGER.error("Payload missing entity_id or app_uid or command")
            return

        app_id = payload["app_id"]
        app_uid = payload["app_uid"]
        command = payload["command"]
        # data = payload["data"]

        if app_id == SWITCH_ID:
            _LOGGER.error("Switch command executing")
            if command == "turn_on":
                hass.states.async_set("switch.virtual_switch_1", STATE_ON)
            elif command == "turn_off":
                hass.states.async_set("switch.virtual_switch_1", STATE_OFF)
            elif command == "toggle":
                hass.states.async_set(
                    "switch.virtual_switch_1",
                    STATE_ON
                    if hass.states.get("switch.virtual_switch_1").state == STATE_OFF
                    else STATE_OFF,
                )
            else:
                _LOGGER.error("Not implemented command")

        elif app_id == LIGHT_ID:
            _LOGGER.error("Light command executing")
            if command == "turn_on":
                # hass.states.async_set("light.smartknob", "on")
                pass
            elif command == "turn_off":
                # hass.states.async_set("light.smartknob", "off")
                pass
            elif command == "set_brightness":
                pass

        else:
            _LOGGER.error("No implemented app_id")
            return

    await hass.components.mqtt.async_subscribe(TOPIC_FROM_KNOB, mqtt_message_recived, 0)

    return True


async def async_setup_entry(hass, config):
    """Set up the Your Integration entry."""
    hass.data.setdefault(DOMAIN, {})
    return True
