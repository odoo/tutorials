import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statisticsService = {
    dependencies: [],
    start() {
        const statistics = reactive({});
        async function _fetchStats() {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data);
        }
        _fetchStats();

        setInterval(_fetchStats, 5000);

        return {
            statistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
