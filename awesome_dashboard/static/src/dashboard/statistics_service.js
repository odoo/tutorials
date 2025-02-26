import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

// Cache statistics
/* 
const statisticsService = { 
    dependencies: [],
    start() {
        return {
            loadStatistics: memoize(async function () {
                return await rpc("/awesome_dashboard/statistics");
            }),
        };
    },
};
 */

// real life update
const statistics = reactive({ stats: {} })
async function fetchStatistics() {
    const result = await rpc('/awesome_dashboard/statistics', {});
    Object.assign(statistics.stats, result)
    return statistics.stats
}


const statisticsService = {
    dependencies: [],
    start() {
        fetchStatistics(); 
        setInterval(() => fetchStatistics(), 10000);
        return { loadStatistics: fetchStatistics }
    }
}

registry.category("services").add("statistics", statisticsService);
