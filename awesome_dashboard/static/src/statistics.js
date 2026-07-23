import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start() {
        return {
            loadStatistics: memoize(async () => {
                const result = await rpc("/awesome_dashboard/statistics");
                console.log(result);
                return result;
            }),
        }
    }
};

registry.category("services").add("statistics", statisticsService);