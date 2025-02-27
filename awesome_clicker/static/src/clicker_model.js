import { Reactive } from "@web/core/utils/reactive";

export class ClickerModel extends Reactive {
    constructor() {
        super(...arguments);

        this.clicks = 0;
        this.level = 0;
        this.clickerBots = 0;

        setInterval(() => {
            this.clicks += this.clickBots * 10;
        }, 10000);
    }

    increment(inc) {
        this.clicks += inc;
        if (this.clicks >= 1000 && this.level == 0) {
            this.level++;
        }
    }

    addBot() {
        this.clickerBots += 1;
    }
}