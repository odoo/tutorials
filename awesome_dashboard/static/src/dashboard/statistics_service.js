/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

const statisticsService = {
    start() {
        const data = reactive({
            average_quantity: 0,
            average_time: 0,
            nb_cancelled_orders: 0,
            nb_new_orders: 0,
            orders_by_size: { m: 0, s: 0, xl: 0 },
            total_amount: 0,
        });

        async function loadData() {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(data, result);
        }

        setInterval(loadData, 10 * 60 * 1000);
        loadData();

        return data;
    },
};

registry.category("services").add("load_statistics", statisticsService);
