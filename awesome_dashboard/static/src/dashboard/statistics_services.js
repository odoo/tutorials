import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    dependencies: [],
    start() {

        const statistics = reactive({});

        async function loadStatistics () {
            try {
                const data = await rpc("/awesome_dashboard/statistics");
                Object.assign(statistics, data); 
                return statistics;
            } catch (error) {
                console.error("Error loading statistics:", error);
                statistics.error = error; 
                return statistics;
            }
        };
        loadStatistics();
        setInterval(loadStatistics, 10000); 
        return {
            statistics,
        };
    },
};
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
