import {Reactive} from "@web/core/utils/reactive";
import {EventBus} from "@odoo/owl";


export class ClickBot {
    constructor(name = "Bot",
                price = 1000,
                production = 10,
                min_level = 1) {
        this.name = name;
        this.price = price;
        this.production = production;
        this.min_level = min_level;
        this.number = 0;
        this.power = 0;
        this.power_upgrade_cost = 0;
        this.currentProduction = 0;
    }

    static fromJSON(json) {
        const bot = new ClickBot();
        Object.assign(bot, json);
        return bot;
    }

    buy() {
        this.number += 1;
        this.updateProduction();
    }

    updateProduction() {
        this.currentProduction = Math.round(this.number * this.production * ((1 + 0.1) ** this.power));
    }

    collectClicks() {
        return this.currentProduction;
    }

    upgradePower() {
        this.power += 1;
        this.power_upgrade_cost = Math.round(this.price * ((1 + 0.1) ** this.power) / 2);
        this.updateProduction();
    }
}


export class ClickerModel extends Reactive {
    constructor() {
        super();
        this.total_clicks = 0;
        this.clicks = 0;
        this.level = 0;
        this.total_production = 0;
        this.bots = [
            new ClickBot("Child Bot", 1_000, 10, 1),
            new ClickBot("Teen Bot", 5_000, 100, 2),
            new ClickBot("Adult Bot", 10_000, 500, 3),
        ];
        this.bus = new EventBus();
    }

    static fromJSON(json) {
        const clicker = Object.assign(new ClickerModel(), json);

        if (Array.isArray(json.bots)) {
            clicker.bots = json.bots.map(ClickBot.fromJSON);
        }
        return clicker;
    }

    increment(inc) {
        this.total_clicks += inc;
        this.clicks += inc;

        const milestones = [
            {level: 1, total_clicks: 1_000, event: "milestone_1k"},
            {level: 2, total_clicks: 5_000, event: "milestone_5k"},
            {level: 3, total_clicks: 10_000, event: "milestone_10k"}
        ];

        for (const milestone of milestones) {
            if (this.level < milestone.level && this.total_clicks >= milestone.total_clicks) {
                this.level++;
                this.bus.trigger(milestone.event);
            }
        }
    }

    tick() {
        for (const bot of this.bots) {
            this.total_clicks += bot.collectClicks();
            this.clicks += bot.collectClicks();
        }
    }

    buyBot(name) {
        const bot = this.bots.find(bot => bot.name === name);
        if (bot && this.clicks >= bot.price) {
            this.clicks -= bot.price;
            bot.buy();
        }
        this.total_production = this.updateTotalProduction()
    }

    empowerBot(name) {
        const bot = this.bots.find(bot => bot.name === name);
        if (bot && this.clicks >= bot.power_upgrade_cost) {
            this.clicks -= bot.power_upgrade_cost;
            bot.upgradePower();
        }
        this.total_production = this.updateTotalProduction()
    }

    updateTotalProduction() {
        let total = 0;
        for (const bot of this.bots) {
            total += bot.currentProduction;
        }
        return total;
    }

    toJSON() {
        const json = Object.assign({}, this);
        delete json["bus"];
        return json;
    }
}
