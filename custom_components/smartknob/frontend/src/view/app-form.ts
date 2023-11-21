import { LitElement, css, html } from 'lit';
import { customElement, property, state } from 'lit/decorators';
import {
  AppListItem,
  AppSlug,
  HomeAssistant,
  SelectOption,
  SelectSelector,
} from '../types';
import { HassEntity } from 'home-assistant-js-websocket';
import '../components/SkReorderableList';
import { mdiPlus } from '@mdi/js';
import { saveApp } from '../data/websockets';

@customElement('app-form')
export class AppForm extends LitElement {
  static styles = css`
    :host {
      display: block;
      max-width: 600px;
    }
    .add-app {
      display: flex;
      gap: 12px;
      padding-bottom: 12px;
    }
  `;

  @property({ type: Object }) hass!: HomeAssistant;
  @property({ type: Array }) entities!: HassEntity[];
  @property({ type: Array }) appSlugs!: AppSlug[];
  @property({ type: Array }) appList!: AppListItem[];

  @state() private _selectedSlug: AppSlug | null = null;
  @state() private _selectedEntity: HassEntity | null = null;
  // @state() private _appList: AppListItem[] = [];
  @state() private _domain: string = '';

  connectedCallback(): void {
    super.connectedCallback();
    this._selectedSlug = this.appSlugs[0];
    this._domain = this._selectedSlug.domain;
  }

  render() {
    const options: SelectOption[] = this.appSlugs.map((slug) => {
      return {
        value: slug.slug,
        label: slug.friendlyName,
      };
    });

    const selectSelector: SelectSelector = {
      select: {
        custom_value: false,
        mode: 'dropdown',
        options,
      },
    };

    return html`
      <form class="add-app" @submit=${this.handleSubmit}>
        <ha-selector
          .hass=${this.hass}
          .selector=${selectSelector}
          .required=${true}
          .label=${'Select App Slug'}
          .value=${this._selectedSlug?.slug}
          @value-changed=${this.appSlugChanged}
        ></ha-selector>
        <ha-selector
          .hass=${this.hass}
          .selector=${{
            entity: {
              include_entities: this.entities.map((entity) => {
                if (!entity.entity_id.startsWith(this._domain)) {
                  return '';
                }
                return entity.entity_id;
              }),
            },
          }}
          .required=${true}
          .value=${this._selectedEntity?.attributes.friendly_name}
          @value-changed=${this.entityChanged}
        ></ha-selector>

        <button type="submit">
          <ha-svg-icon title="submit" .path=${mdiPlus}></ha-svg-icon>
        </button>
      </form>

      <sk-reorderable-list .items="${this.appList}"></sk-reorderable-list>
    `;
  }
  handleSubmit = (e: Event) => {
    e.preventDefault();
    //! VALIDATE INPUTS
    if (!this._selectedSlug || !this._selectedEntity) return; //TODO HANDLE

    const appListItem: AppListItem = {
      app_id: `${this._selectedSlug.slug}-${this._selectedEntity.entity_id}`,
      app_slug: this._selectedSlug,
      entity: this._selectedEntity,
    };
    if (
      !this.appList.find(
        (appEntity) =>
          appEntity.app_slug == appListItem.app_slug &&
          appEntity.entity == appListItem.entity,
      )
    )
      this.appList.push(appListItem);
    this.appList = [...this.appList]; //TODO VALIDATE DATA _entity could be null for example

    saveApp(this.hass, appListItem); //SAVE TO STORAGE

    this.requestUpdate();
  };

  listApps() {
    return html`${this.appList.map((app) => {
      const id = `${app.app_slug.slug}-${app.entity!.entity_id}`;
      return html`<li .id="${id}">
        ${app.app_slug.friendlyName} - ${app.entity!.attributes.friendly_name}
      </li>`;
    })}`;
  }

  appSlugChanged(e: any) {
    //TODO CREATE TYPE MATCHING EVENT LOOK AT COMMENTED TYPE UP TOP ETC https://github.com/home-assistant/frontend/blob/dev/src/common/dom/fire_event.ts#L60
    //!https://github.com/home-assistant/frontend/blob/dev/src/common/dom/fire_event.ts#L60
    this._selectedSlug =
      this.appSlugs.find((app) => app.slug == e.detail.value) ?? null;
    this._domain = this._selectedSlug?.domain ?? '';
    this._selectedEntity = null;
    this.requestUpdate();
  }

  entityChanged(e: any) {
    //TODO CREATE TYPE MATCHING EVENT LOOK AT COMMENTED TYPE UP TOP ETC
    //! https://github.com/home-assistant/frontend/blob/dev/src/common/dom/fire_event.ts#L60
    this._selectedEntity =
      Object.values(this.hass.states).find(
        (entity) => entity.entity_id == e.detail.value,
      ) ?? null;
  }
}
