import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

export async function loadStatistics() {
    return rpc("/awesome_dashboard/statistics");
}

export const statisticsService = {
    start() {
        return { loadStatistics: memoize(loadStatistics) };
    }
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService)
