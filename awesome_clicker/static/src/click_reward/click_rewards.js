export const rewards = [
   {
      description: "Get 1 click bot",
      apply(clicker) {
            clicker.bots.clickBot.quantity ++;
      },
      minLevel: 1,
      maxLevel: 3,
   },
   {
      description: "Get 100 clicks",
      apply(clicker) {
            clicker.addClicks(100);
      },
      maxLevel: 2,
   },
   {
      description: "Get 10 click bot",
      apply(clicker) {
            clicker.bots.clickBot.quantity += 10;
      },
      minLevel: 3,
      maxLevel: 4,
   },
   {
      description: "Increase bot power!",
      apply(clicker) {
            clicker.power += 1;
      },
      minLevel: 3,
   },
];
