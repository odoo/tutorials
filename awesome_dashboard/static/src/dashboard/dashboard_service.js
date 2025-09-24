import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const dashboardService = {
    start() {
        let stats = reactive({
            average_quantity: 0, 
            average_time: 0, 
            nb_cancelled_orders: 0,
            nb_new_orders: 0,
            orders_by_size: {},
            total_amount: 0 
        });
        async function loadData() {
            const newStats = await rpc("/awesome_dashboard/statistics");
            Object.keys(newStats).forEach((k) => stats[k] = newStats[k])
        }
        setInterval(loadData, 2*1000);
        loadData();

        return stats;
    },
};


registry.category("services").add("awesome_dashboard.statistics", dashboardService);
