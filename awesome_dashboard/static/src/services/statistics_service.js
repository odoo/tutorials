import { reactive } from '@odoo/owl'
import { registry } from '@web/core/registry';
import { rpc } from "@web/core/network/rpc";

let stats = reactive({
    average_quantity: 0,
    nb_new_orders: 0,
    nb_cancelled_orders: 0,
    average_time: 0,
    orders_by_size: {},
    total_amount: 0

}, () => {});

const loadStatistics = async () => {
    let result = await rpc("/awesome_dashboard/statistics");
    stats.nb_new_orders = stats.nb_new_orders + 1
    Object.assign(stats, result);    
};

export const statisticsService = {
    dependencies: [],
    start() {
        loadStatistics();
        // setInterval(() => {
        //     loadStatistics();
        // }, 1000);
        return stats;
    },
};

registry.category("services").add("statistics", statisticsService);
