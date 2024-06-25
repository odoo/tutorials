/** @odoo-module **/

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "../click_rewards.js"


export class ClickerModel extends Reactive {

    constructor() {
        super();

        this.clicks = 110000;
        this.level = 0;
        this.clickBots = 0;
        this.bigBots = 0;
        this.power = 1;

        this.milestones = [1000, 5000, 100000];
        this.bus = new EventBus();
    }

    increment(inc) {
        this.clicks += inc;
            
        if (this.level < 3 && this.clicks >= this.milestones[this.level]) {
            this.level++;
            this.bus.trigger("MILESTONE_REACHED", this.level);
        }
    }

    buyClickBot() {
        this.clickBots++;
        this.clicks -= 1000;
        setInterval(() => this.clicks += 10 * this.power, 10*1000);
    }

    buyBigBot() {
        this.bigBots++;
        this.clicks -= 5000;
        setInterval(() => this.clicks += 100 * this.power, 10*1000);
    }

    getReward() {
        const eligible_rewards = rewards.filter((reward) => (!reward.minLevel || reward.minLevel <= this.level)
             && (!reward.maxLevel || reward.maxLevel >= this.level));
        const reward = eligible_rewards[Math.floor(Math.random() * eligible_rewards.length)];
        this.bus.trigger("REWARD_RECEIVED", reward);
    }
}