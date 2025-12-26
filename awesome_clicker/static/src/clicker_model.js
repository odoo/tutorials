import { EventBus } from "@odoo/owl";
import { Reactive } from "@web/core/utils/reactive";
import {
    BIGBOT_CLICKS,
    BOT_FREQUENCY,
    CLICKBOT_CLICKS,
    MILESTONES,
    PURCHASABLE_REWARDS,
    RANDOM_REWARDS,
    TREE_FREQUENCY,
} from "./clicker_data";
import { choose, randomBoolean } from "./utils";

export class ClickerModel extends Reactive {
    constructor() {
        super(...arguments);
        this.clicks = 0;
        this.level = 0;
        this.clickBots = 0;
        this.bigBots = 0;
        this.multiplier = 1;
        this.trees = {};
        this.fruits = {};
        this.shopItems = PURCHASABLE_REWARDS;
        this.botFrequency = BOT_FREQUENCY;
        this.treeFrequency = TREE_FREQUENCY;
        this.bus = new EventBus();
    }

    get totalFruits() {
        return Object.values(this.fruits).reduce((a, b) => a + b, 0);
    }

    get totalTrees() {
        return Object.values(this.trees).reduce((a, b) => a + b, 0);
    }

    get persistentState() {
        return {
            clicks: this.clicks,
            level: this.level,
            clickBots: this.clickBots,
            bigBots: this.bigBots,
            multiplier: this.multiplier,
            trees: this.trees,
            fruits: this.fruits,
        };
    }

    set persistentState(state) {
        Object.assign(this, state);
    }

    getItemsByCategory(category) {
        return this.shopItems.filter((item) => item.category === category);
    }

    _getApplicableRewards() {
        return RANDOM_REWARDS.filter(
            (r) =>
                (r.minLevel == null || this.level >= r.minLevel) &&
                (r.maxLevel == null || this.level <= r.maxLevel)
        );
    }

    increment(val) {
        this.clicks += val;

        for (const milestone of MILESTONES) {
            if (this.level < milestone.level && this.clicks >= milestone.clicks) {
                this.bus.trigger(milestone.event);
                this.level = milestone.level;
                break;
            }
        }
    }

    verifyPurchase(minLevel, price) {
        if (this.level < minLevel || this.clicks < price) {
            return false;
        }

        this.clicks -= price;
        return true;
    }

    purchase(id) {
        const index = this.shopItems.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.shopItems[index].buy(this);
        }
    }

    giveRandomReward(chance = 1) {
        if (!randomBoolean(chance)) {
            return;
        }

        const reward = choose(this._getApplicableRewards());
        // reward can be undefined if no applicable reward
        if (reward) {
            this.bus.trigger("REWARD", reward);
        }
    }

    botsDoClicks() {
        this.clicks +=
            (this.clickBots * CLICKBOT_CLICKS + this.bigBots * BIGBOT_CLICKS) * this.multiplier;
    }

    treesProduceFruit() {
        for (const [type, nb] of Object.entries(this.trees)) {
            if (!this.fruits[type]) {
                this.fruits[type] = 0;
            }
            this.fruits[type] += nb;
        }
    }
}
