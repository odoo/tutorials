import { EventBus } from "@odoo/owl";
import { Reactive } from "@web/core/utils/reactive";
import {
    BIGBOT_CLICKS,
    BOT_FREQUENCY,
    CLICKBOT_CLICKS,
    MILESTONES,
    PURCHASABLE_REWARDS,
    RANDOM_REWARDS,
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
        this.shopItems = PURCHASABLE_REWARDS;
        this.botFrequency = BOT_FREQUENCY;
        this.bus = new EventBus();
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
}
