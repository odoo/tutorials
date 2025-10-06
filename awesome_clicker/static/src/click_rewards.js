export const rewards = [
    {
        description: "Get 1 click bot",
        apply(clicker) {
            clicker.clickBots += 1;
        },
        maxLevel: 3,
    },
    {
        description: "Get 10 click bot",
        apply(clicker) {
            clicker.clickBots += 10;
        },
        minLevel: 3,
        maxLevel: 4,
    },
    {
        description: "Increase power multiplier!",
        apply(clicker) {
            clicker.power += 1;
        },
        minLevel: 3,
    },
    {
        description: "1000 extra clicks!",
        apply(clicker) {
            clicker.increment(1000);
        },
    },
    {
        description: "One Big Bot gifted!",
        apply(clicker) {
            clicker.bigBots += 1;
        },
        minLevel: 2,
    },
];
