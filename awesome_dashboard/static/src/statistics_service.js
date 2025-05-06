import { reactive } from "@odoo/owl"
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";


const statisticsService = {
    start() {
        const statistics = reactive({});
        
        async function loadStatistics() {
            const fetch_statistics = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, fetch_statistics);
        };
        setInterval(loadStatistics, 1000*60*10); // 1000 ms (1 second) times 60 times 10 = 10 minutes

        loadStatistics();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
