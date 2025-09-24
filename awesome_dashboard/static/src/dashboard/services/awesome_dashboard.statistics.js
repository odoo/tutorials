import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

export function loadStatistics() {
    return rpc("/awesome_dashboard/statistics");
}

export const awesomeDashboardStatisticsService = {
    start() {
        let stats = reactive({});
        const getStats = async () => {
            let newStats = await loadStatistics();
            Object.assign(stats, newStats);
        };

        setInterval(getStats, 1000 * 60 * 10);

        getStats();

        return stats;
    },
};

registry
    .category("services")
    .add("awesome_dashboard.statistics", awesomeDashboardStatisticsService);
