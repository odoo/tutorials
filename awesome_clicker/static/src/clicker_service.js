/** @odoo-module **/

import { reactive } from "@odoo/owl"
import { registry } from "@web/core/registry";

const clickerService = {
    start(_env) {
        const state = reactive({ clicks: 0, level: 0, clickBots: 0 });
        
        setInterval(() => {
            state.clicks += 10 * state.clickBots;
        }, 10_000);
        
        return {
            state,
            increment(inc) {
                state.clicks += inc;
                if (state.level == 0 && state.clicks >= 1000) state.level = 1;
            },
            buyClickBot() {
                state.clicks -= 1000;
                state.clickBots++;
            }
        }
    }
}

registry.category("services").add("clicker", clickerService);
