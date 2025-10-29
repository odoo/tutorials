
import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { rewards } from "./click_rewards";
import { randomChoice } from "./utils";
import { CURRENT_VERSION } from "./clicker_migration";

export class ClickerModel extends Reactive {

    constructor() {
        super();
        this.value = 0;
        this.level = 0;
        this.bus = new EventBus();
        this.bots = {
            clickBots : {
                price: 1000,
                number: 0,
                level: 1,
                clicks: 10
            },
            bigBots : {
                price: 5000,
                number: 0,
                level: 2,
                clicks: 100
            }
        }
        this.power = 1;
        this.fruits = {
            cherries: 0,
            pears: 0,
            peaches: 0
        };
        this.trees = {
            cherryTrees: {
                price: 1000000,
                number: 0,
                level: 4,
                fruit: "cherries"
            },
            pearTrees: {
                price: 1000000,
                number: 0,
                level: 4,
                fruit: "pears"
            },
            peachTree: {
                price: 1500000,
                level: 4,
                produce: "peaches",
                purchased: 0,
            }
        };
        this.version_number = CURRENT_VERSION;
    }

    increment(inc) {
        this.value += inc;
        if (this.milestones[this.level] && this.value >= this.milestones[this.level].clicks) {
            this.bus.trigger("MILESTONE", this.milestones[this.level]);
            this.level++;
        }
    }

    buyBot(botName) {
        const bot = this.bots[botName];
        const clickBotPrice = bot.price;
        if (this.value < clickBotPrice) {
            return false;
        }
        bot.number++;
        this.value-=clickBotPrice;
    };

    clickBotsAction() {
        for(const bot in this.bots) {
            this.value += ( this.bots[bot].clicks * this.bots[bot].number ) * this.power;
        }
    };

    buyPower() {
        const powerPrice = 50000;
        if (this.value < powerPrice) {
            return false;
        }
        this.power++;
        this.value-=powerPrice;
    };

    getReward() {
        const availableReward = [];
        for (const reward of rewards) {
            if (reward.minLevel <= this.level || !reward.minLevel) {
                if (reward.maxLevel >= this.level || !reward.maxLevel) {
                    availableReward.push(reward);
                }
            }
        }
        const reward = randomChoice(availableReward);
        this.bus.trigger("REWARD", reward);
        return reward;
    }

    buyTree(treeName) {
        const tree = this.trees[treeName];
        const treePrice = tree.price;
        if (this.value < treePrice) {
            return false;
        }
        tree.number++;
        this.value-=treePrice;
    };

    treesAction() {
        for(const tree in this.trees) {
            this.fruits[this.trees[tree].fruit] += this.trees[tree].number;
        }
    };

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

    get milestones() {
        return [
            { clicks: 1000, bot: "ClickBot" },
            { clicks: 5000, bot: "BigBot" },
            { clicks: 100000, bot: "Power" },
            { clicks: 1000000, bot: "Trees and Fruits" }
        ]
    }

}
