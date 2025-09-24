import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";


export const StatisticsService = {
    start() {
        return {
            data: memoize(async() => await rpc("/awesome_dashboard/statistics"))
        };
    }
};
registry.category("services").add("awesome_dashboard.statistics", StatisticsService);
