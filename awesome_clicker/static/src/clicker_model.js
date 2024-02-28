/** @odoo-module **/

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "./click_rewards";
import { chooseReward } from "./utils";

export class ClickerModel extends Reactive {

    constructor() {
        super();
        this.state = {
            clicks: 0,
            level: 0,
            bots : Object.fromEntries(Object.keys(this.bots).map(key => [key, 0])),
            power: 1,
            unlockedRewards: []
        }
        this.bus = new EventBus();
        document.addEventListener("click", () => this.increment(1));
        setInterval(() => this.state.clicks += this.state.bots["clickbot"] * 10 * this.state.power, 10 * 1000);
        setInterval(() => this.state.clicks += this.state.bots["bigbot"] * 100 * this.state.power, 10 * 1000);
    }

    getReward() {
        let availableRewards = [];
        for (const reward in rewards) {
            if (!reward.minLevel || reward.minLevel <= this.state.level && !reward.maxLevel || reward.maxLevel >= this.state.level) {
                availableRewards.push(reward);
            }
        }
        const reward = chooseReward(availableRewards);
        this.bug.trigger("REWARD", reward);
        return reward;
    }

    increment(inc) {
        this.state.clicks += inc;
        if (this.state.level < 1 && this.state.clicks >= 1000) {
            this.bus.trigger("MILESTONE_1K");
            this.state.level++;
        }
        if (this.state.level < 2 && this.state.clicks >= 5000) {
            this.state.level++;
        }
        if (this.state.level < 3 && this.state.click >= 100000) {
            this.state.level++;
        }
    }

    buyBot(type){
        if (this.state.clicks < this.bots[type].price) {
            return false;
        }
        this.state.clicks -= this.bots[type].price;
        this.state.bots[type] += 1;
    }

    purchasePowerLevel() {
        const POWER_LEVEL_PRICE = 50000;
        this.state.power++;
        this.state.clicks -= POWER_LEVEL_PRICE;
    }

    bots = {
        clickbot: {
            price: 1000,
            level: 1,
            increment: 10,
        },
        bigbot: {
            price: 5000,
            level: 2,
            increment: 100,
        }
    }

    milestones = [
        { clicks: 1000, unlock: "clickBot" },
        { clicks: 5000, unlock: "bigBot" },
        { clicks: 100000, unlock: "power multiplier" },
    ];

};

