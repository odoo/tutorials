import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const state = reactive({});

        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");

            Object.assign(state, result);
        }

        setInterval(loadStatistics, 10000);

        return {
            state,
            loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
