/** @odoo-module **/

import { EventBus } from "@odoo/owl";
import { Reactive } from "@web/core/utils/reactive";

export class ClickerModel extends Reactive {

    constructor() {
        super();
        this.setup(...arguments);
    }

    setup(bus) {
        this.clicks = 0;
        this.level = 0;
        this.clickBots = 0;
        this.bigBots = 0;
        this.power = 1;
        this.bus = bus;
        setInterval(() => {
            this.increment((10 * this.clickBots + 100 * this.bigBots) * this.power);
        }, 10_000);
    }

    increment(inc) {
        this.clicks += inc;
        if (this.level == 0 && this.clicks >= 1000) {
            this.level = 1
            this.bus.trigger("MILESTONE_1k"); 
        }
        if (this.level == 1 && this.clicks >= 5000) {
            this.level = 2
            this.bus.trigger("MILESTONE_5k"); 
        }
        if (this.level == 2 && this.clicks >= 100_000) {
            this.level = 3
            this.bus.trigger("MILESTONE_100k"); 
        }
    }
    
    buyClickBot() {
        this.clicks -= 1000;
        this.clickBots++;
    }

    buyBigBot() {
        this.clicks -= 5000;
        this.bigBots++;
    }

    buyPower() {
        this.clicks -= 50_000;
        this.power++;
    }
}