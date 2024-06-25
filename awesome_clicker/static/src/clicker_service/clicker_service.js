/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";


const clickerService = {
    dependencies: ['effect'],
    start(env, services) {

        const clicker_model = new ClickerModel();
        clicker_model.bus.addEventListener("MILESTONE_REACHED", (event) => {
            services.effect.add({message: `You have reached level ${event.detail}!`}
        )});

        return clicker_model;
    }
}

registry.category("services").add("awesome_clicker.clickCounter", clickerService);
