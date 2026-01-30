export const rewards = [
    {
        description: "Get 1 ClickBot",
        apply(clicker) {
            clicker.bots.clickbot.quantity++;
        },
        maxLevel: 3,
    },
    {
        description: "Get 1 BigBot",
        apply(clicker) {
            clicker.bots.bigbot.quantity++;
        },
        minLevel: 3,
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
