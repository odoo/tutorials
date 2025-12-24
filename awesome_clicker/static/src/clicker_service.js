import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

export const clickerService = {
    start() {
        const state = reactive({ clicks: 0 });

        return {
            state,
            increment(val) {
                state.clicks += val;
            },
        };
    },
};

registry.category("services").add("awesome_clicker.game_service", clickerService);
