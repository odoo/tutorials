import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

async function fetchStatistics() {
    return await rpc("/awesome_dashboard/statistics", {});
}

export const statisticsService = {
    dependencies: [],
    start() {
        const state = reactive({
            data: {
                new_orders: 0,
                total_amount: 0,
                average_quantity: 0,
                cancelled_orders: 0,
                avg_order_time: 0,
                orders_by_size: {
                    s: 0,
                    m: 0,
                    l: 0,
                },
            }
        });

        const loadStatistics = async () => {
            try {
                const result = await fetchStatistics();
                if (result) {
                    state.data.new_orders = result.nb_new_orders || 0;
                    state.data.total_amount = result.total_amount || 0;
                    state.data.average_quantity = result.average_quantity || 0;
                    state.data.cancelled_orders = result.nb_cancelled_orders || 0;
                    state.data.avg_order_time = result.average_time || 0;
                    state.data.orders_by_size = result.orders_by_size || {
                        s: 0,
                        m: 0,
                        l: 0,
                    };
                }
            } catch (error) {
                console.error("Error fetching statistics:", error);
            }
        };

        loadStatistics();

        // setInterval(() => {
        //     loadStatistics()
        // }, 1000);

        return {
            data: state.data, loadStatistics
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
