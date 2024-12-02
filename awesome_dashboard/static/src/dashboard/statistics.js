import {rpc} from "@web/core/network/rpc";
import {registry} from "@web/core/registry";
import {reactive, useState} from "@odoo/owl";

export const store = reactive({
    average_quantity: 0,
    average_time: 0,
    nb_cancelled_orders: 0,
    nb_new_orders: 0,
    orders_by_size: {},
    total_amount: 0
});

export async function loadData() {
    const result = await rpc("/awesome_dashboard/statistics", {});

    store.average_quantity = result.average_quantity
    store.average_time = result.average_time
    store.nb_cancelled_orders = result.nb_cancelled_orders
    store.nb_new_orders = result.nb_new_orders
    store.orders_by_size = result.orders_by_size
    store.total_amount = result.total_amount
}

export function useStatistics() {
    return useState(store);
}

export const statisticsService = {
    start() {
        loadData().then(() => {
        });
        setInterval(loadData, 10 * 1000)

        return {useStatistics}
    }
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService);