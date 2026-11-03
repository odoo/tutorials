import { Reactive } from "@web/core/utils/reactive";
import {EventBus} from "@odoo/owl";
import { rewards } from "../click_reward/click_rewards";
import { choose } from "../utils";
import { CURENTVERSION } from "../clicker_migration/clicker_migration";


export class ClickerModel extends Reactive{
    constructor()
    {
        super();
        this.clicks = 0;
        this.level = 0;
        this.power = 1,
        this.bots = {
            clickBot:
            {
                price:100,
                quantity:0,
                value:10,
            },
            bigClickBot: 
            {
                price:500,
                quantity:0,
                value:1000,
            }
        };
        this.trees = {
            cherry:
            {
                quantity:0,
                fruit:0,
                price:10000
            },
            pear: {
                quantity:0,
                fruit:0,
                price:10000
            },
            peach: {
                quantity:0,
                fruit:0,
                price:10000
            }
        }
        this.event = new EventBus();
        this.version = CURENTVERSION;
    }

    get milestones()
    {
        return[
            this.bots.clickBot.price,this.bots.bigClickBot.price,1000,10000
        ]
    }
    get powerPrice(){return 5000}

    tickBot(){
        let add = 0;
        for(const bot in this.bots){
            add += this.bots[bot].quantity * this.bots[bot].value;
        }
        this.addClicks(this.power * add);
    }
    tickFruit(){
        for(const tree in this.trees)
        {
            this.trees[tree].fruit += this.trees[tree].quantity;
        }
    }

    addClicks(val)
    {
        if(this.level < this.milestones.length && this.clicks >= this.milestones[this.level])
            {
                this.level++;
                this.event.trigger("MILESTONE1K");
            }
        this.clicks+= val;
    }

    buyBot(id)
    {
        const bot = Object.keys(this.bots)[id]
        if (this.clicks < this.bots[bot].price)
            {
                return false;
            }
        this.clicks -= this.bots[bot].price;
        this.bots[bot].quantity++;       
    }
    buyPower()
    {
        if(this.clicks < this.powerPrice)
        {
            return false;
        }
        this.clicks -= this.powerPrice;
        this.power ++;
    }
    buyTrees(id)
    {
        const tree = Object.keys(this.trees)[id]
        if (this.clicks < this.trees[tree].price)
            {
                return false;
            }
        this.clicks -= this.trees[tree].price;
        this.trees[tree].quantity++;
    }
    giveReward()
    {
        const available = []
        for(const reward in rewards )
        {
            if ((rewards[reward].minLevel == undefined || rewards[reward].minLevel <= this.level)&&(rewards[reward].maxLevel == undefined || rewards[reward].maxLevel >= this.level))
            {
                available.push(rewards[reward]);
            }       
        }
        let reward = choose(available);
        this.event.trigger("REWARD",reward);
        return reward;
    }
    toJSON(){
        const json = Object.assign({}, this);
        delete json["event"];
        return JSON.stringify(json);
    }
    static fromJSON(json)
    {
        if(!json)
        {
            return undefined;
        }

        try{
            return Object.assign(new ClickerModel,JSON.parse(json));
        }catch(e)
        {
            console.log("Corrupted save data!");
            return undefined;
        }
    }
}
