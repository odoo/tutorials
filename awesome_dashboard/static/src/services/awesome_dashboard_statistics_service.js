import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions"

export const awesomeDashboardStatisticsService = {
    async: ["loadStatistics"],
    start() {
        const loadStatistics = memoize(() => rpc("/awesome_dashboard/statistics"))
        return {
            stats: loadStatistics()
        }
    },
}

registry.category("services").add("awesome_dashboard.statistics", awesomeDashboardStatisticsService);
