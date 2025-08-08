/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsObj = reactive({
    nb_new_orders: 0,
    total_amount: 0,
    average_quantity: 0,
    nb_cancelled_orders: 0,
    average_time: 0,
    orders_by_size: {}
});

const loadStatistics = async() => {
    const result = await rpc("/awesome_dashboard/statistics");
    statisticsObj.nb_new_orders = result.nb_new_orders;
    statisticsObj.total_amount = result.total_amount;
    statisticsObj.average_quantity = result.average_quantity;
    statisticsObj.nb_cancelled_orders = result.nb_cancelled_orders;
    statisticsObj.average_time = result.average_time;
    statisticsObj.orders_by_size = result.orders_by_size;
}

export const loadStatService = {
    dependencies: [],
    start () {
        loadStatistics();
        setInterval(loadStatistics, 60 * 1000 * 10);

        return {
            get stats() {
                return statisticsObj;
            },
        }
    }
}

registry.category("services").add("awesome_dashboard.statistics", loadStatService);
