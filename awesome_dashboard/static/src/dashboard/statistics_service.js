import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false })
        let refreshInterval = null;
        
        async function loadData(){
            const changes = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, changes, { isReady: true });
        }

        function startAutoRefresh() {
            if (!refreshInterval) {
                loadData();
                refreshInterval = setInterval(loadData, 10*60*1000);
            }
        }

        // Stop polling when dashboard is closed
        function stopAutoRefresh() {
            if (refreshInterval) {
                clearInterval(refreshInterval);
                refreshInterval = null;
            }
        }

        return {statistics, startAutoRefresh, stopAutoRefresh};
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
