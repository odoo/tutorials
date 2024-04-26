/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";

const state = reactive({ clicks: 0 });

export const clicker_service = {
    start() {
        return { 
            state, 
            increment(inc) {
                state.clicks += inc
            }
        };
    },
};

registry.category("services").add("awesome_clicker.service", clicker_service);
