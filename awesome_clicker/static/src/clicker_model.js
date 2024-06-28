/** @odoo-module **/

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { choose } from "./utils";
import { rewards } from "./clicker_rewards";

export class ClickerModel extends Reactive {
    static template = "awesome_clicker.clicker_model";
    static props = {};

    constructor() {
        super();

        this.count = 0;
        this.level = 0;
        this.clickBots = 0;
        this.bigBots = 0;
        this.power = 1;

        setInterval(async () => {
            this.increment(this.clickBots * 1);
            this.increment(this.bigBots * 10);
        }, 1000);

        document.addEventListener("click", this.page_increment.bind(this), true);

        this.bus = new EventBus();
    }

    increment(inc) {
        this.count += inc * this.power;
        switch (this.level) {
            case 0:
                if (this.count >= 1000) {
                    this.level = 1;
                    this.bus.trigger("level_1_is_reached");
                }
                else break;
            case 1:
                if (this.count >= 5000) {
                    this.level = 2;
                    this.bus.trigger("level_2_is_reached");
                }
                else break;
            case 2:
                if (this.count >= 30000) {
                    this.level = 3;
                    this.bus.trigger("level_3_is_reached");
                }
                else break;
          }
    };

    button_increment() {
        this.increment(9);
    }

    page_increment() {
        if (Math.random() < 1/3) {
            this.get_reward();
        }
        this.increment(1);
    }

    buy(itemName, price = 0, amount = 1) {
        if (this.count >= price) {
            this.count -= price;
            this[itemName] += amount;
        }
    }

    get_reward() {
        var possible_rewards = [];
        for (let reward of rewards) {
            if ((!reward.minLevel || this.level >= reward.minLevel) && (!reward.maxLevel || this.level <= reward.maxLevel)) {
                possible_rewards.push(reward);
            }
        }
        if (possible_rewards.length == 0) return;
        const reward = choose(possible_rewards);
        console.log("Récompense : ", reward.description)
        reward.apply(this);
    }
}
