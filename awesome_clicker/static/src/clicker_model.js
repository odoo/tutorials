import { Reactive } from "@web/core/utils/reactive";


export class ClickerModel extends Reactive {

    constructor() {
        super();
        
        this.clicks = 0;
        this.level = 1;
        this.clickBots = 0;

        document.addEventListener("click", () => this.increment(1), { capture: true });
        setInterval(() => this.clicks += this.clickBots * 10, 10 * 1000);
    }

    increment(inc) {
        this.clicks += inc;
    }

    purchaseClickBot() {
        this.clickBots++;
        this.clicks -= 1000;
    }
}
