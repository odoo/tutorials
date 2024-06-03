/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { ClickerModel, MILESTONE_1K, MILESTONE_5K } from "./clicker_model";
import { EventBus, useState } from "@odoo/owl";

export const useClicker = () => useState(useService("awesome_clicker.clicker_service"));


const ClickerService = {
    dependencies: ["effect"],
    start: (env, {effect}) => {
        const bus = new EventBus();
        const model = new ClickerModel(bus);

        bus.addEventListener(MILESTONE_1K, () => {
            effect.add({
                type: "rainbow_man",
                message: "You've reached level 1! You can now buy click bots!"
            })
        })
        bus.addEventListener(MILESTONE_5K, () => {
            effect.add({
                type: "rainbow_man",
                message: "You've reached level 2! You can now buy big click bots!"
            })
        })

        return model;
    },
};

registry.category("services").add("awesome_clicker.clicker_service", ClickerService);
