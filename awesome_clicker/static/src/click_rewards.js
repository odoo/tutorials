/** @odoo-module **/

export const rewards = [
    {
        description: "Get 100 clicks",
        apply(clicker) {
              clicker.increment(100);
        },
        maxLevel: 3,
    },
    {
       description: "Get 1 click bot",
       apply(clicker) {
             clicker.clickBots++;
       },
       minLevel: 1,
       maxLevel: 3,
    },
    {
       description: "Get 10 click bot",
       apply(clicker) {
             clicker.clickBots += 10;
       },
       minLevel: 2,
       maxLevel: 4,
    },
    {
       description: "Increase bot power!",
       apply(clicker) {
             clicker.power++;
       },
       minLevel: 3,
    },
 ];