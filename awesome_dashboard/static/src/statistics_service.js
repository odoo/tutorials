import { reactive } from "@odoo/owl"
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";


const statistics = reactive({ stats: {} })

async function fetchStatistics() {
    const result =  await rpc("/awesome_dashboard/statistics", {});
    Object.assign(statistics.stats, result);
    console.log(statistics)
}

export const statisticsService = {
    dependencies: [],
    start() {
        fetchStatistics();
        setInterval(fetchStatistics, 50000);

        return {stats: statistics.stats };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);