import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start(env) {
        const statistics = reactive({});

        async function loadStatistics() {
            console.log("Loading statistics...");
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data);
            console.log("Statistics loaded:", statistics);
        }

        const interval = setInterval(loadStatistics, 10 * 60 * 1000);
        loadStatistics();

        return statistics;
    },
};

registry.category("services").add("statistics_service", statisticsService);
