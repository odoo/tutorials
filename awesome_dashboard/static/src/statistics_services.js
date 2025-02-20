
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
// import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start() {
        // Memoize the RPC call to cache the result
        // const loadStatistics = memoize(async () => {
        //     return await rpc("/awesome_dashboard/statistics");
        // });

        // return {
        //     loadStatistics, 
        // };
        const statistics = reactive({ isReady: false });
        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });
        }
        setInterval(loadData, 10*60*1000);
        loadData();
        return statistics;
    },
};

// Register the service
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
