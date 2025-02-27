import { useState } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import  { ClickerModel } from "./clicker_model"

export function useClicker() {
    return useState(useService("awesome_clicker.cliker_service"));
}

export const clickerService = {
    start() {
        return new ClickerModel();
    }
}

registry.category("services").add("awesome_clicker.cliker_service", clickerService)
