import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

const loadStatistics = memoize(async () => {
    const response = await rpc("/awesome_dashboard/statistics");
    return {
        numOrders: response.nb_new_orders,
        newOrders: response.total_amount,
        ShirtByOrder: response.average_quantity,
        cancelledOrders: response.nb_cancelled_orders,
        timeFromNew: response.average_time,
        sizeLabels: Object.keys(response.orders_by_size),
        sizeValues: Object.values(response.orders_by_size),
    }
})

const dashboardStatistics = {
    start(env) {
        return { loadStatistics }
    }
}

registry.category("services").add("awesome_dashboard.statistics", dashboardStatistics);