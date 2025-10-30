import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "./clicker_reward";
import { choose } from "./utils";
import { CURRENT_VERSION } from "./clicker_migration";

export class ClickerModel extends Reactive {

    constructor() {
        super();
        this.version = CURRENT_VERSION;
        this.clicks = 0;
        this.level = 0;
        this.power = 1;
        this.bots = {
            clickbot: {
                price: 1000,
                increment: 10,
                purchased: 0,
                level: 1,
            },
            bigbot: {
                price: 5000,
                increment: 100,
                purchased: 0,
                level: 2,
            }
        };
        this.trees = {
            pearTree: {
                price: 1000000,
                level: 4,
                purchased: 0,
                fruit: "pear",
            },
            cherryTree: {
                price: 1000000,
                level: 4,
                purchased: 0,
                fruit: "cherry",
            },
            appleTree: {
                price: 1000000,
                level: 4,
                purchased: 0,
                fruit: "apple",
            },
            peachTree: {
                price: 1500000,
                level: 4,
                fruit: "peach", 
                purchased: 0,
            }
        };
        this.fruits = {
            pear: 0,
            cherry: 0,
            apple: 0,
            peach: 0,

        }
        this.bus = new EventBus();
    }

    ticks() {
        for (const bot in this.bots) {
            this.clicks += this.bots[bot].purchased * this.bots[bot].increment * this.power;
        }
    }

    updateFruits() {
        for (const tree in this.trees) {
            this.fruits[this.trees[tree].fruit] += this.trees[tree].purchased;
        }
    }

    increment(incr) {
        this.clicks += incr;
        if (this.level < 1 && this.clicks >= 1000) {
            this.bus.trigger("MILESTONE_1k");
            this.level++;
        }
        if (this.level < 2 && this.clicks >= 5000) {
            this.bus.trigger("MILESTONE_5k");
            this.level++;
        }
        if (this.level < 3 && this.clicks >= 100000) {
            this.bus.trigger("MILESTONE_100k");
            this.level++;
        }
        if (this.level < 4 && this.clicks >= 1000000) {
            this.bus.trigger("MILESTONE_1M");
            this.level++;
        }
    };

    buyBot(bot) {
        if (this.clicks < this.bots[bot].price){
            return false;
        }
        this.clicks -= this.bots[bot].price;
        this.bots[bot].purchased++;
    };

    buyPower() {
        if (this.clicks < 50000){
            return false;
        }
        this.power++;
        this.clicks -= 50000;
    }

    buyTree(tree) {
        if (this.clicks < 1000000){
            return false;
        }
        this.trees[tree].purchased++;
        this.clicks -= 1000000;
    }

    giveReward() {
        const availableRewards = [];
        for (const reward of rewards) {
            if (reward.minLevel <= this.level || !reward.minLevel){
                if (reward.maxLevel >= this.level || !reward.maxLevel){
                    availableRewards.push(reward);
                }
            }
        }
        const reward = choose(availableRewards);
        this.bus.trigger("REWARD", reward);
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
}
