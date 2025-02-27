import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";
import { memoize } from "@web/core/utils/functions";

/** Main stat function */
export async function getStatistics() {
    const result = await rpc("/awesome_dashboard/statistics");
    return {
        "average_quantity" : result.average_quantity,
        "average_time" : result.average_time,
        "nb_cancelled_orders" : result.nb_cancelled_orders,
        "nb_new_orders" : result.nb_new_orders,
        "total_amount" : result.total_amount,
        "orders_by_size" : result.orders_by_size,
    }
}

/** Stats have the same values during all the runtime */
export const staticStatisticsService = { 
    start(){
        return { statistics : memoize(getStatistics) };
    }    
}

registry.category("services").add("awesome_dashboard.statistics.static", staticStatisticsService);


/** Stats values change every few seconds !! */
export const statisticsService = { 
    start(){
        let statistics = reactive({ isReady: false });

        async function loadData() {
            const updates = await getStatistics();
            Object.assign(statistics, updates, { isReady: true });
        }

        setInterval(loadData, 5*1000);
        loadData();
        
        return statistics;
    }    
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService);