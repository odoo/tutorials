// imports
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

// fetches and manages dashboard statistics data.
const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false });

        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });
        }

        // refreshing data every 10 minutes
        setInterval(loadData, 10*60*1000);
        loadData()

        return statistics;
    },
};
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
