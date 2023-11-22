import './types';
import { html, css, LitElement } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

import './view/app-form';
import { AppListItem, AppSlug, HomeAssistant } from './types';
import { loadHa } from './load-ha-elements';
import { getAsyncAppSlugs, getAsyncApps } from './data/websockets';

import './const';

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

  @property({ type: Object }) public hass!: HomeAssistant;
  @state() private _appSlugs: AppSlug[] = [];
  @state() private _appList: AppListItem[] = [];

  async connectedCallback() {
    const loadedAppSlugs = (await getAsyncAppSlugs(this.hass)).app_slugs;

    const loadedApps = (await getAsyncApps(this.hass)).apps;
    const __appList: AppListItem[] = []; // BAD NAMING CONVENTION?? BUT NEED TO REPLACE _appList in its entirety FOR LIT TO RERENDER
    loadedApps.forEach((app) => {
      const _appSlug =
        loadedAppSlugs.find((a) => a.slug_id == app.app_slug_id) ??
        loadedAppSlugs[0];
      const _entity =
        [...Object.values(this.hass.states)].find(
          (e) => e.entity_id == app.entity_id,
        ) ?? null;
      __appList.push({
        app: {
          app_id: app.app_id,
          app_slug_id: app.app_slug_id,
          entity_id: app.entity_id,
        },
        app_slug: _appSlug,
        entity: _entity,
      });
    });
    this._appList = __appList;
    this._appSlugs = loadedAppSlugs;

    super.connectedCallback();

    this.requestUpdate();
  }

  async firstUpdated() {
    await loadHa();

    this.requestUpdate();
  }

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
            .appSlugs=${this._appSlugs}
            .apps=${this._appList}
          ></app-form>
        </div>
      </div>
    </div>`;
  }
}
