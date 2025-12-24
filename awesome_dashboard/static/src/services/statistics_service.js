import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

const statisticsService = {
    async start() {
        const loadStatistics = memoize(() => rpc("/awesome_dashboard/statistics"));

        return {
            loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
