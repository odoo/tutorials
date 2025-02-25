import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";


const statisticsService = {
    start() {
        const statistics = reactive({ isReady: false });
        async function loadData() {
            try {
                const updates = await rpc("/awesome_dashboard/statistics");
                statistics.averageQuantity = updates.average_quantity;
                statistics.averageTime = updates.average_time;
                statistics.nbCancelledOrders = updates.nb_cancelled_orders;
                statistics.nbNewOrders = updates.nb_new_orders;
                statistics.totalAmount = updates.total_amount;
                statistics.ordersBySize = updates.orders_by_size;
                statistics.isReady = true;
            } catch (error) {
                console.error("Failed to load statistics:", error);
            }
        }
        setInterval(loadData, 10 * 60 * 1000);
        loadData();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
