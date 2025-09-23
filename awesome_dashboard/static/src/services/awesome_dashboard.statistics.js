import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

export function loadStatistics() {
    return rpc("/awesome_dashboard/statistics")
}

export const awesomeDashboardStatisticsService = {
    start() {
        return { loadStatistics: memoize(loadStatistics) };
    }
}

registry.category(
    "services").add(
        "awesome_dashboard.statistics", awesomeDashboardStatisticsService)
