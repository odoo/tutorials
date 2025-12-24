import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

const loadStatistics = memoize(async () => {
    return await rpc("/awesome_dashboard/statistics");
});

export const statisticsService = {
    start() {
        return {
            loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
