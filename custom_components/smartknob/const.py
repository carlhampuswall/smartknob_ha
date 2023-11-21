DOMAIN = "smartknob"
NAME = "Smartknob"

STORAGE_KEY = f"{DOMAIN}.storage"
DATA_REGISTRY = f"{DOMAIN}_storage"

SAVE_DELAY = 10

TOPIC_TO_KNOB = "smartknob/to_knob"
TOPIC_TO_HASS = "smartknob/to_hass"


LIGHT_SWITCH = "light_switch"
LIGHT_DIMMER = "light_dimmer"
SWITCH = "switch"

# APP_SLUG_IDS = [LIGHT_SWITCH, LIGHT_DIMMER, SWITCH]


APP_SLUGS = [
    {
        "app_slug_id": LIGHT_SWITCH,
        "friendly_name": "Light Switch",
        "supported_features": 1,
    },
    {
        "app_slug_id": LIGHT_DIMMER,
        "friendly_name": "Light Dimmer",
        "supported_features": 1,
    },
    {
        "app_slug_id": SWITCH,
        "friendly_name": "Switch",
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
