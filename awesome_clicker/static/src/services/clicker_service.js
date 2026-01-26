import { registry } from "@web/core/registry";
import { ClickerModel } from "../models/clicker_model";

const allEvents = [
    {eventName: "MILESTONE_1k", description: "Milestone reached! You can now buy clickbots"},
    {eventName: "MILESTONE_5k", description: "Milestone reached! You can now buy big clickbots"},
    {eventName: "MILESTONE_100k", description: "Milestone reached! You can now buy power"}    
]

const clickerService = {
    dependencies: ["effect"],
    start(env, {effect}) {
        let clicker = new ClickerModel();

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
