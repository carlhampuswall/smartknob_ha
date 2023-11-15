from homeassistant.helpers import area_registry, entity_registry


class Controller:
    def __init__(self, hass, entity_id, app_slug):
        self.hass = hass
        self.entity_id = entity_id
        self.app_slug = app_slug

    async def async_get_area(self, entity_id):
        area_reg = area_registry.async_get(self.hass)
        entity_reg = entity_registry.async_get(self.hass)

        entity = entity_reg.async_get(entity_id)
        if entity is None:
            return None

        return area_reg.async_get_area(entity.area_id)
