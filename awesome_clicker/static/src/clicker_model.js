import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import {rewards} from "./click_rewards";

export class ClickerModel extends Reactive {

    constructor() {
        super()
        this.clicks = 850
        this.level = 0
        this.clickBots = 0
        this.bigBots = 0
        this.power = 1
        this.bus = new EventBus();
    }

    increment(inc) {
        this.clicks += inc;
        if (this.level < 1 && this.clicks >= 1000) {
            this.level++;
            this.bus.trigger("Level1");
        }
        if (this.level === 1 && this.clicks >= 5000) {
            this.level++;
            this.bus.trigger("Level2")
        }
        if (this.level === 2 && this.clicks >= 100000) {
            this.level++;
            this.bus.trigger("Level3")
        }
    }

    tick() {
        this.increment((this.clickBots * 10 + this.bigBots * 100) * this.power);
    }

    buyClickBot() {
        const clickBotPrice = 1000;
        if (this.clicks < clickBotPrice) {
            return false;
        }
        this.clicks -= clickBotPrice;
        this.clickBots++;
    }

    buyBigBot() {
        const bigBotPrice = 5000;
        if (this.clicks < bigBotPrice) {
            return false;
        }
        this.clicks -= bigBotPrice;
        this.bigBots++;
    }

    buyPower() {
        const powerPrice = 100000;
        if (this.clicks < powerPrice) {
            return false
        }
        this.clicks -= powerPrice;
        this.power++;
    }

    giveReward() {
        const validRewards = rewards.filter((r) => r.maxLevel >= this.level && r.minLevel <= this.level);
        console.log(validRewards);
        const reward = validRewards[Math.floor(Math.random() * validRewards.length)];
        console.log(reward)
        this.bus.trigger("Reward", reward)
    }
}