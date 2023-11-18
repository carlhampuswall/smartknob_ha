DOMAIN = "smartknob"

TOPIC_TO_KNOB = "smartknob/to_knob"
TOPIC_TO_HASS = "smartknob/to_hass"


LIGHT_SWITCH = "light_switch"
LIGHT_DIMMER = "light_dimmer"


APP_SLUGS = [
    {
        "app_slug": LIGHT_SWITCH,
        "friendly_name": "Light Switch",
        "supported_features": 1,
    },
    {
        "app_slug": LIGHT_DIMMER,
        "friendly_name": "Light Dimmer",
        "supported_features": 1,
    },
]
