export const rewards = [
    {
        description: "You got 100 clicks!",
        apply(clicker) {
            clicker.increment(100);
        },
        maxLevel: 2,
    },
    {
        description: "You got 1500 clicks!",
        apply(clicker) {
            clicker.increment(1500);
        },
        minLevel: 2,
        maxLevel: 4,
    },
    {
        description: "You got 4000 clicks!",
        apply(clicker) {
            clicker.increment(4000);
        },
        minLevel: 3,
    },
    {
        description: "You got an extra power level!",
        apply(clicker) {
            clicker.power += 1;
        },
        minLevel: 3,
    },
];
