import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

const statisticsService = {
    start() {
        const loadStatistics = memoize(() => {
            return rpc("/awesome_dashboard/statistics");
        });

        return {
            loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
