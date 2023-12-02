import { App, AppSlug, HomeAssistant } from '../types';

export const getAsyncApps = (hass: HomeAssistant) => {
  return hass.callApi<{ success; apps: App[] }>('GET', 'smartknob/apps');
};

export const saveApp = (hass: HomeAssistant, app: App) => {
  return hass.callApi('POST', 'smartknob/apps', {
    apps: [
      {
        app_id: app.app_id,
        app_slug_id: app.app_slug_id,
        entity_id: app.entity_id,
        friendly_name: app.friendly_name,
      },
    ],
  });
};

export const saveApps = (hass: HomeAssistant, apps: App[]) => {
  const _apps: {}[] = [];
  for (const app of apps) {
    _apps.push({
      app_id: app.app_id,
      app_slug_id: app.app_slug_id,
      entity_id: app.entity_id,
      friendly_name: app.friendly_name,
    });
  }

  console.log(_apps);
  console.log('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!');
  return hass.callApi('POST', 'smartknob/apps', {
    apps: _apps,
  });
};

//! WTF ?? why does this still return a promise what am i missing?
export const getAsyncAppSlugs = async (hass: HomeAssistant) => {
  const res = await hass.callApi<{ success; app_slugs: AppSlug[] }>(
    'GET',
    'smartknob/app_slugs',
  );

  if (res.success != 'success') console.log("ERROR: Couldn't get app slugs");

  return res;
};
