import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


export const dashboardService = {
    start() {
        const statistics = reactive({})

        const loadStatistics = async () => {
            const updateStatistics = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updateStatistics);
        }
        setInterval(loadStatistics, 10 * 60 * 1000); // Calls after every 10 minutes
        loadStatistics();
        return statistics;
    }
}

registry.category("services").add("awesome_dashboard.statistics", dashboardService);
