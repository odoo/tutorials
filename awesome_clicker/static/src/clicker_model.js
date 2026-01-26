import { EventBus } from "@odoo/owl";
import { Reactive } from "@web/core/utils/reactive";

import { chooseReward } from "./utils";


export const LEVEL_REQUIREMENTS = [
    { level: 1, requirement: 1000, event_name: "MILESTONE_1k", message: "Level up! You have unlocked ClickBots." },
    { level: 2, requirement: 5000, event_name: "MILESTONE_5k", message: "Level up! You have unlocked BigBots." },
    { level: 3, requirement: 100000, event_name: "MILESTONE_100k", message: "Level up! You have unlocked Power." },
    { level: 4, requirement: 1000000, event_name: "MILESTONE_1M", message: "Level up! You have unlocked Trees." },
];

export class ClickerModel extends Reactive {

    constructor() {
        super();
        
        this.clicks = 0;
        this.level = 0;
        this.power = 1;
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
        this.trees = {
            pear: {
                name: "Pear Tree",
                fruit_name: "Pear",
                quantity: 0,
                price: 1000000,
                fruits: 0,
                level_required: 4,
            },
            cherry: {
                name: "Cherry Tree",
                fruit_name: "Cherry",
                quantity: 0,
                price: 1000000,
                fruits: 0,
                level_required: 4,
            }
        }

        this.bus = new EventBus();
        document.addEventListener("click", () => this.increment(1), { capture: true });
        setInterval(() => {
            Object.values(this.bots).forEach(bot => this.clicks += bot.yield * this.power * bot.quantity);
        }, 10 * 1000);
        setInterval(() => {
            Object.values(this.trees).forEach(tree => tree.fruits += tree.quantity);
        }, 30 * 1000);
    }

    increment(inc) {
        this.clicks += inc;

        LEVEL_REQUIREMENTS.forEach(milestone => {
            if (this.clicks >= milestone.requirement && this.level < milestone.level) {
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

    purchaseTree(tree_name) {
        let purchased_tree = Object.values(this.trees).find(tree => tree.name === tree_name);
        purchased_tree.quantity++;
        this.clicks -= purchased_tree.price;
    }

    purchasePower() {
        this.power++;
        this.clicks -= 50000;
    }

    getReward() {
        this.bus.trigger("RANDOM_REWARD", chooseReward(this.level));
    }

    getTotalTreeCount() {
        return Object.values(this.trees).map(tree => tree.quantity).reduce((sum, qty) => sum + qty);
    }

    getTotalFruitCount() {
        return Object.values(this.trees).map(tree => tree.fruits).reduce((sum, qty) => sum + qty);
    }
}
