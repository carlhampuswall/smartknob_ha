import logging
import json

from .apps import Apps

from homeassistant.core import HomeAssistant, Config
from homeassistant.const import STATE_ON, STATE_OFF, SERVICE_TURN_ON, SERVICE_TURN_OFF
from .dimmercontroller import DimmerController
from .switchcontroller import SwitchController
from homeassistant.helpers.entity_registry import async_validate_entity_id, async_get

from .const import (
    DOMAIN,
    TOPIC_TO_KNOB,
    TOPIC_TO_HASS,
    LIGHT_SWITCH,
    LIGHT_DIMMER,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config):
    _LOGGER.debug("async_setup")

    apps = Apps()

    apps.add(DimmerController(hass, "light.virtual_light_1"))
    apps.add(SwitchController(hass, "switch.virtual_switch_1"))

    async def init_knob():
        await hass.components.mqtt.async_publish(
            hass,
            TOPIC_TO_KNOB,
            json.dumps(await apps.async_get_all_for_knob()),
        )

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
            _LOGGER.error("Switch command executing")
            await apps.get(entity_id).async_set_value(new_value)

        elif app_slug == LIGHT_DIMMER:
            _LOGGER.error("Light command executing")
            await apps.get(entity_id).async_set_value(new_value)

        else:
            _LOGGER.error("No implemented app_slug")
            return

    await hass.components.mqtt.async_subscribe(TOPIC_TO_HASS, mqtt_message_recived, 0)

    await init_knob()

    return True


async def async_setup_entry(hass, config):
    """Set up the Your Integration entry."""
    hass.data.setdefault(DOMAIN, {})
    return True
