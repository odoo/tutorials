import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const StatisticsService = {
    start() {
        const stats = reactive({});

        async function loadData() {
            const update = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, update);
        }

        setInterval(loadData, 10000);
        loadData();

        return stats;
    },
    
};

registry.category("services").add("awesome_dashboard.statistics", StatisticsService);