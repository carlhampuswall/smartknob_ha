// import { getAsyncAppSlugs } from './data/websockets';
// import { AppSlug, SelectOption, SelectSelector } from './types';

import { Tab } from './types';

// import { HomeAssistant } from './types';

// // const appSlugs = [];

// // const options: SelectOption[] = .map((slug) => {
// //   return {
// //     value: slug.slug,
// //     label: slug.friendlyName,
// //   };
// // });

// // const selectSelector: SelectSelector = {
// //   select: {
// //     custom_value: false,
// //     mode: 'dropdown',
// //     options,
// //   },
// // };

// export class Const {
//   static instance: Const;
//   readonly hass: HomeAssistant;
//   readonly appSlugs: AppSlug[];
//   readonly selectSelector: SelectSelector = {};

//   private constructor(hass: HomeAssistant) {
//     console.log('Const constructor');
//     this.hass = hass;
//     // this.appSlugs = [];

//     const options: SelectOption[] = this.appSlugs.map((slug) => {
//       return {
//         value: slug.slug_id,
//         label: slug.friendly_name,
//       };
//     });

//     this.selectSelector = {
//       select: {
//         custom_value: false,
//         mode: 'dropdown',
//         options,
//       },
//     };
//   }

//   static async getInstance(hass: HomeAssistant) {
//     if (!Const.instance) {
//       Const.instance = new Const(hass);
//     }

//     return Const.instance;
//   }

//   // readonly appSlugs = appSlugs;

//   // readonly options = options;

//   // readonly selectSelector = selectSelector;
// }

export const DOMAIN = 'smartknob';

export const TABS: Tab[] = [
  {
    tabId: 'setup',
    tabName: 'Setup',
  },
  {
    tabId: 'configuration',
    tabName: 'Configuration',
  },
];
