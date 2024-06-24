/** @odoo-module **/

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "./click_rewards";
import { choose } from "./utils";

const COSTS = {
    TREE: 1_000_000,
    CLICK_BOT: 1_000,
    BIG_CLICK_BOT: 5_000,
    MULTIPLIER: 50_000,
};

export const clickerBus = new EventBus();

export class ClickerModel extends Reactive {
    constructor() {
        super();

        this.versionNumber = 1;

        this.clicks = 0;
        this.clickBots = 0;
        this.bigClickBots = 0;
        this.level = 0;
        this.multiplier = 1;

        // FIXME: ability to improve structure by storing trees and fruit in a dict
        // for easy display and calculation of total number of trees/fruit
        this.pearsTreeCount = 0;
        this.pearsFruitCount = 0;

        this.cherriesTreeCount = 0;
        this.cherriesFruitCount = 0;

        this.peachTreeCount = 0;
        this.peachFruitCount = 0;

        setInterval(() => {
            this.cherriesFruitCount += this.cherriesTreeCount;
            this.pearsFruitCount += this.pearsTreeCount;
            this.pearsFruitCount += this.pearsTreeCount;
        }, 5 * 1000);

        setInterval(() => this.increment(this.clickBots * 100 * this.multiplier), 2 * 1000);
        setInterval(() => this.increment(this.bigClickBots * 100 * this.multiplier), 10 * 1000);
    }

    increment(inc) {
        this.ensureEnoughClick(inc);
        this.clicks += inc;
        this.checkForNewLevel();
    }

    checkForNewLevel() {
        const initialLevel = this.level;
        if (this.level === 0 && this.clicks > 1_000) {
            this.level = 1;
            clickerBus.trigger("MILESTONE_1k");
        }
        if (this.level === 1 && this.clicks > 5_000) {
            this.level++;
        }
        if (this.level === 2 && this.clicks > 100_000) {
            this.level++;
        }
        if (this.level === 3 && this.clicks > 1_000_000) {
            this.level++;
        }

        if (initialLevel !== this.level) {
            const reward = this.getReward();
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

    ensureEnoughClick(clickToAdd) {
        if (this.clicks + clickToAdd < 0) {
            throw new Error("No enough click");
        }
    }

    incrementClickBots() {
        this.increment(-COSTS.CLICK_BOT);
        this.clickBots++;
    }

    incrementBigClickBots() {
        this.increment(-COSTS.BIG_CLICK_BOT);
        this.bigClickBots++;
    }

    incrementMultiplier() {
        this.increment(-COSTS.MULTIPLIER);
        this.multiplier++;
    }

    incrementPearTree() {
        this.increment(-COSTS.TREE);
        this.pearsTreeCount++;
    }

    incrementCherryTree() {
        this.increment(-COSTS.TREE);
        this.cherriesTreeCount++;
    }

    incrementPeachTree() {
        this.increment(-COSTS.TREE);
        this.peachTreeCount++;
    }

    totalTreeCount() {
        return this.pearsTreeCount + this.cherriesTreeCount + this.peachTreeCount;
    }

    totalFruitCount() {
        return this.pearsFruitCount + this.cherriesFruitCount + this.peachFruitCount;
    }
}
