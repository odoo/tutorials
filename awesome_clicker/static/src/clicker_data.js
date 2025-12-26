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
        currentNumber: (clickerModel) => clickerModel.clickBots,
        buy(clickerModel) {
            if (clickerModel.verifyPurchase(1, 1000)) {
                clickerModel.clickBots++;
            }
        },
    },
    {
        name: "bigbot",
        icon: "fa-android",
        clicks: BIGBOT_CLICKS,
        price: 5000,
        minLevel: 2,
        currentNumber: (clickerModel) => clickerModel.bigBots,
        buy(clickerModel) {
            if (clickerModel.verifyPurchase(2, 5000)) {
                clickerModel.bigBots++;
            }
        },
    },
    {
        name: "bot power",
        icon: "fa-bolt",
        price: 50000,
        minLevel: 3,
        currentNumber: (clickerModel) => clickerModel.multiplier,
        buy(clickerModel) {
            if (clickerModel.verifyPurchase(3, 50000)) {
                clickerModel.multiplier++;
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
