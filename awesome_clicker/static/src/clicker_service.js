import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

const myService = {
    start() {
        const state = reactive({
            clicks: 0,
            level: 0,
            clickBots: 0,
        });

        async function loadBotClicks() {
            state.clicks += state.clickBots*10
        }

        setInterval(loadBotClicks, 10*1000);

        return {
            state,
            increment(inc) {
                state.clicks += inc
                if (state.clicks >= 1000)
                    state.level = 1
            }
        };
    }
};

registry.category("services").add("awesome_clicker.clicker_service", myService);
