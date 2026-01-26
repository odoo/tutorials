import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { registry } from "@web/core/registry";

const buyables = {
    clickBot: {
        minLevel: 1,
        price: 1000,
        name: "clickBots",
        onBuy: "triggerInterval"
    },
    bigClickBot: {
        minLevel: 2,
        price: 5000,
        name: "bigClickBots",
        onBuy: "triggerInterval"
    },
    power: {
        minLevel: 3,
        price: 100_000,
        name: "power",
        onBuy: ""
    }
}

const allLevels = [
    {minClicks: 1_000, eventName: "MILESTONE_1k"},
    {minClicks: 5_000, eventName: "MILESTONE_5k"},
    {minClicks: 100_000, eventName: "MILESTONE_100k"}    
]

export class ClickerModel extends Reactive {
    clicks = 0;
    level = 0;

    clickBots = 0;
    bigClickBots = 0;
    power = 1;
    clickBotInterval = null;

    bus = new EventBus();

    constructor() {
        super();
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

    buy(availability) {
        if(this.clicks < availability.price || this.level < availability.minLevel) return;

        this.clicks -= availability.price;
        this[availability.name]++;
        
        let onBuy = this[availability.onBuy];
        if(onBuy) onBuy(this);
    }

    get(availability, count) {
        if(this.level < availability.minLevel) return;

        this[availability.name] += count;
        
        let onBuy = this[availability.onBuy];
        if(onBuy) onBuy(this);
    }

    triggerInterval(el) {
        if(el.clickBotInterval === null) {
            el.clickBotInterval = setInterval(() => {
                el.clicks += el.clickBots * 10 * el.power;
                el.clicks += el.bigClickBots * 100 * el.power;
            }, 1000);
        }
    }
}

registry.category("command_provider").add("clicker", {
    provide: (env, options) => {
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
