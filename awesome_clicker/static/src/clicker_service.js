/** @odoo-module **/
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
const clickerService = {
    start() {
        const state = reactive({ clicks: 0, level: 0, clickBots: 0 });

        setInterval(() => {
            state.clicks += state.clickBots * 10;
            console.log(state.clicks);
        }, 1000 * 10);

        return {
            state,
            increment(inc) {
                state.clicks += inc;
                console.log(state.clicks);
            },
            incrementClickBots(inc) {
                state.clickBots += inc;
                state.clicks -= inc * 1000;
            },
        };
    },
};

registry.category("services").add("awesome_clicker.clicker_service", clickerService);
