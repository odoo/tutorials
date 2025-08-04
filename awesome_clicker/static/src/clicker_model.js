import { EventBus } from "@odoo/owl";
import { Reactive } from "@web/core/utils/reactive";
import { CURRENT_VERSION } from "./clicker_migration";
import { rewards } from "./clicker_rewards";
import { choose } from "./utils";

export class ClickerModel extends Reactive {
    constructor(){
        super();
        this.version = CURRENT_VERSION;
        this.clicks = 0
        this.level=0
        this.bus = new EventBus();
        this.power = 1
        this.clickBots=0;
        this.bigBots=0;
        this.cherryTree=0;
        this.cherries=0;
        this.pearTree=0
        this.pears=0

        setInterval(() => {
            const autoClicks = (this.clickBots * 10 + this.bigBots * 100) * this.power;
            if (autoClicks > 0) {
                this.clicks += autoClicks;
                console.log(`Auto-clicked: +${autoClicks}`);
            }

            if (this.clicks >= 1000 && this.level < 1) {
                this.level = 1;
                console.log("Level 1 unlocked!");
            }
        }, 10000);

        setInterval(() => {
            this.cherries += this.cherryTree;
            this.pears += this.pearTree;
        }, 30000);
    }

    increment(inc = 1) {
        this.clicks += inc;
        if (this.level === 0 && this.clicks >= 1000) {
            this.bus.trigger("MILESTONE_1K")
            this.level = 1;
            console.log("Level 1!");
        }
        else if (this.level === 1 && this.clicks >= 5000) {
            this.level = 2;
            console.log("Level 2!");
        }
        else if (this.level === 2 && this.clicks >= 100000) {
            this.level = 3;
            console.log("Level 3!");
        }
        else if (this.level === 3 && this.clicks >= 1000000) {
            this.level = 4;
            console.log("Level 4!");
        }
    }

    getReward() {
        const available = [];
        for (const reward of rewards) {
            if (!reward.minLevel || this.level >= reward.minLevel) {
                if (!reward.maxLevel || this.level <= reward.maxLevel) {
                    available.push(reward);
                }
            }
        }
        const reward = choose(available);
        this.bus.trigger("REWARD",reward);
        return reward;
    }
            
    buyClickBot() {
        if (this.clicks >= 1000) {
            this.clickBots++;
            this.clicks -= 1000;
        }
    }

    buyBigBot() {
        if (this.clicks >= 5000) {
            this.bigBots++;
            this.clicks -= 5000;
        }
    }

    buyPower() {
        if (this.clicks >= 50000) {
            this.power++;
            this.clicks -= 50000;
        }
    }

    buyCherryTree() {
        if (this.clicks >= 1000000) {
            this.cherryTree++;
            this.clicks -= 1000000;
        }
    }

    buyPearTree() {
        if (this.clicks >= 1000000) {
            this.pearTree++;
            this.clicks -= 1000000;
        }
    }

    toJSON() {
        const json = Object.assign({}, this);
        delete json["bus"];
        return json;

    }

    static fromJSON(json) {
        const clicker = new ClickerModel();
        const clickerInstance = Object.assign(clicker, json);
        return clickerInstance;
    }
}
