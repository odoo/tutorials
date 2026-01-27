import { registry } from "@web/core/registry";
import { ClickerModel } from "../models/clicker_model";
import { clickerModelKey } from "../models/clicker_model";
import { migrate } from "../models/clicker_migration";

const allEvents = [
    {eventName: "MILESTONE_1k", description: "Milestone reached! You can now buy clickbots"},
    {eventName: "MILESTONE_5k", description: "Milestone reached! You can now buy big clickbots"},
    {eventName: "MILESTONE_100k", description: "Milestone reached! You can now buy power"},
    {eventName: "MILESTONE_1M", description: "Milestone reached! You can now buy trees"}  
]

const clickerService = {
    dependencies: ["effect"],
    start(env, {effect}) {
        let stored = localStorage.getItem(clickerModelKey);
        let clicker;
        
        if(stored) {
            clicker = new ClickerModel(JSON.parse(stored));
            if(migrate(clicker)) localStorage.setItem(clickerModelKey, JSON.stringify(clicker));
        }
        else clicker = new ClickerModel();

        for(let event of allEvents) {
            clicker.bus.addEventListener(event.eventName, () => {
                effect.add({
                    type: 'rainbow_man',
                    message: event.description
                })
            })
        }

        return { clicker }
    }
}

registry.category("services").add("clicker", clickerService);
