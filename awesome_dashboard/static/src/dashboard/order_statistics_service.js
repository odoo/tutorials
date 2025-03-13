import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const orderStatisticsService = {
    start() {
        const orderStats = reactive({});

        async function loadStatistics() {
            const latestStats = await rpc("/awesome_dashboard/statistics");
            Object.assign(orderStats, latestStats);
        }
        loadStatistics();
        setInterval(loadStatistics, 10*60*1000);

        return orderStats;
    },
}

registry.category("services").add("awesome_dashboard.statistics", orderStatisticsService);
