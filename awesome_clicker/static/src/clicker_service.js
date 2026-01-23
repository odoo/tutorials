import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { ClickerModel, LEVEL_REQUIREMENTS } from "./clicker_model";


const clickerService = {
    dependencies: ["effect"],
    start(env, services) {
        let clicker_model = new ClickerModel();

        LEVEL_REQUIREMENTS.forEach(milestone =>
            clicker_model.bus.addEventListener(
                milestone.event_name,
                () => services.effect.add({ message: milestone.message }),
            )
        )
        return clicker_model;
    }
}

export function useClicker() {
    return useState(useService("awesome_clicker.clicker_service"));
}

registry.category("services").add("awesome_clicker.clicker_service", clickerService);
