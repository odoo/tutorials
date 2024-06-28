/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ClickerModel } from "./clicker_model";

export const clickerService = {
    dependencies: ["effect"],

    start(env, { effect }) {
        const clickerModel = new ClickerModel();

        clickerModel.bus.addEventListener("level_1_is_reached", () => effect.add({
            message: "Level 1 is reached! You can now buy ClickBots",
            type: "rainbow_man",
        }));
        clickerModel.bus.addEventListener("level_2_is_reached", () => effect.add({
            message: "Level 2 is reached! You can now buy BigBots",
            type: "rainbow_man",
        }));
        clickerModel.bus.addEventListener("level_3_is_reached", () => effect.add({
            message: "Level 3 is reached! You can now buy some Power",
            type: "rainbow_man",
        }));

        return clickerModel;
    },
};

registry.category("services").add("clicker_service", clickerService);
