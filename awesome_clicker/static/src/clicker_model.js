/** @odoo-module **/
import { Reactive } from "@web/core/utils/reactive";


const CLICK_BOT_GAIN = 10;
const CLICK_BOT_COST = 1000;
const BIG_CLICK_BOT_GAIN = 100;
const BIG_CLICK_BOT_COST = 5000;
const POWER_COST = 50000;
export const MILESTONE_1K = "MILESTONE_1K";
export const MILESTONE_5K = "MILESTONE_5K";
export const MILESTONE_100K = "MILESTONE_100K";

export class ClickerModel extends Reactive {
    constructor(bus) {
        super();

        this.count = 0;
        this.level = 0;
        this.clickBots = 0;
        this.bigClickBots = 0;
        this.powerFactor = 1;
        this.bus = bus;

        this.setupIntervals();
    }

    setupIntervals() {
        setInterval(() => {
            this.increment(this.clickBots * CLICK_BOT_GAIN * this.powerFactor);
            this.increment(this.bigClickBots * BIG_CLICK_BOT_GAIN * this.powerFactor);
        }, 1000);
    }

    handleMilestones() {
        if (this.count >= 1000 && this.level < 1) {
            this.bus.trigger(MILESTONE_1K);
            this.level = 1;
        }
        if (this.count >= 5000 && this.level < 2) {
            this.bus.trigger(MILESTONE_5K);
            this.level = 2;
        }
        if (this.count >= 100000 && this.level < 3) {
            this.bus.trigger(MILESTONE_100K);
            this.level = 3;
        }
    }

    increment(inc) {
        this.count += inc;
        this.handleMilestones();
    }

    buyClickBot() {
        if (this.count >= CLICK_BOT_COST) {
            this.increment(-CLICK_BOT_COST);
            this.clickBots += 1;
        }
    }

    buyBigClickBot() {
        if (this.count >= BIG_CLICK_BOT_COST) {
            this.increment(-BIG_CLICK_BOT_COST);
            this.bigClickBots += 1;
        }
    }

    buyPower() {
        if (this.count >= POWER_COST) {
            this.increment(-POWER_COST);
            this.powerFactor++;
        }
    }

    clickBotAvailable() {
        return this.level >= 1;
    }

    clickBotAffordable() {
        return this.count >= CLICK_BOT_COST;
    }

    bigClickBotAvailable() {
        return this.level >= 2;
    }

    bigClickBotAffordable() {
        return this.count >= BIG_CLICK_BOT_COST;
    }

    powerAvailable() {
        return this.level >= 3;
    }

    powerAffordable() {
        return this.count >= POWER_COST;
    }
}