import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

export const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false });
        async function loadStatistics() {
            try {
                const updates = await rpc("/awesome_dashboard/statistics");
                Object.assign(statistics, updates, { isReady: true });
            } catch (error) {
                console.error("Failed to load statistics:", error);
            }
        }
        setInterval(loadStatistics, 10 *60* 1000);
        loadStatistics();
        return statistics;
    },
};
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
