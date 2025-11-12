import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const REFRESH_INTERVAL = 60000;

const statisticsService = {
    start() {
        const stats = reactive({});

        async function fetchStats(){
            try{
                const loadStatistics = await rpc("/awesome_dashboard/statistics");
                Object.assign(stats, loadStatistics);
            }
            catch (error){
                console.error("Error fetching statistics:", error);
            }
        }

        fetchStats();
        setInterval(fetchStats, REFRESH_INTERVAL);

        return { stats };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
