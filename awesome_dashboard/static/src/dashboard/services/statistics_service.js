import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

// 10 secondes
const INTERVAL = 10000;

const statistics = reactive({
    average_quantity: 0,
    average_time: 0,
    nb_cancelled_orders: 0,
    nb_new_orders: 0,
    total_amount: 0,
    orders_by_size: {
        s: 0,
        m: 0,
        xl: 0,
    },
});

let refreshToken = 0;

const fetchStatistics = memoize(async () => rpc("/awesome_dashboard/statistics", {}));

async function loadStatistics() {
    const result = await fetchStatistics();
    Object.assign(statistics, result);
    Object.assign(statistics.orders_by_size, result.orders_by_size || {});
    return statistics;
}

export const statisticsService = {
    start() {
        loadStatistics();
        setInterval(() => {
            refreshToken += 1;
            loadStatistics();
        }, INTERVAL);
        return {
            statistics
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
