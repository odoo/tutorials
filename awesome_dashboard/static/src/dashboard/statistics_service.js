import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    async: ["loadStatistics"],
    start() {
        const statistics = reactive({ isLoaded: false });

        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            statistics.isLoaded = true;
            Object.assign(statistics, result);
        }

        setInterval(loadStatistics, 10 * 60 * 1000);
        loadStatistics();

        return statistics;
    },
};

registry
    .category("services")
    .add("awesome_dashboard.statistics", statisticsService);
