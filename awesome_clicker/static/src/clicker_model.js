import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "./click_rewards";
import { choose } from "./utils";
import { CURRENT_VERSION } from "./clicker_migration";

export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.version = CURRENT_VERSION;
        this.clicks = 0;
        this.level = 0;
        this.power = 1;
        this.bus = new EventBus();
        this.milestones = [
            { clicks: 1000, unlock: "ClickBots" },
            { clicks: 5000, unlock: "BigBots"},
            { clicks: 100000, unlock: "Power multipliers"},
            { clicks: 1000000, unlock: "Trees" }
        ]
        this.bots = [
            { name: "Click Bot", price: 1000, amount: 0, clicks: 10 },
            { name: "Big Bot", price: 5000, amount: 0, clicks: 100 },
        ]
        this.trees = [
            { fruit: "Pear", price: 1000000, amount: 0, fruit_number: 0 },
            { fruit: "Cherry", price: 1000000, amount: 0, fruit_number: 0 },
            { fruit: "Apple", price: 1000000, amount: 0, fruit_number: 0 },
            { fruit: "Orange", price: 1000000, amount: 0, fruit_number: 0 },
            { fruit: "Peach", price: 1000000, amount: 0, fruit_number: 0 },
        ]
    }

    increment(inc) {
        this.clicks += inc;
        if (this.milestones[this.level] &&this.clicks >= this.milestones[this.level].clicks) {
            this.bus.trigger("MILESTONE", this.milestones[this.level]);
            this.level += 1;
            this.getReward()
        }
    }

    buyBot(bot) {
        if (this.clicks >= bot.price) {
            bot.amount++;
            this.clicks -= bot.price;
        }
    }

    buyClickBot() {
        this.buyBot(this.bots[0]);
    }

    buyBigBot() {
        this.buyBot(this.bots[1]);
    }

    buyPower() {
        if (this.clicks >= 50000) {
            this.power++;
            this.clicks -= 50000;
        }
    }

    buyTree(tree) {
        if (this.clicks >= tree.price) {
            tree.amount++;
            this.clicks -= tree.price;
        }
    }

    getReward() {
        const reward = choose(this, rewards);
        this.bus.trigger("REWARD", reward);
    }

    getTotalTrees() {
        let total = 0;
        this.trees.forEach((tree) => total += tree.amount)
        return total;
    }

    getTotalFruits() {
        let total = 0;
        this.trees.forEach((tree) => total += tree.fruit_number)
        return total;
    }

    toJSON() {
        const json = Object.assign({}, this);
        delete json["bus"];
        return json;
    }
}
