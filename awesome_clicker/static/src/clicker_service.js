import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const ClickerService = {
    start() {
        const state = reactive({
            clicks: 0,
            level: 0,
            clickBots: 0,
        });

        setInterval(() => state.clicks += 10*state.clickBots, 10 * 1000)

        return {
           state,
           increment(inc) {
              state.clicks += inc
           }
        };
    },
};

registry.category("services").add("clicker", ClickerService);