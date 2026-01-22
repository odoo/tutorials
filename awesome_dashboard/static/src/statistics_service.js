import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";


async function loadStatistics() {
    return await rpc("/awesome_dashboard/statistics");
}

const statisticsService = {
    start() {
        loadStatistics = memoize(loadStatistics);
        return { loadStatistics };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
