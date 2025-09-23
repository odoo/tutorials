import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start(env) {
        const statistics = reactive({ isReady: false });

        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, result, { isReady: true });
        }

        setInterval(loadStatistics, 10000);
        loadStatistics();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
