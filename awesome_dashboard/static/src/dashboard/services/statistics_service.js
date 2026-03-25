import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statisticsService = {
    start() {
        const state = reactive({
            data: null,
        });

        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            state.data = result;
        }

        const initialLoad = loadStatistics();

        setInterval(loadStatistics, 100000);

        return {
            state,
            loadStatistics,
            initialLoad,
        };
    },
};

registry
    .category("services")
    .add("awesome_dashboard.statistics", statisticsService);
