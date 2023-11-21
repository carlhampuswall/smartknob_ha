import { mdiDrag } from '@mdi/js';
import { LitElement, css, html } from 'lit';
import { customElement, property } from 'lit/decorators';
import { AppListItem } from '../types';

@customElement('sk-reorderable-list')
export class SkReorderableList extends LitElement {
  static styles = css`
    :host {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    :host > * {
      padding: 12px;
    }
    :host > :nth-child(odd) {
      background-color: var(--secondary-background-color);
    }
    :host > :nth-child(even) {
      background-color: var(--primary-background-color);
    }

    .list-item {
      display: flex;
      flex-direction: row;
      flex-wrap: nowrap;
      align-items: center;
      gap: 12px;
    }
  `;

  @property({ type: Array }) items: AppListItem[] = [];

  render() {
    return html`
      ${this.items.map(
        (item, index) =>
          html`<sk-reorderable-list-item
            .id="${item.app_id}"
            @drop="${this.drop}"
          >
            <div class="list-item">
              <div>${index + 1}</div>
              |
              <div>${item.app_slug.friendlyName}</div>
              |
              <div>${item.entity?.attributes.friendly_name}</div>
            </div>
          </sk-reorderable-list-item> `,
      )}
    `;
  }

  drop(e: any) {
    e.target.classList.remove('over');
    const draggableId = e.dataTransfer?.getData('text/plain');
    const dropId = e.target.getAttribute('draggable-id');

    this.items = this.reorderItems(this.items, draggableId, dropId);

    // TODO Save apps after reordering !?
    // saveApps(this.hass, this.items);

    this.requestUpdate();
  }

  reorderItems(
    items: AppListItem[],
    draggedId: string,
    dropId: string,
  ): AppListItem[] {
    const draggableIndex = items.findIndex((item) => item.app_id === draggedId);
    const dropIndex = items.findIndex((item) => item.app_id === dropId);

    const [draggedItem] = items.splice(draggableIndex, 1);
    items.splice(
      draggableIndex < dropIndex ? dropIndex : dropIndex,
      0,
      draggedItem,
    );

    return items;
  }
}

@customElement('sk-reorderable-list-item')
export class SkReorderableListItem extends LitElement {
  static styles = css`
    :host {
      display: flex;
      flex-direction: row;
      flex-wrap: nowrap;
      align-items: center;
      justify-content: space-between;
      user-select: none;
      cursor: grab;
    }
    :host(.over) {
      border-bottom: 4px solid var(--primary-color);
    }
    [draggable] {
      opacity: 1;
    }
  `;

  @property() id!: string;
  @property({ type: Boolean }) isDraggable?: boolean = true;

  connectedCallback() {
    super.connectedCallback();

    this.addEventListener('dragstart', this.dragStart);
    this.addEventListener('dragenter', this.dragEnter);
    this.addEventListener('dragover', this.dragOver);
    this.addEventListener('dragleave', this.dragLeave);
    this.addEventListener('dragend', this.dragEnd);

    this.setAttribute('draggable', 'true');
  }

  render() {
    this.setAttribute('draggable-id', this.id);
    return html` <slot></slot
      ><ha-svg-icon title="draggable" .path=${mdiDrag}></ha-svg-icon>`;
  }
  dragStart(e: any) {
    this.style.opacity = '0.4';
    e.dataTransfer?.setData('text/plain', this.id);
    e.dataTransfer!.effectAllowed = 'move';

    this.classList.add('draggable-content');
    e.target.classList.add('over');
  }

  dragEnter(e: any) {
    e.preventDefault();
    e.target.classList.add('over');
  }

  dragOver(e: any) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }

  dragLeave(e: any) {
    e.preventDefault();
    e.target.classList.remove('over');
  }

  dragEnd(e: any) {
    this.style.opacity = '1';
    e.target.classList.remove('over');
    this.requestUpdate();
  }
}
