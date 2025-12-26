import { EventBus } from "@odoo/owl";
import { Reactive } from "@web/core/utils/reactive";
import {
    BIGBOT_CLICKS,
    BOT_FREQUENCY,
    CLICKBOT_CLICKS,
    MILESTONES,
    PURCHASABLE_REWARDS,
} from "./clicker_data";

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

    botsDoClicks() {
        this.clicks +=
            (this.clickBots * CLICKBOT_CLICKS + this.bigBots * BIGBOT_CLICKS) * this.multiplier;
    }
}
