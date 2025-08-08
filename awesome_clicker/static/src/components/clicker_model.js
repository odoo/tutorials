import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "../click_rewards";

export class clickerModel extends Reactive {

    constructor() {
        super();
        this.bus = new EventBus();
        this.clicks = 0;
        this.clickBots = 0;
        this.bigBots = 0;
        this.level = 1;
        this.firstTime1k = true;
        this.clicksToUpLevel = 5000;
        this.power = 1;
        this.version = 2;
        this.trees = {
            pear: 0,
            cherry: 0,
        };
        this.fruits = {
            pear: 0,
            cherry: 0,
        }

        const runBots = () => {
            this.clicks += 10 * this.clickBots * this.power;
            this.clicks += 100 * this.bigBots * this.power;
        }
        setInterval(runBots, 10 * 1000);

        const fetchFruits = () => {
            this.fruits.pear += this.trees.pear;
            this.fruits.cherry += this.trees.cherry;
        }
        setInterval(fetchFruits, 30 * 1000);
    }

    getModelStatus() {
        return {
            clicks: this.clicks,
            clickBots: this.clickBots,
            bigBots: this.bigBots,
            level: this.level,
            firstTime1k: this.firstTime1k,
            clicksToUpLevel: this.clicksToUpLevel,
            power: this.power,
            trees: this.trees,
            fruits: this.fruits,
            version: this.version
        }
    }


    setModelStatus(old_save) {
        this.clicks = old_save.clicks;
        this.clickBots= old_save.clickBots;
        this.bigBots= old_save.bigBots;
        this.level= old_save.level;
        this.firstTime1k= old_save.firstTime1k;
        this.clicksToUpLevel= old_save.clicksToUpLevel;
        this.power= old_save.power;
        this.trees= old_save.trees;
        this.fruits= old_save.fruits;
        this.version = old_save.version;
    }

    getTotalTree() {
        return this.trees.pear + this.trees.cherry;
    }

    getTotalFruits() {
        return this.fruits.pear + this.fruits.cherry;
    }

    incrementClickBots(inc) {
        this.increment(-1000);
        this.clickBots += inc;
    }

    incrementBigBots(inc) {
        this.increment(-5000);
        this.bigBots += inc;
    }

    increment(inc) {
        this.clicks += inc;
        if (this.firstTime1k && this.clicks >= 1000) {
            this.bus.trigger("MILESTONE_1k");
            this.firstTime1k = false;
        } else if (this.clicks >= this.clicksToUpLevel) {
            this.level++;
            if (this.level == 2) {
                this.clicksToUpLevel = 100000;
            } else if (this.level == 3) {
                this.clicksToUpLevel = 1000000;
            }
        }
    }

    incrementPower(inc) {
        this.increment(-50000);
        this.power += inc;
    }

    incrementPearTree(inc) {
        this.increment(-1000000);
        this.trees.pear += 1;
    }

    incrementCherryTree(inc) {
        this.increment(-1000000);
        this.trees.cherry += 1;
    }

    getReward() {
        while (true) {
            const i = Math.floor(Math.random() * rewards.length);
            const reward = rewards[i];

            if ((reward.minLevel === undefined || reward.minLevel <= this.level) &&
                (reward.maxLevel === undefined || reward.maxLevel >= this.level)) {
                return reward;
            }
        }
    }

    applyReward(reward) {
        reward.apply(this);
    }

}