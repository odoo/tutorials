import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { registry } from "@web/core/registry";


const statisticsService = {
    start() {
        return {
            loadStatistics: memoize(() => rpc("/awesome_dashboard/statistics")),
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
