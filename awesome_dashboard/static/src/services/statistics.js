import { rpc } from "@web/core/network/rpc"
import { registry } from "@web/core/registry"
import { memoize } from "@web/core/utils/functions";

export const statistics = {
    depedencies: [],
    async start(env){
        const loadStatistics = memoize(async()=>{
            return await rpc("/awesome_dashboard/statistics");
        })
        return { loadStatistics };
    }
};

registry.category("services").add("awesome_dashboard.statistics",statistics)
