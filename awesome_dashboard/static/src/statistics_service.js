import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start(env) {
        const stats = reactive({ data: {} });

        async function fetchStatistics() {
            console.log("Fetching statistics from API...");
            const result = await rpc("/awesome_dashboard/statistics",{});
            Object.assign(stats.data, result);  
        }

        fetchStatistics();
        setInterval(fetchStatistics, 10000);

        return stats;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);