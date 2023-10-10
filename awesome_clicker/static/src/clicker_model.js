import { Reactive } from "@web/core/utils/reactive";

export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.clicks = 0;
        this.level = 0;
        this.clickBots = 0;

        document.addEventListener("click", () => this.increment(1), true);
        setInterval(() => {
            this.clicks += this.clickBots * 10;
        }, 10000);
    }

    increment(inc) {
        this.clicks += inc;
        if (this.level < 1 && this.clicks >= 1000) {
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
