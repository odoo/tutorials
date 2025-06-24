import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

const statisticsService = {
    async: [
        "getStatistics",
    ],
    start(){
        
        return{
            getStatistics: memoize(() => rpc("/awesome_dashboard/statistics"))
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
