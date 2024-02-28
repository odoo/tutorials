/** @odoo-module */

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "./clicker_rewards";
import { choose } from "./utils";

export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.bus = new EventBus();
        this.clicks = 0;
        this.level = 0;
        this.power = 1;
        this.bots = {
            clickbot: {
                price: 1000,
                level: 1,
                increment: 10,
                purchased: 0
            },
            bigbot: {
                price: 5000,
                level: 2,
                increment: 100,
                purchased: 0
            }
        };

        setInterval(() => {
            for (const bot in this.bots) {
                this.clicks += this.bots[bot].increment * this.bots[bot].purchased * this.power;
            }
        }, 10000)

        document.addEventListener("click", () => this.increment(1), true);
    }

    giveReward() {
        const availableRewards = [];
        for(const reward of rewards) {
            if(reward.minLevel <= this.level || !reward.minLevel) {
                if(reward.maxLevel >= this.level || !reward.maxLevel) {
                    availableRewards.push(reward);
                }
            }
        }

        const reward = choose(availableRewards);
        this.bus.trigger("REWARD", reward);
        return reward;
    }

    increment(count) {
        this.clicks += count;
        if (
            this.milestones[this.level] &&
            this.clicks >= this.milestones[this.level].clicks
        ) {
            this.bus.trigger("MILESTONE", this.milestones[this.level]);
            this.level += 1;
        }
    }

    buyMultiplier() {
        if (this.clicks < 50000) {
            return false;
        }
        this.clicks -= 50000;
        this.power++;
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

    get milestones() {
        return [
            { clicks: 1000, unlock: "clickBot" },
            { clicks: 5000, unlock: "bigBot" },
            { clicks: 100000, unlock: "power multiplier"}
        ];
    }
}
