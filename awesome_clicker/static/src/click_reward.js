const rewards = [
   {
      description: "Get 1 click bot",
      apply(clicker) {
            clicker.increment(1);
      },
      maxLevel: 3,
   },
   {
      description: "Get 10 click bot",
      apply(clicker) {
            clicker.increment(10);
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

export function getReward(clicker) {
   let availables = rewards.filter((reward) => {
      if (reward.minLevel && clicker.level < reward.minLevel) {
         return false
      }
      if (reward.maxLevel && clicker.level > reward.maxLevel) {
         return false
      }
      return true
   });
   if (availables) {
      return availables[Math.floor(Math.random()*availables.length)];
   }
   else {
      return null;
   }
}