import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "./click_rewards";
import { choose } from "./utils";

export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.clicks = 0;
        this.level = 0;
        this.bus = new EventBus();
        this.bots = {
            clickbot: {
                price: 1000,
                level: 1,
                increment: 10,
                purchased: 0,
            },
            bigbot: {
                price: 5000,
                level: 2,
                increment: 100,
                purchased: 0,
            }
        }
        this.trees = {
            pearTree: {
                price: 1000000,
                level: 4,
                produce: "pear",
                purchased: 0,
            },
            cherryTree: {
                price: 1000000,
                level: 4,
                produce: "cherry",
                purchased: 0,
            },
        }
        this.fruits = {
            pear: 0,
            cherry: 0,
        },
        this.multiplier = 1


        document.addEventListener("click", () => this.increment(1), true);
        setInterval(() => {
            for (const bot in this.bots) {
                this.clicks += this.bots[bot].increment * this.bots[bot].purchased * this.multiplier;
            }
        }, 10000);

        setInterval(() => {
            for (const tree in this.trees) {
                this.fruits[this.trees[tree].produce] += this.trees[tree].purchased;
            }
        }, 30000);
    }

    buyMultiplier() {
        if (this.clicks < 50000) {
            return false;
        }
        this.clicks -= 50000;
        this.multiplier++;
    }

    increment(inc) {
        this.clicks += inc;
        if (
            this.milestones[this.level] &&
            this.clicks >= this.milestones[this.level].clicks
        ) {
            this.bus.trigger("MILESTONE", this.milestones[this.level]);
            this.level += 1;
        }
    }

    buyBot(name) {
        if (!Object.keys(this.bots).includes(name)) {
            throw new Error(`Invalid bot name ${name}`);
        }
        if (this.clicks < this.bots[name].price) {
            return false;
        }

        this.clicks -= this.bots[name].price;
        this.bots[name].purchased += 1;
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

    buyTree(name) {
        if (!Object.keys(this.trees).includes(name)) {
            throw new Error(`Invalid tree name ${name}`);
        }
        if (this.clicks < this.trees[name].price) {
            return false;
        }
        this.clicks -= this.trees[name].price;
        this.trees[name].purchased += 1;
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

    get milestones() {
        return [
            { clicks: 1000, unlock: "clickBot" },
            { clicks: 5000, unlock: "bigBot" },
            { clicks: 100000, unlock: "power multiplier" },
            { clicks: 1000000, unlock: "pear tree & cherry tree" },
        ];
    }
}
