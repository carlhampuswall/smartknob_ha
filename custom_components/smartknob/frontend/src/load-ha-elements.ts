/* eslint-disable  @typescript-eslint/no-explicit-any */
export const loadHa = async () => {
  if (customElements.get('ha-selector-entity')) return;

  await customElements.whenDefined('partial-panel-resolver');
  const ppr = document.createElement('partial-panel-resolver') as any;
  ppr.hass = {
    panels: [
      {
        url_path: 'tmp',
        component_name: 'config',
      },
    ],
  };
  ppr._updateRoutes();
  await ppr.routerOptions.routes.tmp.load();

  await customElements.whenDefined('ha-panel-config');

  const cpr = document.createElement('ha-panel-config') as any;
  await cpr.routerOptions.routes.automation.load();
};
