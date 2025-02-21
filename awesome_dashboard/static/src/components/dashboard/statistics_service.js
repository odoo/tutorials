import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statisticsService = {

    start() {
        const interval = 10 * 1000;
        const stats = reactive({ isReady: false });

        async function loadStatistics() {
            const newStats = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, newStats, { isReady: true });
        };

        setInterval(loadStatistics, interval);
        loadStatistics();
        return stats;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
