import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const StatisticsService = {
    start() {
        const statistics = reactive({ data: {} });

        async function fetchStatistics() {
            try {
                const result = await rpc("/awesome_dashboard/statistics", {});
                Object.assign(statistics.data, result);
            } catch (error) {
                console.error("Error fetching statistics:", error);
            }
        }
        
        fetchStatistics();

        setInterval(fetchStatistics, 5000);
        
        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", StatisticsService);
