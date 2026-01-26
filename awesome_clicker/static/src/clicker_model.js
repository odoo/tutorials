import { EventBus } from "@odoo/owl";
import { Reactive } from "@web/core/utils/reactive";

import { chooseReward } from "./utils";


export const LEVEL_REQUIREMENTS = [
    { level: 1, requirement: 1000, event_name: "MILESTONE_1k", message: "Level up! You have unlocked ClickBots." },
    { level: 2, requirement: 5000, event_name: "MILESTONE_5k", message: "Level up! You have unlocked BigBots." },
    { level: 3, requirement: 100000, event_name: "MILESTONE_100k", message: "Level up! You have unlocked Power." },
];

export class ClickerModel extends Reactive {

    constructor() {
        super();
        
        this.clicks = 0;
        this.level = 0;
        this.bots = {
            clickbot: {
                name: "ClickBot",
                quantity: 0,
                price: 1000,
                yield: 10,
                level_required: 1,
            },
            bigbot: {
                name: "BigBot",
                quantity: 0,
                price: 5000,
                yield: 100,
                level_required: 2,
            }
        };
        this.power = 1;

        this.bus = new EventBus();
        document.addEventListener("click", () => this.increment(1), { capture: true });
        setInterval(() => {
            Object.values(this.bots).forEach(bot => this.clicks += bot.yield * this.power * bot.quantity);
        }, 10 * 1000);
    }

    increment(inc) {
        this.clicks += inc;

        LEVEL_REQUIREMENTS.forEach(milestone => {
            if (this.clicks > milestone.requirement && this.level < milestone.level) {
                this.level++;
                this.bus.trigger(milestone.event_name);
            }
        })
    }

    purchaseBot(bot_name) {
        let purchased_bot = Object.values(this.bots).find(bot => bot.name === bot_name);
        purchased_bot.quantity++;
        this.clicks -= purchased_bot.price;
    }

    purchasePower() {
        this.power++;
        this.clicks -= 50000;
    }

    getReward() {
        this.bus.trigger("RANDOM_REWARD", chooseReward(this.level));
    }
}
