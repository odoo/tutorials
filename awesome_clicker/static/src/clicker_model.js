/** @odoo-module **/

import { EventBus } from "@odoo/owl";
import { Reactive } from "@web/core/utils/reactive";
import { browser } from "@web/core/browser/browser";

const rewards = [
    {
        description: "Get 6 clicks",
        apply(clicker) {
            clicker.click(6);
        },
        availability(clicker) {
            return clicker.level <= 3;
        },
    },
    {
        description: "Get 42 clicks",
        apply(clicker) {
            clicker.click(42);
        },
        availability(clicker) {
            return 3 <= clicker.level;
        },
    },
    {
        description: "Enable Mini bot",
        apply(clicker) {
            if (clicker.bots.findIndex((bot) => bot.amount == 1) == -1) {
                clicker.bots.push({
                    name: "minibot",
                    amount: 1,
                    delay: 3,
                    price: 100,
                    count: 0,
                });
            }
        },
        availability(clicker) {
            return clicker.bots.findIndex((bot) => bot.amount == 1) == -1;
        },
    },
    {
        description: "Increase multiplier",
        apply(clicker) {
            clicker.multiplier += 1;
        },
        availability(clicker) {
            return 1 <= clicker.multiplier && clicker.multiplier <= 10;
        },
    },
];

const peachTree = {
    name: "Peach tree",
    fruitsName: "Peaches",
    amount: 1,
    delay: 42,
    price: 1234567,
    count: 0,
    fruitCount: 0,
};

const levels = [
    {
        condition(clicker) {
            return 1000 <= clicker.clicks;
        },
        effect(clicker) {
            clicker.bots.push({
                name: "clickbot",
                amount: 10,
                delay: 10,
                price: 1000,
                count: 0,
            });
            clicker.bus.trigger("MILESTONE_1k");
        },
    },
    {
        condition(clicker) {
            return 5000 <= clicker.clicks;
        },
        effect(clicker) {
            clicker.bots.push({
                name: "bigbot",
                amount: 100,
                delay: 10,
                price: 5000,
                count: 0,
            });
        },
    },
    {
        condition(clicker) {
            return 100000 <= clicker.clicks;
        },
        effect(clicker) {
            clicker.multiplier = 1;
        },
    },
    {
        condition(clicker) {
            return 1000000 <= clicker.clicks;
        },
        effect(clicker) {
            clicker.trees.push({
                name: "Pear tree",
                fruitsName: "Pears",
                amount: 1,
                delay: 30,
                price: 1000000,
                count: 0,
                fruitCount: 0,
            });
            clicker.trees.push({
                name: "Cherry tree",
                fruitsName: "Cherries",
                amount: 1,
                delay: 30,
                price: 1000000,
                count: 0,
                fruitCount: 0,
            });
            clicker.trees.push(peachTree);
        },
    },
];

const migrations = [
    {
        name: "Add peach trees",
        fromVersion: 1,
        toVersion: 2,
        apply(backup) {
            if (backup.level >= 4) {
                backup.trees.push(peachTree);
            }
        },
    },
];
const currentVersion = 2;

function migrate(backup) {
    for (const migration of migrations) {
        if (backup.version === migration.fromVersion) {
            console.log("Running migration: " + migration.name)
            migration.apply(backup);
            backup.version = migration.toVersion;
        }
    }
    return backup;
}

export class ClickerModel extends Reactive {

    constructor(backup) {
        super();
        migrate(backup);
        this.clicks = backup.clicks || 0;
        this.level = backup.level || 0;
        this.bots = backup.bots || [];
        this.multiplier = backup.multiplier || false;
        this.multiplierPrice = backup.multiplierPrice || 50000;
        this.trees = backup.trees || [];
        this.version = currentVersion;
        this.bus = new EventBus();

        browser.addEventListener("click", (ev) => this.captureClick(ev), { capture: true });

        for (const bot of this.bots) {
            const count = bot.count;
            browser.setInterval(
                () => this.click(this.effectiveBotAmount(bot) * count),
                bot.delay * 1000,
            );
        }
        for (const tree of this.trees) {
            const count = tree.count;
            browser.setInterval(
                () => tree.fruitCount += count,
                tree.delay * 1000,
            );
        }
    }

    captureClick(ev) {
        const count = ev.target.attributes.getNamedItem("click-count")?.value || 1;
        this.click(1 * count);
    }

    click(count) {
        this.clicks += count || 1;
        const current = levels[this.level];
        if (current && current.condition(this)) {
            current.effect(this);
            this.level += 1;
        }
    }

    effectiveBotAmount(bot) {
        return bot.amount * (this.multiplier || 1);
    }

    checkBuyBot(bot) {
        return bot.price <= this.clicks;
    }

    buyBot(bot) {
        if (!this.checkBuyBot(bot)) {
            throw new Error("Not enough clicks to buy a " + bot.name);
        }
        this.clicks -= bot.price;
        bot.count += 1;
        browser.setInterval(
            () => this.click(this.effectiveBotAmount(bot)),
            bot.delay * 1000,
        );
    }

    checkBuyMultiplier() {
        return this.multiplierPrice <= this.clicks;
    }

    buyMultiplier() {
        if (!this.checkBuyMultiplier()) {
            throw new Error("Not enough clicks to buy a multiplier");
        }
        this.clicks -= this.multiplierPrice;
        this.multiplier += 1;
    }

    checkBuyTree(tree) {
        return tree.price <= this.clicks;
    }

    buyTree(tree) {
        if (!this.checkBuyTree(tree)) {
            throw new Error("Not enough clicks to buy a " + tree.name);
        }
        this.clicks -= tree.price;
        tree.count += 1;
        browser.setInterval(
            () => tree.fruitCount += 1,
            tree.delay * 1000,
        );
    }
    
    treeCount() {
        return this.trees.reduce((acc, t) => acc + t.count, 0);
    }

    fruitCount() {
        return this.trees.reduce((acc, t) => acc + t.fruitCount, 0);
    }

    giveReward() {
        const available = [];
        for (const reward of rewards) {
            if (reward.availability(this)) {
                available.push(reward);
            }
        }
        return available[Math.floor(Math.random() * available.length)];
    }
}
