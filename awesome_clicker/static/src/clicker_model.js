import { EventBus } from "@odoo/owl";

import { Reactive } from "@web/core/utils/reactive";

export class ClickerModel extends Reactive {
    constructor() {
        super(...arguments);

        this.clicks = 0;
        this.level = 0;
        this.clickerBots = 0;

        setInterval(() => {
            this.increment(this.clickerBots * 10);
        }, 10000);

        this.bus = new EventBus();
    }

    increment(inc) {
        this.clicks += inc;
        if (this.clicks >= 1000 && this.level == 0) {
            this.level++;
            this.bus.trigger("MILESTONE_1k");
        }
    }

    addBot() {
        this.clickerBots += 1;
    }
}