import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start() {
        const loadStatistics = memoize(() => rpc("/awesome_dashboard/statistics"));
        return {
            loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
