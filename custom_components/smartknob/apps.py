from .controller import Controller


class Apps:
    def __init__(self):
        self.apps = []
        pass

    def add(self, controller):
        self.apps.append(controller)

    def remove(self, controller):
        self.apps.remove(controller)

    def get(self, entity_id):
        for app in self.apps:
            if app.entity_id == entity_id:
                return app
        return None  # Couldnt find app connected to entity_id

    async def async_get_all_for_knob(self):
        all = []
        for app in self.apps:
            area = await app.async_get_area(app.entity_id)
            all.append(
                {
                    "app_slug": app.app_slug,
                    "entity_id": app.entity_id,
                    "friendly_name": app.hass.states.get(app.entity_id).attributes[
                        "friendly_name"
                    ],
                    "area": area.name
                    if area
                    else "",  # TODO: What value should be here if area is None?
                    "menu_color": "#ffffff",
                }
            )
        return all
