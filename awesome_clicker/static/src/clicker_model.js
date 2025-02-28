/* @odoo-module */
import { Reactive } from "@web/core/utils/reactive";
import { EventBus } from "@odoo/owl";
import { getReward } from "./click_reward";


export class ClickerModel extends Reactive {
    constructor(){
        super();
        this._clicks = 0;
        this._level = 0;
        this._power = 1;
        this._bots = {
            clickBot: {
                price: 1000,
                level: 1,
                increment: 10,
                purchased: 0,
            },
            bigBot: {
                price: 5000,
                level: 2,
                increment: 100,
                purchased: 0,
            },
        };
        this.trees = {
            pearTree: {
                price: 1000000,
                level: 4,
                produce: "pear",
                purchased: 0
            },
            cherryTree: {
                price: 1000000,
                level: 4,
                produce: "cherry",
                purchased: 0
            },
        };
        this.fruits = {
            pear: 0,
            cherry: 0,
        };
        this._milestones = [
            { clicks: 1000, unlock: "clickBot" },
            { clicks: 5000, unlock: "bigBot" },
            { clicks: 100000, unlock: "power multiplier" },
            { clicks: 1000000, unlock: "trees" },
        ];
        this._bus = new EventBus();
        this._tick = 0;
    }

    setup(){}

    get clicks(){ return this._clicks; }

    get level(){ return this._level; }

    get power() { return this._power; }
    set power(pwr){ this._power = pwr; }

    get bots() { return this._bots; }

    get bus(){ return this._bus; }

    increment(inc){
        this._clicks += inc;
        if(this._milestones[this._level]
            && this._clicks >= this._milestones[this._level].clicks){
            this.bus.trigger("MILESTONE", this._milestones[this._level]);
            this._level++;
        }
    }

    tick(){
        this._tick++;
        for(const bot in this._bots){
            this.increment(this._bots[bot].increment * this._power * this._bots[bot].purchased);
        }
        if(this._tick === 3){
            for(const tree in this.trees){
                this.fruits[this.trees[tree].produce] += this.trees[tree].purchased;
            }
            this._tick = 0;
        }
    }

    buyBot(name){
        if(!Object.keys(this._bots).includes(name)){
            throw new Error(`Invalid bot name ${name}`);
        }
        if(this._clicks < this._bots[name].price){
            return false;
        }
        this.increment(-this._bots[name].price);
        this._bots[name].purchased++;
    }

    buyPower(nb){
        if(this._clicks >= 50000 && this._level >= 3){
            this._power += nb;
            this.increment(-50000*nb);
        }
    }

    buyTree(name){
        if(this._clicks >= this.trees[name].price){
            this.trees[name].purchased++;
            this.increment(-this.trees[name].price);
        }
    }

    getReward(){
        const reward = getReward(this._level);
        this._bus.trigger("REWARD", reward);
    }

}
