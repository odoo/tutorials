import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const statistics = reactive({});

        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, result);
        }

        loadStatistics();

        setInterval(loadStatistics, 10 * 1000);

        return { statistics, loadStatistics };
    },
};

registry.category("services").add(
    "awesome_dashboard.statistics",
    statisticsService
);