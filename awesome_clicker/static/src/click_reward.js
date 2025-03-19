import { choose } from "./utils";


const rewards = [
    {
        description: "Get 1 click bot",
        apply(clicker) {
            clicker.increment(1);
        },
        maxLevel: 3,
    },
    {
        description: "Get 10 click bots",
        apply(clicker) {
            clicker.increment(10);
        },
        minLevel: 3,
        maxLevel: 4,
    },
    {
        description: "Increase bot power",
        apply(clicker) {
            clicker.power += 1;
        },
        minLevel: 3,
    },
];

export function getReward(level){
    const availableRewards = rewards.filter((reward) => {
        return (level >= (reward?.minLevel || level)) && (level <= (reward?.maxLevel || level));
    });
    return choose(availableRewards);
}
