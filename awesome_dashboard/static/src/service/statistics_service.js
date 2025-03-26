import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


export const statisticsService = {

    start() {
        const stats = reactive({
            data: {
                nb_new_orders: 0,
                total_amount: 0,
                average_quantity: 0,
                nb_cancelled_orders: 0,
                average_time: 0,
                orders_by_size: { m: 0, s: 0, xl: 0 },
            },
        });

        const loadStatistics = async () => {
            const result = await rpc("/awesome_dashboard/statistics", {});
            if (result) {
                Object.assign(stats.data, result);
            }
        };

        // Initial load
        loadStatistics();

        // Periodic refresh every 10 seconds
        setInterval(() => {
            loadStatistics();
        }, 10000);

        return { data: stats.data, loadStatistics };
    },
};
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
