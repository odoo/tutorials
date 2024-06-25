/** @odoo-module **/

import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "../click_rewards.js";


export class ClickerModel extends Reactive {

    constructor() {
        super();

        this.clicks = 2000000;
        this.level = 0;
        this.clickBots = 0;
        this.bigBots = 0;
        this.power = 1;

        this.trees = {
            pearTree: {
                nb_trees: 0,
                fruit: "Pear",
                nb_fruits: 0
            },
            cherryTree: {
                nb_trees: 0,
                fruit: "Cherry",
                nb_fruits: 0
            }
        }

        this.milestones = [1000, 5000, 100000, 1000000];
        this.maxLevel = 4;
        this.bus = new EventBus();

        setInterval(() => this.clicks += this.power * (10 * this.clickBots + 100 * this.bigBots), 10*1000);
        for (const treeType of Object.keys(this.trees))
            setInterval(() => this.trees[treeType].nb_fruits += this.trees[treeType].nb_trees, 30*1000)
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

    increment(inc) {
        this.clicks += inc;
            
        if (this.level < this.maxLevel && this.clicks >= this.milestones[this.level]) {
            this.level++;
            this.bus.trigger("MILESTONE_REACHED", this.level);
        }
    }

    buyClickBot() {
        this.clickBots++;
        this.clicks -= 1000;
    }

    buyBigBot() {
        this.bigBots++;
        this.clicks -= 5000;
    }

    buyTree(treeType) {
        this.trees[treeType].nb_trees++;
        this.clicks -= 1000000;
    }

    getReward() {
        const eligible_rewards = rewards.filter((reward) => (!reward.minLevel || reward.minLevel <= this.level)
             && (!reward.maxLevel || reward.maxLevel >= this.level));
        const reward = eligible_rewards[Math.floor(Math.random() * eligible_rewards.length)];
        this.bus.trigger("REWARD_RECEIVED", reward);
    }

    totalTreesAndFruits() {
        var treeTotal = 0;
        var fruitsTotal = 0;

        for (const treeType of Object.keys(this.trees)) {
            treeTotal += this.trees[treeType].nb_trees;
            fruitsTotal += this.trees[treeType].nb_fruits;
        }

        return { 'treeTotal': treeTotal, 'fruitsTotal': fruitsTotal };
    }
}