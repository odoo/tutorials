export const CLICKBOT_CLICKS = 10;
export const BIGBOT_CLICKS = 100;
export const BOT_FREQUENCY = 10000; // In milliseconds

export const PURCHASABLE_REWARDS = [
    {
        name: "clickbot",
        icon: "fa-android",
        clicks: CLICKBOT_CLICKS,
        price: 1000,
        minLevel: 1,
        currentNumber: (clicker) => clicker.clickBots,
        buy(clicker) {
            if (clicker.verifyPurchase(1, 1000)) {
                clicker.clickBots++;
            }
        },
    },
    {
        name: "bigbot",
        icon: "fa-android",
        clicks: BIGBOT_CLICKS,
        price: 5000,
        minLevel: 2,
        currentNumber: (clicker) => clicker.bigBots,
        buy(clicker) {
            if (clicker.verifyPurchase(2, 5000)) {
                clicker.bigBots++;
            }
        },
    },
    {
        name: "bot power",
        icon: "fa-bolt",
        price: 50000,
        minLevel: 3,
        currentNumber: (clicker) => clicker.multiplier,
        buy(clicker) {
            if (clicker.verifyPurchase(3, 50000)) {
                clicker.multiplier++;
            }
        },
    },
];

// Ordered milestones
export const MILESTONES = [
    {
        level: 1,
        clicks: 1000,
        event: "MILESTONE_1k",
        description: "You can now buy clickbots.",
    },
    {
        level: 2,
        clicks: 5000,
        event: "MILESTONE_5k",
        description: "You can now buy bigbots.",
    },
    {
        level: 3,
        clicks: 100000,
        event: "MILESTONE_100k",
        description: "You can now increase your bots' power.",
    },
];

export const RANDOM_REWARDS = [
    {
        description: "Get 3 click bots",
        apply(clicker) {
            clicker.clickBots += 3;
        },
        minLevel: 1,
        maxLevel: 2,
    },
    {
        description: "Get 3 big bots",
        apply(clicker) {
            clicker.bigBots += 3;
        },
        minLevel: 2,
    },
    {
        description: "Get 10 big bots",
        apply(clicker) {
            clicker.bigBots += 10;
        },
        minLevel: 3,
    },
    {
        description: "Increase bot power!",
        apply(clicker) {
            clicker.multipler += 1;
        },
        minLevel: 3,
    },
];
