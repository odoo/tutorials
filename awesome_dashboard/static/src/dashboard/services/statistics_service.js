/** @odoo-module **/
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const REFRESH_INTERVAL = 10000;

export const statisticsService = {
    dependencies: [],
    async start(env) {
        const state = reactive({ dashboardItems: {} });

        async function loadStatistics() {
            const data = await rpc("/awesome_dashboard/statistics", {});
            Object.assign(state.dashboardItems, data); // Update in place
        }

        // Initial load
        await loadStatistics();

        // Periodic refresh
        setInterval(loadStatistics, REFRESH_INTERVAL);

        return {
            state,
        };
    },
};

// Register the service
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
