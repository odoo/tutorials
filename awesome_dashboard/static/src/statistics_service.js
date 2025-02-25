import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

export async function getStatistics() {
    const result = await rpc("/awesome_dashboard/statistics");
    return {
        "average_quantity" : result.average_quantity,
        "average_time" : result.average_time,
        "nb_cancelled_orders" : result.nb_cancelled_orders,
        "nb_new_orders" : result.nb_new_orders,
        "total_amount" : result.total_amount,
    }
}


export const statisticsService = { 
    start(){
        return { statistics : memoize(getStatistics) };
    }    
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService);