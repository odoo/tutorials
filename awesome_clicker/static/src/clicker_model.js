import { Reactive } from "@web/core/utils/reactive";
import { humanNumber } from "@web/core/utils/numbers";
import { EventBus } from "@odoo/owl";
import { browser } from "@web/core/browser/browser"
import { state_migrations } from "./clicker_state_migrations"

export class Clicker extends Reactive {
    constructor() {
        super();
        this.version = 2;
        this.bus = new EventBus();

        const stored = JSON.parse(browser.sessionStorage.getItem("clicker_state"));
        stored ? this._reloadState(stored) : this._setInitialState();

        setInterval(() => {
            this.increment((10 * this.clickbots + 100 * this.bigbots) * this.power);
        }, 10000);

        setInterval(() => {
            this.fruits.cherries += this.trees.cherries;
            this.fruits.peaches += this.trees.peaches;
            this.fruits.pears += this.trees.pears;
        }, 30000);

        setInterval(() => {
            browser.sessionStorage.setItem(
                "clicker_state",
                JSON.stringify(this)
            );
        }, 10000);
    }

    _setInitialState() {
        this.clicks = 0;
        this.clicks_text = "0"
        this.level = 0;
        this.clickbots = 0;
        this.bigbots = 0;
        this.power = 1;
        this.fruits = { cherries: 0, peaches: 0, pears: 0 }
        this.trees = { cherries: 0, peaches: 0, pears: 0 }
    }

    _reloadState(state) {
        if (state.version != this.version) {
            const migration = state_migrations.filter((el) => el.from == state.version && el.to == this.version)
            if (migration.length != 1) {
                this._setInitialState();
                return;
            }
            state = migration[0].apply(state);
        }
        for (const [key, value] of Object.entries(state)) {
            if (!this[key]) { this[key] = value; }
        }
    }

    increment(inc) {
        this.clicks += inc;
        this.clicks_text = humanNumber(this.clicks, { decimals: (this.clicks > 1000) ? 1 : 0 });
        if (this.clicks >= 1000 && this.level < 1) {
            this.level += 1;
            this.bus.trigger("MILESTONE_1k");
        }
        if (this.clicks >= 5000 && this.level < 2) {
            this.level += 1;
            this.bus.trigger("MILESTONE_5k");
        }
        if (this.clicks >= 100000 && this.level < 3) {
            this.level += 1;
            this.bus.trigger("MILESTONE_100k");
        }
        if (this.clicks >= 1000000 && this.level < 4) {
            this.level += 1;
            this.bus.trigger("MILESTONE_1M");
        }
    }

    buyBot() {
        this.clickbots += 1;
        this.increment(-1000);
    }

    buyBigBot() {
        this.bigbots += 1;
        this.increment(-5000);
    }

    buyPower() {
        this.power += 1;
        this.increment(-50000);
    }

    buyTree(idx) {
        if (idx == 0) {
            this.trees.cherries += 1;
            this.increment(-1000000);
        }
        else if (idx == 1) {
            this.trees.peaches += 1;
            this.increment(-1000000);
        }
        else if (idx == 2) {
            this.trees.pears += 1;
            this.increment(-1000000);
        }
    }

    getTotalTrees() {
        return Object.values(this.trees).reduce((acc, val) => { return acc + val }, 0);
    }

    getTotalFruits() {
        return Object.values(this.fruits).reduce((acc, val) => { return acc + val }, 0);
    }
}
