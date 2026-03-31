import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl"; 

const statisticsService = {
    start() {
        const stats = reactive({});
        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, result);
        }
        loadStatistics();
        
        setInterval(() => {
            loadStatistics()
        },10000);

        return {
            stats,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);