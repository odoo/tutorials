import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { currentVersion } from "./clicker_migration";

export const treeTypes = [
    "pear", "cherry", "peach"
]

let buyables = {
    clickBot: {
        minLevel: 1,
        price: 1000,
        name: "clickBots",
        onBuy: "triggetClickBotInterval"
    },
    bigClickBot: {
        minLevel: 2,
        price: 5000,
        name: "bigClickBots",
        onBuy: "triggetClickBotInterval"
    },
    power: {
        minLevel: 3,
        price: 100_000,
        name: "power",
        onBuy: ""
    },
}

const allLevels = [
    {minClicks: 1_000, eventName: "MILESTONE_1k"},
    {minClicks: 5_000, eventName: "MILESTONE_5k"},
    {minClicks: 100_000, eventName: "MILESTONE_100k"},
    {minClicks: 1_000_000, eventName: "MILESTONE_1M"}   
]

export const clickerModelKey = "clicker-model-key";

export class ClickerModel extends Reactive {
    clicks = 0;
    level = 0;

    clickBots = 0;
    bigClickBots = 0;
    power = 1;
    clickBotInterval = null;

    trees = new Array(treeTypes.length).fill(0);
    fruits = new Array(treeTypes.length).fill(0);
    treeInterval = null;

    bus = new EventBus();

    version = 0;

    constructor(def = {}) {
        super();

        this.clicks = def.clicks ?? 0;
        this.level = def.level ?? 0;
        this.clickBots = def.clickBots ?? 0;
        this.bigClickBots = def.bigClickBots ?? 0;
        this.power = def.power ?? 1;
        this.version = def.version ?? currentVersion;

        if(def.fruits) {
            for(let i = 0; i < this.fruits.length; i++) {
                this.fruits[i] = def.fruits[i] ?? 0;
            }
        }

        if(def.trees) {
            for(let i = 0; i < this.trees.length; i++) {
                this.trees[i] = def.trees[i] ?? 0;
            }
        }

        if(this.clickBots > 0 || this.bigClickBots > 0) this.triggetClickBotInterval(this);
        if(this.trees.find(t => t > 0)) this.triggerTreeInterval(this);
    }

    increment(val) {
        this.clicks += val;

        for(let i = this.level; i < allLevels.length; i++) {
            let level = allLevels[i];
            if(this.clicks >= level.minClicks) {
                this.level = i + 1;
                this.bus.trigger(level.eventName);
            }
        }
    }

    buyClickBot() {
        this.buy(buyables.clickBot);
    }

    buyBigClickBot() {
        this.buy(buyables.bigClickBot);
    }

    buyPower() {
        this.buy(buyables.power);
    }

    getClickBot(count) {
        this.get(buyables.clickBot, count);
    }

    getBigClickBot(count) {
        this.get(buyables.bigClickBot, count);
    }

    getPower(count) {
        this.get(buyables.power, count);
    }

    buyTree(fruitName) {
        let index = treeTypes.indexOf(fruitName);
        if(index < 0) return;

        if(this.clicks < 1_000_000 || this.level < 4) return;

        this.clicks -= 1_000_000;
        this.trees[index]++;
        this.triggerTreeInterval(this);
    }

    buy(buyable) {
        if(this.clicks < buyable.price || this.level < buyable.minLevel) return;

        this.clicks -= buyable.price;
        this[buyable.name]++;
        
        let onBuy = this[buyable.onBuy];
        if(onBuy) onBuy(this);
    }

    get(buyable, count) {
        if(this.level < buyable.minLevel) return;

        this[buyable.name] += count;
        
        let onBuy = this[buyable.onBuy];
        if(onBuy) onBuy(this);
    }

    getTreeCount(fruitName) {
        let index = treeTypes.indexOf(fruitName);
        if(index < 0) return 0;

        return this.trees[index];
    }

    getAllTreesCount() {
        return this.trees.reduce((acc, t) => acc += t, 0);
    }

    getAllFruitsCount() {
        return this.fruits.reduce((acc, t) => acc += t, 0);
    }

    getFruitCount(fruitName) {
        let index = treeTypes.indexOf(fruitName);
        if(index < 0) return 0;

        return this.fruits[index];
    }

    triggetClickBotInterval(el) {
        if(el.clickBotInterval === null) {
            el.clickBotInterval = setInterval(() => {
                el.clicks += el.clickBots * 10 * el.power;
                el.clicks += el.bigClickBots * 100 * el.power;

                localStorage.setItem(clickerModelKey, JSON.stringify(el));
            }, 1000);
        }
    }

    triggerTreeInterval(el) {
        if(el.treeInterval === null) {
            el.treeInterval = setInterval(() => {
                for(let i = 0; i < treeTypes.length; i++) {
                    el.fruits[i] += el.trees[i];
                }

                localStorage.setItem(clickerModelKey, JSON.stringify(el));
            }, 3000);
        }
    }
}

registry.category("command_provider").add("clicker", {
    provide: (env) => {
        return [{
            action() {
                env.services.action.doAction({
                    type: 'ir.actions.client',
                    tag: 'awesome_clicker.client_action',
                    target: 'new',
                    name: 'Clicker'
                })
            },
            category: "clicker",
            name: "Open Clicker Game"
        },{
            action() {
                env.services.clicker.clicker.buyClickBot();
            },
            category: "Clicker",
            name: "Buy 1 click bot"
        }]
    }
})
