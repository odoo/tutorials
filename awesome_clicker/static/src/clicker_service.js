import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";


const state = reactive({ clicks: 0 });

export const clickerService = {
    start(){
        return {
            state,
            increment(inc) {
                state.clicks += inc;
            }
        }
    }
};

registry.category("services").add("clickerService", clickerService);
