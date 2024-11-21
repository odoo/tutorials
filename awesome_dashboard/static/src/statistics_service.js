import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

const statisticsService = {
    start() {
        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            return result;
        }
        const memoizedloadStatistics = memoize(loadStatistics);
        

        return memoizedloadStatistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);