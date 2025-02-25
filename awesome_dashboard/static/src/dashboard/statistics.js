import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export const statisticsService = {
    start() {
        const data = reactive({}); 

        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(data, result); 
        }

        loadStatistics();
        setInterval(loadStatistics, 10 * 1000); 
        return { data, loadStatistics };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
