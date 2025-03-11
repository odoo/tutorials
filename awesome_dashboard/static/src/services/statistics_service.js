import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const REFRESH_INTERVAL = 60000;

const StatisticsService = {
    start() {
        const stats = reactive({});
        async function fetchStats() {
            try {
                const latestStats = await rpc("/awesome_dashboard/statistics");
                Object.assign(stats, latestStats);
            }
            catch(error) {
                console.error("Error fetching statistics:", error);
            }
        }
        fetchStats();
        setInterval(fetchStats, REFRESH_INTERVAL);
        return { stats };
    },
};

registry.category("services").add("awesome_dashboard.statistics", StatisticsService);
