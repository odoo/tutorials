/** @odoo-module **/

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "./click_rewards";
import { choose, randomInt } from "./utils";

export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.bus = new EventBus();
        this._first1KMilestoneTriggered = false;
        this.clicks = 0;
        this.clickBots = 0;
        this.bigClickBots = 0;
        this.level = 0;
        this.multiplier = 1;

        setInterval(() => this.increment(this.clickBots * 10 * this.multiplier), 1000 * 20);
        setInterval(() => this.increment(this.bigClickBots * 100 * this.multiplier), 1000 * 10);
    }

    increment(inc) {
        this.clicks += inc;
        this.checkForNewLevel();
    }

    checkForNewLevel() {
        const initialLevel = this.level;
        if (this.level === 0 && this.clicks > 1_000) {
            this.level = 1;
            this._first1KMilestoneTriggered = true;
            console.log("TRIGGERING");
            this.bus.trigger("MILESTONE_1k");
        }
        if (this.level === 1 && this.clicks > 5_000) {
            this.level++;
        }
        if (this.level === 2 && this.clicks > 100_000) {
            this.level++;
        }

        if (initialLevel !== this.level) {
            const reward = this.getReward();
            console.log(reward);
            if (reward) reward.apply(this);
        }
    }

    getReward() {
        return choose(
            rewards.filter(
                (reward) =>
                    this.level >= (reward.minLevel ?? 0) && this.level <= (reward.maxLevel ?? Number.MAX_SAFE_INTEGER)
            )
        );
    }

    incrementClickBots(inc) {
        this.clickBots += inc;
        this.increment(-inc * 1000);
    }
    incrementBigClickBots(inc) {
        this.bigClickBots += inc;
        this.increment(-inc * 5000);
    }

    incrementMultiplier(inc) {
        this.multiplier++;
        this.increment(inc * -50_000);
    }
}
