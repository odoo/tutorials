export const rewards = [
   {
      description: "Get 1 click bot",
      apply(clicker) {
            clicker.bots["clickBots"].number += 1;
      },
      maxLevel: 2,
   },
   {
      description: "Get 10 click bot",
      apply(clicker) {
            clicker.bots["clickBots"].number += 10;
      },
      minLevel: 1,
      maxLevel: 3,
   },
   {
      description: "Get 5 big bot",
      apply(clicker) {
            clicker.bots["bigBots"].number += 5;
      },
      minLevel: 2,
      maxLevel: 4,
   },
   {
      description: "Increase bot power!",
      apply(clicker) {
            clicker.power += 1;
      },
      minLevel: 3,
   },
   {
      description: "Increase bot power by 100!",
      apply(clicker) {
            clicker.power += 100;
      },
      minLevel: 4,
   },
   {
      description: "Get a Cherry Tree",
      apply(clicker) {
            clicker.trees["cherryTrees"].number += 1;
      },
      minLevel: 4,
   },
   {
      description: "Get a Pear Tree",
      apply(clicker) {
            clicker.trees["pearTrees"].number += 1;
      },
      minLevel: 4,
   },
   
];
