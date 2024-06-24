/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";


const clickerService = {
    start(env) {

        const state = reactive({ clicks: 990, level: 1, clickBots: 0 });

        return {
            state,
            increment(inc) {
               state.clicks += inc;
            },
            buyClickbot() {
                state.clickBots++;
                state.clicks -= 1000;
                setInterval(() => state.clicks += 10, 10*1000);
            }
         };
    }
}

registry.category("services").add("awesome_clicker.clickCounter", clickerService);
