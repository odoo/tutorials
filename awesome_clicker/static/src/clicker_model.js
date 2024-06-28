/** @odoo-module **/

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { choose } from "./utils";
import { rewards } from "./clicker_rewards";
import { browser } from "@web/core/browser/browser";

export class ClickerModel extends Reactive {
    static template = "awesome_clicker.clicker_model";
    static props = {};

    constructor(savedState = [999000,0,0,0,1]) {
        super();

        this.count = savedState[0];
        this.level = savedState[1];
        this.clickBots = savedState[2];
        this.bigBots = savedState[3];
        this.power = savedState[4];

        setInterval(async () => {
            this.increment(this.clickBots * 1);
            this.increment(this.bigBots * 10);
        }, 1000);

        setInterval(async () => {
            browser.localStorage.setItem("savedClickerModel", [
                this.count,
                this.level,
                this.clickBots,
                this.bigBots,
                this.power],
            );
        }, 5000);

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
        if (Math.random() < 1/1000) {
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
        this.bus.trigger("reward_obtained", reward);
    }
}
