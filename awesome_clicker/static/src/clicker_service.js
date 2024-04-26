/** @odoo-module **/

import { EventBus } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

const clickerService = {
    dependencies: ["effect"],
    start(_env, { effect }) {
        const bus = new EventBus();
        const clicker = new ClickerModel(bus);

        bus.addEventListener("MILESTONE_1k", () => {
            effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy click bots.",
            });
        });
        bus.addEventListener("MILESTONE_5k", () => {
            effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy big bots.",
            });
        });
        bus.addEventListener("MILESTONE_100k", () => {
            effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy power.",
            });
        });

        return clicker;
    }
}

registry.category("services").add("clicker", clickerService);
