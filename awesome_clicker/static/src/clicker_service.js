import { useState } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import  { ClickerModel } from "./clicker_model"

export function useClicker() {
    return useState(useService("awesome_clicker.cliker_service"));
}

export const clickerService = {
    dependencies: ["effect"],
    start(env, services) {
        const clicker = new ClickerModel();
        clicker.bus.addEventListener("MILESTONE_1k", () => {
            services.effect.add({
                type: "rainbow_man",
                message: "Milestone reached! You can now buy clickbots",
            });
        });
        return clicker;
    }
}

registry.category("services").add("awesome_clicker.cliker_service", clickerService)
