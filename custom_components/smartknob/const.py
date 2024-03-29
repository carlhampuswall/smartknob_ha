DOMAIN = "smartknob"
NAME = "Smartknob"

STORAGE_KEY = f"{DOMAIN}.storage"
DATA_REGISTRY = f"{DOMAIN}_storage"

SAVE_DELAY = 10

TOPIC_INIT = DOMAIN + "/init"

TOPIC_TO_KNOB = "smartknob/to_knob"
TOPIC_TO_HASS = "smartknob/to_hass"


LIGHT_SWITCH = "light_switch"
LIGHT_DIMMER = "light_dimmer"
SWITCH = "switch"

DOMAIN_LIGHT = "light"
DOMAIN_SWITCH = "switch"


APP_SLUGS = [
    {
        "slug_id": LIGHT_SWITCH,
        "friendly_name": "Light Switch",
        "domain": DOMAIN_LIGHT,
        "supported_features": 1,
    },
    {
        "slug_id": LIGHT_DIMMER,
        "friendly_name": "Light Dimmer",
        "domain": DOMAIN_LIGHT,
        "supported_features": 1,
    },
    {
        "slug_id": SWITCH,
        "friendly_name": "Switch",
        "domain": DOMAIN_SWITCH,
        "supported_features": 1,
    },
]


CUSTOM_COMPONENTS = "custom_components"
INTEGRATION_FOLDER = DOMAIN

PANEL_TITLE = NAME
PANEL_FOLDER = "frontend/dist"
PANEL_FILENAME = "smartknob-panel.js"
PANEL_URL = "/api/panel_custom/smartknob"
PANEL_NAME = "smartknob-panel"
PANEL_ICON = "mdi:knob"
