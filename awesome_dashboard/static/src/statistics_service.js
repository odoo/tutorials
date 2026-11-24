import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false });

        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });
        }

        loadData();
        // Use 10 * 1000 (10s) for testing, or 10 * 60 * 1000 (10m) in production
        setInterval(loadData, 10 * 1000);

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
