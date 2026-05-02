
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export const dashStatService = {
    start(env) {
        const state = reactive({
            data: {},
        });

        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(state.data, result);
            return state.data;
        }

        setInterval(loadStatistics, 1000);

        return {
            state,
            loadStatistics,
        };
    },
};
registry.category("services").add("stat_dash", dashStatService);