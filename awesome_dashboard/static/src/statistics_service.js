import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

export async function loadStatistics() {
    return await rpc('/awesome_dashboard/statistics');
}

export const statisticsService = {
    start() {
        return {
            loadStatistics: memoize(loadStatistics),
        }
    },
}

registry.category("services").add("statistics", statisticsService);
