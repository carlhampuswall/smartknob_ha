import './types';
import { html, css, LitElement } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

import './view/app-form';
import { HassEntity } from 'home-assistant-js-websocket';
import { AppListItem, AppSlug, HomeAssistant } from './types';
import { loadHa } from './load-ha-elements';
import { getAsyncApps } from './data/websockets';

@customElement('smartknob-panel')
export class SmartknobPanel extends LitElement {
  static styles = css`
    .header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      height: 64px;
      background-color: var(--app-header-background-color);
      color: var(--text-primary-color);
    }

    .toolbar {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .content {
      padding: 24px;
    }
  `;

  appSlugs: AppSlug[] = [
    {
      slug: 'light_switch',
      friendlyName: 'Light Switch',
      domain: 'light',
    },
    {
      slug: 'light_dimmer',
      friendlyName: 'Light Dimmer',
      domain: 'light',
    },
    {
      slug: 'switch',
      friendlyName: 'Switch',
      domain: 'switch',
    },
  ];

  @state() private _appList: AppListItem[] = [];

  async connectedCallback() {
    super.connectedCallback();
    const object: any = await getAsyncApps(this.hass);
    const apps = object.apps;
    const __appList: AppListItem[] = []; // BAD NAMING CONVENTION?? BUT NEED TO REPLACE _appList in its entirety FOR LIT TO RERENDER
    apps.forEach((app) => {
      __appList.push({
        app_id: app.app_id,
        app_slug:
          this.appSlugs.find((a) => a.slug == app.app_slug_id) ??
          this.appSlugs[0],
        entity:
          [...Object.values(this.hass.states)].find(
            (e) => e.entity_id == app.entity_id,
          ) ?? null,
      });
    });
    this._appList = __appList;
    this.requestUpdate();
  }

  async firstUpdated() {
    await loadHa();

    this.requestUpdate();
  }

  @property({ type: Object }) public hass!: HomeAssistant;
  @property({ type: Object }) selectedSlug: AppSlug = this.appSlugs[0];
  @property({ type: Object }) selectedEntity: HassEntity | null = null;

  render() {
    if (
      !customElements.get('ha-panel-config') ||
      !customElements.get('ha-menu-button')
    )
      return html` loading... `;

    console.log(this._appList);

    const entities = [...Object.values(this.hass.states)];

    return html`<div>
      <div>
        <div class="header">
          <div class="toolbar">
            <ha-menu-button .hass=${this.hass} .narrow=${true}></ha-menu-button>
            Smartknob - Configuration
          </div>
        </div>
        <div class="content">
          <app-form
            .hass=${this.hass}
            .entities=${entities}
            .appSlugs=${this.appSlugs}
            .appList=${this._appList}
          ></app-form>
        </div>
      </div>
    </div>`;
  }
}
