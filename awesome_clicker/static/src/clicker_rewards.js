/** @odoo-module **/

export const rewards = [
   {
      description: "Get 1 click bot",
      apply(clicker) {
         clicker.buy("clickBots");
      },
      minLevel: 1,
      maxLevel: 3,
   },
   {
      description: "Get 10 click bot",
      apply(clicker) {
         clicker.buy("clickBots", 0,10);
      },
      minLevel: 3,
      maxLevel: 4,
   },
   {
      description: "Increase bot power!",
      apply(clicker) {
         clicker.buy("power");
      },
      minLevel: 3,
   },
];