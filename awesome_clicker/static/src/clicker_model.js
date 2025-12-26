import { EventBus } from "@odoo/owl";
import { Reactive } from "@web/core/utils/reactive";

export class ClickerModel extends Reactive {
    constructor() {
        super(...arguments);
        this.clicks = 0;
        this.level = 0;
        this.clickBots = 0;
        this.bigBots = 0;
        this.bus = new EventBus();
    }

    increment(val) {
        this.clicks += val;
        if (this.level < 1 && this.clicks >= 1000) {
            this.bus.trigger("MILESTONE_1k");
            this.level++;
        } else if (this.level < 2 && this.clicks >= 5000) {
            this.bus.trigger("MILESTONE_5k");
            this.level++;
        }
    }

    buyClickBot() {
        const botPrice = 1000;
        if (this.clicks < botPrice) {
            return;
        }

        this.clicks -= botPrice;
        this.clickBots++;
    }

    buyBigBot() {
        const botPrice = 5000;
        if (this.clicks < botPrice) {
            return;
        }

        this.clicks -= botPrice;
        this.bigBots++;
    }

    botsDoClicks() {
        this.clicks += this.clickBots * 10 + this.bigBots * 100;
    }
}
