import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";


const statisticsService = {
    start() {
        let statistics = reactive({ isReady: false });

        async function loadStatistics() {
            let updated_stats = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updated_stats, { isReady: true });
        }

        setInterval(loadStatistics, 10 * 60 * 1000);
        loadStatistics();
        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
