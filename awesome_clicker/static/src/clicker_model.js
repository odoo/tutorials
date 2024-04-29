/** @odoo-module **/

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";

export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.clicks = 0;
        this.level = 0;
        this.power = 1;
        this.clickBots = 0;
        this.bigBots = 0;

        this.bus = new EventBus();

        setInterval(this.applyBotsClicks.bind(this), 1000);
    }

    updateLevel() {
        if(this.level == 0 && this.clicks > 999) {
            this.level = 1;
            this.bus.trigger("MILESTONE_1k");
        } else if (this.level == 1 && this.clicks > 4999) {
            this.level = 2;
        } else if (this.level == 2 && this.clicks > 99999) {
            this.level = 3;
        }
    }
    
    applyBotsClicks() {
        this.clicks += (10*this.clickBots + 100*this.bigBots)*this.power;
    }

    increment(inc) {
        this.clicks += inc;
        this.updateLevel();
    }
}
