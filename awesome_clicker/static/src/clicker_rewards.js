export const rewards = [
   {
      description: "Get 100 click bot",
      apply(clicker) {
            clicker.increment(100);
      },
      maxLevel: 3,
   },
   {
      description: "Get 1 Big bot",
      apply(clicker) {
            clicker.buyBigBot(10);
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
