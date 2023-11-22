from email.policy import default
from typing import MutableMapping, cast
import attr

from homeassistant.core import HomeAssistant, callback
from homeassistant.loader import bind_hass
from .logger import _LOGGER
from homeassistant.helpers.storage import Store

from .const import (
    DATA_REGISTRY,
    DOMAIN,
    LIGHT_DIMMER,
    LIGHT_SWITCH,
    SAVE_DELAY,
    STORAGE_KEY,
    SWITCH,
)


@attr.s(slots=True, frozen=True)
class AppEntry:
    """App storage entry."""

    app_id = attr.ib(type=str, default=None)
    app_slug_id = attr.ib(type=str, default=None)
    entity_id = attr.ib(type=str, default=None)


class SmartknobStorage:
    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.config: MutableMapping[
            str, str
        ] = {}  #! ADD SMARTKNOB DEVICE SPECIFIC CONFIG HERE
        self.apps = []
        self._store = Store(hass, 1, STORAGE_KEY)

    async def async_load(self) -> None:
        data = await self._store.async_load()
        if data is None:
            return
        if "apps" in data:
            for app in data["apps"]:
                self.apps.append(
                    AppEntry(
                        app_id=app["app_id"],
                        app_slug_id=app["app_slug_id"],
                        entity_id=app["entity_id"],
                    )
                )

    @callback
    def async_schedule_save(self) -> None:
        """Schedule saving the registry of alarmo."""
        self._store.async_delay_save(self._data_to_save, SAVE_DELAY)

    async def async_save(self) -> None:
        await self._store.async_save(self._data_to_save())

    @callback
    def _data_to_save(self) -> dict:
        store_data = {
            "apps": [attr.asdict(app) for app in self.apps],
        }

        # EXAMPLE OF ADDING MORE DATA TO STORE
        # store_data["apps"] = [attr.asdict(entry) for entry in self.areas.values()]

        return store_data

    async def async_delete(self):
        _LOGGER.warning("Removing Smartknob configuration data!")
        await self._store.async_remove()
        self.config = {}
        self.apps = []

    @callback
    def async_get_app(self, app_id: str):
        res = None
        for app in self.apps:
            if app.app_id == app_id:
                res = attr.asdict(app)
        return res

    @callback
    def async_get_apps(self):
        res = []
        for app in self.apps:
            res.append(attr.asdict(app))
        return res

    @callback
    def async_create_app(self, data: dict) -> AppEntry:
        new_app = AppEntry(**data)
        self.apps.append(new_app)
        self.async_schedule_save()
        return attr.asdict(new_app)

    @callback
    def async_delete_app(self, app_id: str) -> None:
        if app_id in self.apps:
            for app in self.apps:
                if app.app_id == app_id:
                    self.apps.remove(app)
            self.async_schedule_save()
            return True
        return False

    # @callback
    # def async_update_app(self, index, data: dict) -> AppEntry:

    #     # old = None
    #     # for app in self.apps:
    #     #     if app.app_id == data.get("app_id"):
    #     #         old = app

    #     # _LOGGER.error("Old: %s", old)
    #     # self.apps.remove(old)

    #     # new = self.apps = attr.evolve(old, **data)
    #     # self.async_schedule_save()
    #     # return attr.asdict(new)

    @callback
    def async_update_apps(self, new_apps):
        """Update existing config."""

        # old = self.apps
        # new = self.apps = attr.evolve(old, **changes)
        # self.async_schedule_save()
        # return attr.asdict(new)
        old = self.apps
        new = []

        for app in new_apps:
            new_app = AppEntry(**app)
            new.append(new_app)

        self.apps = new

        self.async_schedule_save()

        return attr.asdict(new)
        # _LOGGER.error("OLD: %s", old)
        # _LOGGER.error("HERE: %s", changes)


@bind_hass
async def async_get_registry(hass: HomeAssistant) -> SmartknobStorage:
    """Return smartknob storage instance."""
    task = hass.data.get(DATA_REGISTRY)

    if task is None:

        async def _load_reg() -> SmartknobStorage:
            registry = SmartknobStorage(hass)
            await registry.async_load()
            return registry

        task = hass.data[DATA_REGISTRY] = hass.async_create_task(_load_reg())

    return cast(SmartknobStorage, await task)
