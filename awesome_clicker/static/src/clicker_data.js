export const CLICKBOT_CLICKS = 10;
export const BIGBOT_CLICKS = 100;
export const BOT_FREQUENCY = 10000; // In milliseconds
export const TREE_FREQUENCY = 30000; // In milliseconds

export const PURCHASABLE_REWARDS = [
    {
        id: "clickbot",
        name: "ClickBot",
        icon: "fa-android",
        category: "Bots",
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
        id: "bigbot",
        name: "BigBot",
        icon: "fa-android",
        category: "Bots",
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
        id: "power-multiplier",
        name: "Power Multiplier",
        icon: "fa-bolt",
        category: "Bots",
        price: 50000,
        minLevel: 3,
        currentNumber: (clicker) => clicker.multiplier,
        buy(clicker) {
            if (clicker.verifyPurchase(3, 50000)) {
                clicker.multiplier++;
            }
        },
    },
    {
        id: "pear-tree",
        name: "Pear Tree",
        icon: "fa-tree",
        category: "Trees",
        price: 1000000,
        minLevel: 4,
        currentNumber: (clicker) => clicker.trees.pear ?? 0,
        buy(clicker) {
            if (clicker.verifyPurchase(4, 1000000)) {
                if (!clicker.trees.pear) {
                    clicker.trees.pear = 0;
                }
                clicker.trees.pear++;
            }
        },
    },
    {
        id: "cherry-tree",
        name: "Cherry Tree",
        icon: "fa-tree",
        category: "Trees",
        price: 1000000,
        minLevel: 4,
        currentNumber: (clicker) => clicker.trees.cherry ?? 0,
        buy(clicker) {
            if (clicker.verifyPurchase(4, 1000000)) {
                if (!clicker.trees.cherry) {
                    clicker.trees.cherry = 0;
                }
                clicker.trees.cherry++;
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
    {
        level: 4,
        clicks: 1000000,
        event: "MILESTONE_1m",
        description: "You can now plant trees.",
    },
];

export const RANDOM_REWARDS = [
    {
        description: "Get 1 click bot",
        apply(clicker) {
            clicker.clickBots += 1;
        },
        maxLevel: 1,
    },
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
