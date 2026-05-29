import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start(env) {
        const statistics = reactive({});
        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, result);
        }
        loadStatistics();
        setInterval(loadStatistics, 10000);
        return statistics;
    }
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
