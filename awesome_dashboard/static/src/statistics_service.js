import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

// const statisticsService = {
//     async: ["loadStatistics"],

//     start(){

//         const loadStatistics = memoize(function loadStatistics(){
//             return rpc('/awesome_dashboard/statistics',{})
//         });
//         return {
//             loadStatistics,
//         }
//     },
// }

// registry.category("services").add(
//     "awesome_dashboard.statistics",
//     statisticsService
// )



const statisticsService = {
    start() {
        const statistics = reactive({});

        async function loadStatistics() {
            const data = await rpc(
                "/awesome_dashboard/statistics",
                {}
            );

            Object.assign(statistics, data);
        }

        // Initial data loading
        loadStatistics();

        // Refresh every 10 seconds (testing)
        setInterval(loadStatistics, 10000);

        return statistics;
    },
};

registry.category("services").add(
    "awesome_dashboard.statistics",
    statisticsService
);