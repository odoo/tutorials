import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

const dashboardStatisticsService = {
    start(env) {
        const loadData = memoize(() => rpc("/awesome_dashboard/statistics"));

        return {
            loadStatistics: () => loadData()
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", dashboardStatisticsService);
