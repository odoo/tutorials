import { Reactive } from "@web/core/utils/reactive";

export class ClickerModel extends Reactive {
    constructor() {
        super(...arguments);
        this.clicks = 0;
        this.level = 0;
        this.clickBots = 0;
    }

    increment(val) {
        this.clicks += val;
        if (this.level < 1 && this.clicks >= 1000) {
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

    botsDoClicks(nbClicks) {
        this.clicks += this.clickBots * nbClicks;
    }
}
