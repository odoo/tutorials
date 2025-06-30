import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";

export class ClickerModel extends Reactive {

    constructor() {
        super();
        this.clicks = 0;
        this.level = 0;
        this.bus = new EventBus();
        this.bots = {
            clickBot: {
                price: 1000,
                level: 1,
                increment: 10,
                purchased: 0,
            },
            bigBot: {
                price: 5000,
                level: 2,
                increment: 100,
                purchased: 0,
            },
        }
    }

    increment(value) {
        this.clicks += value;

        if (this.milestones[this.level] && this.clicks >= this.milestones[this.level].clicks) {
            this.bus.trigger("MILESTONE", this.milestones[this.level].unlock);
            this.level++;
        }
    }

    buyBot(name) {
        if (!Object.keys(this.bots).includes(name)) {
            throw new Error(`Invalid bot name ${name}`)
        }

        if (this.clicks < this.bots[name].price) {
            return false;
        }

        this.clicks -= this.bots[name].price;
        this.bots[name].purchased += 1;
    }

    tick() {
        for (const bot in this.bots) {
            this.increment(this.bots[bot].purchased * this.bots[bot].increment);
        }
    }

    get milestones() {
        return [
            { clicks: 1000, unlock: "clickbots" },
            { clicks: 5000, unlock: "bigbots" },
        ];
    }
}
