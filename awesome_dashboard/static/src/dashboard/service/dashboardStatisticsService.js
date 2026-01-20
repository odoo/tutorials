import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const dashboardStatisticsService = { 

        start() {
        const stats = reactive({
            nb_new_orders: 0,
            total_amount: 0,
            average_quantity: 0,
            nb_cancelled_orders: 0,
            average_time: 0,
            orders_by_size: { m: 0, s: 0, xl: 0 }
        });
        async function fetchStatistics() {
            const result =   await rpc("/awesome_dashboard/statistics");
            if (result) {
            Object.assign(stats, result);
          }
        }

        fetchStatistics();

        setInterval(() => {
            fetchStatistics();
        }, 10601000);
        return {
            data : stats
        };
    },
    
}

registry.category("services").add("awesome_dashboard.statistics", dashboardStatisticsService);
