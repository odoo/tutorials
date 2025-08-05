import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

const statisticsService = {
    start(env) {

        const loadStatistics = memoize(async () => {
            const result = await rpc("/awesome_dashboard/statistics");
            return result;
        });

        return {
            loadStatistics,
        };
    }
};

registry.category("services").add("statisticsService", statisticsService);
