/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

const clicker_service = {
    dependencies: ["effect"],
    start(env, services) {
        const model = new ClickerModel();
        model.bus.addEventListener("MILESTONE_1k", () => { 
            services.effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy clickbots!",
            });
            console.log("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
        });
        return model;
    },
};

registry.category("services").add("awesome_clicker.service", clicker_service);
