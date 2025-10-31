export const rewards = [
    {
        description: "Get 1 click bot",
        apply(clicker) {
            clicker.clickBots += 1;
        },
        minLevel: 0,
        maxLevel: 2,
    },
    {
        description: "Get 10 click bots",
        apply(clicker) {
            clicker.clickBots += 10;
        },
        minLevel: 3,
        maxLevel: 4,
    },
    {
        description: "Increase bot power!",
        apply(clicker) {
            clicker.multipler += 1;
        },
        minLevel: 3,
        maxLevel: 10
    },
];