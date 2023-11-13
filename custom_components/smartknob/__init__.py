import logging
import json

from homeassistant.const import STATE_ON, STATE_OFF, SERVICE_TURN_ON, SERVICE_TURN_OFF

from .const import (
    DOMAIN,
    TOPIC_TO_KNOB,
    TOPIC_FROM_KNOB,
    LIGHT_SWITCH,
    LIGHT_DIMMER,
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
            "entity_id" not in payload
            or "app_slug" not in payload
            or "new_value" not in payload
        ):
            _LOGGER.error("Payload missing entity_id or app_slug or new_value")
            return

        entity_id = payload["entity_id"]
        app_slug = payload["app_slug"]
        new_value = payload["new_value"]
        # data = payload["data"]

        # _LOGGER.error(payload)

        if app_slug == LIGHT_SWITCH:
            _LOGGER.error("Switch command executing")
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
            _LOGGER.error("Light command executing")
            if new_value != None:
                await hass.services.async_call(
                    "light",
                    SERVICE_TURN_ON if new_value > 0.0 else SERVICE_TURN_OFF,
                    {"entity_id": entity_id, "brightness": new_value * 2.55},
                )
                _LOGGER.error(hass.states.get(entity_id))
            else:
                _LOGGER.error("Not implemented command")

        else:
            _LOGGER.error("No implemented app_id")
            return

    await hass.components.mqtt.async_subscribe(TOPIC_FROM_KNOB, mqtt_message_recived, 0)

    return True


async def async_setup_entry(hass, config):
    """Set up the Your Integration entry."""
    hass.data.setdefault(DOMAIN, {})
    return True
