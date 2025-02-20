import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

const orderStatisticsService = {
    start() {
        return {
            loadStatistics: memoize(async () => await rpc("/awesome_dashboard/statistics"))
        }
    }
}

registry.category("services").add("awesome_dashboard.statistics", orderStatisticsService);
