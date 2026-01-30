
import { memoize } from "@web/core/utils/functions";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const statsService = {
    start(env) {
        const loadStatistics = memoize(async () => {
            return await rpc("/awesome_dashboard/statistics");
        });

        return {loadStatistics};
    },
};

registry.category("services").add("awesome_dashboard.statistics", statsService);
