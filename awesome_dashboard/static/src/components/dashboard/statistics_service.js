import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export const StatisticsService = {
    start() {
        const statistics = reactive({
            isReady: false,
        });

    async function loadStatistics() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });

    }
    setInterval(loadStatistics, 60000); // Refresh every minute
    loadStatistics();

    return statistics;
    }
};

registry.category("services").add("awesome_dashboard.statistics", StatisticsService);
