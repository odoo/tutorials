import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

// // export const loadStatistics = memoize(async function () {
// //     return await rpc("/awesome_dashboard/statistics", {});
// // });

// // registry.category("services").add("awesome_dashboard.statistics", {
// //     start() {
// //         return { loadStatistics };
// //     },
// // });

// const statistics = reactive({ data: {} });
const statistics = reactive({ isReady: false });

async function fetchStatistics() {
    try {
        const result = await rpc("/awesome_dashboard/statistics", {});
        Object.assign(statistics, result, { isReady: true });
        console.log(statistics)
    } catch (error) {
        console.error("Error fetching statistics:", error);
    }
}

fetchStatistics();

setInterval(fetchStatistics, 10*1000);

registry.category("services").add("awesome_dashboard.statistics", {
    start() {
        return { statistics };
    },
});