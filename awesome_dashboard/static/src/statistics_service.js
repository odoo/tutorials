import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const REFRESH_DELAY = 10 * 1000; // use 10 * 60 * 1000 for the real 10 minutes

const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false });

        async function loadStatistics() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });
        }

        loadStatistics();
        setInterval(loadStatistics, REFRESH_DELAY);

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
