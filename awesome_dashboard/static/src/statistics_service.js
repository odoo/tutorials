import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false });

        async function loadStatistics() {
            try {
                const result = await rpc("/awesome_dashboard/statistics");
                Object.assign(statistics, result);
                statistics.isReady = true;
            } catch (error) {
                console.error("Failed to load statistics:", error);
            }
        }

        loadStatistics();
        setInterval(loadStatistics, 10000);

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
