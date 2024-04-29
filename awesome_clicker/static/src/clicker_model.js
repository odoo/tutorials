/** @odoo-module **/

import { Reactive } from "@web/core/utils/reactive";
import { choose } from "./utils";
import { rewards } from "./click_rewards";


export class ClickerModel extends Reactive {

    constructor() {
        super();
        this.setup(...arguments);
    }

    setup(bus, notification, action) {
        this.clicks = 0;
        this.level = 0;
        this.clickBots = 0;
        this.bigBots = 0;
        this.power = 1;
        this.pearTrees = 0;
        this.pears = 0;
        this.cherryTrees = 0;
        this.cherries = 0;
        this.peachTrees = 0;
        this.peaches = 0;

        this.bus = bus;
        this.notification = notification;
        this.action = action;

        setInterval(() => {
            this.increment((10 * this.clickBots + 100 * this.bigBots) * this.power);
        }, 10_000);
        setInterval(() => {
            this.pears += this.pearTrees;
            this.cherries += this.cherryTrees;
        }, 30_000);
    }

    getState() {
        return {
            clicks: this.clicks,
            level: this.level,
            clickBots: this.clickBots,
            bigBots: this.bigBots,
            power: this.power,
            pearTrees: this.pearTrees,
            pears: this.pears,
            cherryTrees: this.cherryTrees,
            cherries: this.cherries,
            peachTrees: this.peachTrees,
            peaches: this.peaches
        }
    }

    loadState(state) {
        Object.assign(this, state);
    }

    increment(inc) {
        this.clicks += inc;
        if (this.level == 0 && this.clicks >= 1000) {
            this.level = 1
            this.bus.trigger("MILESTONE_1k"); 
        }
        if (this.level == 1 && this.clicks >= 5000) {
            this.level = 2
            this.bus.trigger("MILESTONE_5k"); 
        }
        if (this.level == 2 && this.clicks >= 100_000) {
            this.level = 3
            this.bus.trigger("MILESTONE_100k"); 
        }
        if (this.level == 3 && this.clicks >= 1_000_000) {
            this.level = 4
            this.bus.trigger("MILESTONE_1m"); 
        }
    }
    
    buyClickBot() {
        if (this.clicks < 1000) return;
        this.clicks -= 1000;
        this.clickBots++;
    }

    buyBigBot() {
        if (this.clicks < 5000) return;
        this.clicks -= 5000;
        this.bigBots++;
    }

    buyPower() {
        if (this.clicks < 50_000) return;
        this.clicks -= 50_000;
        this.power++;
    }

    buyPearTree() {
        if (this.clicks < 1_000_000) return;
        this.clicks -= 1_000_000;
        this.pearTrees++;
    }

    buyCherryTree() {
        if (this.clicks < 1_000_000) return;
        this.clicks -= 1_000_000;
        this.cherryTrees++;
    }

    buyPeachTree() {
        if (this.clicks < 1_500_000) return;
        this.clicks -= 1_500_000;
        this.peachTrees++;
    }

    getReward() {
        var reward = choose(rewards.filter(reward =>
            (reward.maxLevel ? this.level <= reward.maxLevel : true) && 
            (reward.minLevel ? this.level >= reward.minLevel : true))
        );
        var close = this.notification.add("Congrats you won a reward: \"" + reward.description + "\"!", {
            type: "success",
            sticky: true,
            buttons: [
                { name: "Collect", onClick: () => this.onCollect(reward.apply, close), primary: false }
            ]}
        );
    }

    onCollect(apply, close) {
        apply(this);
        close();
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.client_action",
            target: "new",
            name: "Clicker"
        });
    }

    getTotalTrees() {
        return this.pearTrees + this.cherryTrees + this.peachTrees;
    }

    getTotalFruits() {
        return this.pears + this.cherries + this.peaches;
    }
}