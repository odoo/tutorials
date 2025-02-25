import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

const statisticsService = {
    start() {
        const statistics = reactive({
            nb_new_orders: 0,
            total_amount: 0,
            average_quantity: 0,
            nb_cancelled_orders: 0,
            average_time: 0,
            orders_by_size: {},
            isReady: false,
        });

        async function loadData() {
            try {
                const data = await rpc("/awesome_dashboard/statistics");
                Object.assign(statistics, data, { isReady: true });
            } catch (error) {
                console.error("Failed to fetch dashboard statistics:", error);
            }
        }

        setInterval(loadData, 1000);
        loadData();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
