import {registry} from "@web/core/registry";
import {rpc} from "@web/core/network/rpc";
import {memoize} from "@web/core/utils/functions";

export const loadStatistics = {

    start: memoize(async () => {
        return await rpc("/awesome_dashboard/statistics");
    })
}

registry.category("services").add("awesome_dashboard.statistics", loadStatistics);
