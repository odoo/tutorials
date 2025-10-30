export const rewards = [
    {
        description: "Get 1 click bot",
        apply(clicker) {
            clicker.bots.clickbot.purchased++;
        },
        maxLevel: 3,
    },
    {
        description: "Get 1 big bot",
        apply(clicker) {
            clicker.bots.bigbot.purchased++;
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
