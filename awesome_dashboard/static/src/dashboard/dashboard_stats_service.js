import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

export async function loadStatistics() {
    return rpc("/awesome_dashboard/statistics");
}

export const dashboardStatsService = {
    dependencies: [],
    start() {
        const memoizedLoad = memoize(loadStatistics);

        // Time key integer changing every 10m in order to miss the cache of memoize
        const getTimeKey = () => Math.floor(Date.now() / (1000 * 60 * 10));

        return {
            loadStatistics: () => memoizedLoad(getTimeKey())
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", dashboardStatsService);
