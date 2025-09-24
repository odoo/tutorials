import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

const fetchStatistics = () => {
    return rpc("/awesome_dashboard/statistics");
}

export const statisticsService = {
    start() {
        return {
            loadStatistics: memoize(() => fetchStatistics()),
        };
    },
}

registry.category("services").add("statistics_service", statisticsService);