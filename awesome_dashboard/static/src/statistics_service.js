import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";


const getStatisticsMemoize = memoize(async () => {
    return rpc("/awesome_dashboard/statistics");
});

const getStatistics = (async () => {
    return rpc("/awesome_dashboard/statistics");
});

const statisticsService = {
    start() {
        return { getStatistics, getStatisticsMemoize };
    },
};

registry.category("services").add("statistics", statisticsService);
