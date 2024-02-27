/** @odoo-module */

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";

export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.bus = new EventBus();
        this.clicks = 0;
        this.level = 0;
        this.clickBots = 0;

        setInterval(() => {
            this.clicks += this.clickBots * 10;
        }, 10000)

        document.addEventListener("click", () => this.increment(1), true);
    }

    increment(count) {
        this.clicks += count;
        if(this.level < 1 && this.clicks >= 1000) {
            this.bus.trigger("MILESTONE_1k");
            this.level++;
        }
    }

    buyClickBot() {
        const clickBotPrice = 1000;

        if(this.clicks < clickBotPrice)
            return false;

        this.clicks -= clickBotPrice;
        this.clickBots += 1;
    }


}
