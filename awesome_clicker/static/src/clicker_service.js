/** @odoo-module **/
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { ClickerModel } from "./clicker_model";
import { EventBus } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

const clickerService = {
    dependencies: ["effect"],
    start(_, { effect }) {
        const clickerModel = new ClickerModel();

        clickerModel.bus.addEventListener("MILESTONE_1k", (event) => {
            console.log("HELLO FROM SERVICE");
            effect.add({
                type: "rainbow_man", // can be omitted, default type is already "rainbow_man"
                message: "Boom! You can now buy clickbots.",
            });
        });

        return clickerModel;
    },
};

registry.category("services").add("awesome_clicker.clicker_service", clickerService);
