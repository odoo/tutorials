import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statisticsService = {
    dependencies: [],
    start() {
        const statistics = reactive({});

        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");

            Object.keys(statistics).forEach((k) => delete statistics[k]);
            Object.assign(statistics, result);
        }        

        loadStatistics();
        setInterval(loadStatistics, 600_000);

        return {
            statistics,
            reload: loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);