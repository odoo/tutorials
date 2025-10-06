/** @odoo-module **/
import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "../click_rewards";
import { choose } from "../utils";
import { CURRENT_VERSION } from "../clicker_migration";

export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.version = CURRENT_VERSION;
        this.clicks = 0;
        this.level = 0;
        this.clickBots = 0;
        this.bigBots = 0;
        this.powerBots = 1;
        this.trees = {
            pear: {
                count: 0,
                fruits: 0,
            },
            cherries: {
                count: 0,
                fruits: 0,
            },
            peach: {
                count: 0,
                fruits: 0,
            },
        }
        this.bus = new EventBus();

        document.addEventListener("click", () => this.increment(1), true);

        setInterval(() => {
            this.clicks += 10 * this.clickBots * this.powerBots;
        }, 10000);

        setInterval(() => {
            this.clicks += 100 * this.bigBots * this.powerBots;
        }, 10000);

        setInterval(() => {
            for (const tree of Object.values(this.trees)) {
                if (tree.count > 0) {
                    tree.fruits += tree.count;
                }
            }
        }, 30000);

    }

    toJSON() {
        const json = Object.assign({}, this);
        delete json["bus"];
        return json;
    }

    static fromJSON(json) {
        const clicker = new ClickerModel();
        const clickerInstance = Object.assign(clicker, json);
        return clickerInstance;
    }

    totalTrees() {
        return Object.values(this.trees).reduce((acc, tree) => acc + tree.count, 0);
    }

    totalFruits() {
        return Object.values(this.trees).reduce((acc, tree) => acc + tree.fruits, 0);
    }

    increment(inc) {
        this.clicks += inc;
        if (this.level < 1 && this.clicks >= 1000) {
            this.bus.trigger("MILESTONE_1k");
            this.level = 1;
        } else if (this.level === 1 && this.clicks >= 5000) {
            this.level = 2;
        } else if (this.level === 2 && this.clicks >= 50000) {
            this.level = 3;
        } else if (this.level === 3 && this.clicks >= 1000000) {
            this.level = 4;
        }
    }

    buyTree(type) {
        const price = 1000000;
        if (this.clicks < price) {
            return false;
        }
        if (this.trees[type]) {
            this.trees[type].count += 1;
        }
        this.clicks -= price;
    }

    buyBot(type) {
        const botConfigs = {
            click: { price: 1000, key: "clickBots" },
            big: { price: 5000, key: "bigBots" },
            power: { price: 50000, key: "powerBots" },
        };

        const bot = botConfigs[type];
        if (!bot || this.clicks < bot.price) {
            return false;
        }

        this.clicks -= bot.price;
        this[bot.key] += 1;
        return true;
    }

    giveReward() {
        const availableReward = [];
        for (const reward of rewards) {
            if (reward.minLevel <= this.level || !reward.minLevel) {
                if (reward.maxLevel >= this.level || !reward.maxLevel) {
                    availableReward.push(reward);
                }
            }
        }
        const reward = choose(availableReward);
        this.bus.trigger("REWARD", reward);
        return choose(availableReward);
    }
}
