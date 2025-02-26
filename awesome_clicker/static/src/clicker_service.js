/** @odoo-module **/
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

export const clickerService = {
    dependencies: ["action"],

    start(env, { action }) {
        const state = reactive({
            clicks: 0,
        });
        const i = 1;
        return {
            state,
            increment() {
                state.clicks += i;
            },
            openClickerClientAction() {
                action.doAction({
                    type: "ir.actions.client",
                    tag: "clicker_client_action.ClickerClientAction",
                    target: "new",
                    name: "Clicker"
                });
            },
        };
    }
};
registry.category("services").add("clicker", clickerService);

