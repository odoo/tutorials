import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statisticsService = {
    start() {
        let statistics = reactive({ isReady: false });
        async function loadStatistics() {
            Object.assign(statistics, await rpc("/awesome_dashboard/statistics"), { isReady: true });
        }

        // Refresh every 10 seconds for testing
        //const interval = 10000;
        // Refresh every 10 minutes for real
        const interval = 600000;
        
        setInterval(loadStatistics, interval);
        loadStatistics();
        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
