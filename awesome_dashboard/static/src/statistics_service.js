import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

async function loadStatistics() {
    const memoizedRpc = memoize(rpc);
    const statistics = await memoizedRpc("/awesome_dashboard/statistics");
    return statistics;
}

export const statisticsService = {
    async start() {
        return await loadStatistics();
    },
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
