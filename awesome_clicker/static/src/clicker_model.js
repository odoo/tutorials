/** @odoo-module **/

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";

export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.bus = new EventBus();
        this._first1KMilestoneTriggered = false;
        this.clicks = 0;
        this.clickBots = 0;
        this.bigClickBots = 0;
        this.level = 0;
        this.power = 1;

        setInterval(() => this.increment(this.clickBots * 10 * this.power), 1000 * 20);
        setInterval(() => this.increment(this.bigClickBots * 100 * this.power), 1000 * 10);
    }

    increment(inc) {
        this.clicks += inc;
        console.log(this.clicks);
        if (this.clicks > 1000 && !this._first1KMilestoneTriggered) {
            this.level = 1;
            this._first1KMilestoneTriggered = true;
            console.log("TRIGGERING");
            this.bus.trigger("MILESTONE_1k");
        }
        if (this.level === 1 && this.clicks > 5_000) {
            this.level++;
        } else if (this.level === 2 && this.clicks > 100_000) {
            this.level++;
        }
    }

    incrementClickBots(inc) {
        this.clickBots += inc;
        this.increment(-inc * 1000);
    }
    incrementBigClickBots(inc) {
        this.bigClickBots += inc;
        this.increment(-inc * 5000);
    }

    incrementPower(inc) {
        this.power++;
        this.increment(inc * -50_000);
    }
}
