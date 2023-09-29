import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";

export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.clicks = 0;
        this.level = 0;
        this.clickBots = 0;
        this.bus = new EventBus();
    }

    addClick() {
        this.increment(1);
    }

    /**
     * This method is supposed to be periodically called by outside code, at some
     * proper interval
     */
    tick() {
        this.clicks += this.clickBots * 10;
    }

    increment(inc) {
        this.clicks += inc;
        if (this.level < 1 && this.clicks >= 1000) {
            this.bus.trigger("MILESTONE_1k");
            this.level++;
        }
    }

    buyClickBot() {
        const clickBotPrice = 1000;
        if (this.clicks < clickBotPrice) {
            return false;
        }
        this.clicks -= clickBotPrice;
        this.clickBots += 1;
    }
}
