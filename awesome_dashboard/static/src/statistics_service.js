import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statisticsService = {
    start() {
        const statistics = reactive({
            newOrders: 0,
            totalAmount: 0,
            avgQuantity: 0,
            cancelledOrders: 0,
            avgTime: 0,
            sizedata:{}
        });
        const loadStatistics = async () => {
            try {
                const result = await rpc("/awesome_dashboard/statistics", {});
                console.log("Fetched statistics:", result);

                statistics.newOrders = result.nb_new_orders || 0;
                statistics.totalAmount = result.total_amount || 0;
                statistics.avgQuantity = result.average_quantity || 0;
                statistics.cancelledOrders = result.nb_cancelled_orders || 0;
                statistics.avgTime = result.average_time || 0;
                statistics.sizedata = result.orders_by_size || 0;

            } catch (error) {
                console.error("Error loading statistics:", error);
            }
        };
        loadStatistics();
        setInterval(loadStatistics, 10000);
        return { statistics };
    },
};
registry.category("services").add("awesome_dashboard.statistics", statisticsService);
