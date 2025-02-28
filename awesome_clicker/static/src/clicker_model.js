import { EventBus } from "@odoo/owl";

import { Reactive } from "@web/core/utils/reactive";

export class ClickerModel extends Reactive {
    constructor() {
        super(...arguments);

        this.clicks = 0;
        this.level = 0;
        this.clickerBots = 0;
        this.clickerBigBots = 0;
        this.power = 1;

        setInterval(() => {
            this.increment((this.clickerBots * 10 + this.clickerBigBots * 100) * this.power);
        }, 10000);

        this.bus = new EventBus();
    }

    increment(inc) {
        this.clicks += inc;
        if (this.clicks >= 1000 && this.level === 0) {
            this.level++;
            this.bus.trigger("MILESTONE_1k");
        }
        if (this.clicks >= 5000 && this.level === 1) {
            this.level++;
            this.bus.trigger("MILESTONE_5k");
        }
        if (this.clicks >= 100000 && this.level === 2) {
            this.level++;
            this.bus.trigger("MILESTONE_100k");
        }
    }

    buyBot() {
        this.clicks -= 1000;
        this.clickerBots += 1;
    }

    buyBigBot() {
        this.clicks -= 5000;
        this.clickerBigBots += 1;
    }

    buyPower() {
        this.clicks -= 50000;
        this.power += 1;
    }
}