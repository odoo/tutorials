import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

async function fetchStatistics() {
    return await rpc("/awesome_dashboard/statistics", {});
}

const loadStatistics = memoize(fetchStatistics);

export const statisticsService = {
    dependencies: [],
    start() {
        return { loadStatistics };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);