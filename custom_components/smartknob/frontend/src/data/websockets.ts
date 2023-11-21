import { AppListItem, HomeAssistant } from '../types';

export const getAsyncApps = (hass: HomeAssistant) => {
  return hass.callApi('GET', 'smartknob/apps');
};

export const saveApp = (hass: HomeAssistant, app: AppListItem) => {
  return hass.callApi('POST', 'smartknob/apps', {
    app_id: app.app_id,
    app_slug_id: app.app_slug.slug,
    entity_id: app.entity?.entity_id,
  });
};
