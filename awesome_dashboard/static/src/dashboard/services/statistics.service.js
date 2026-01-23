import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const fetchInterval = 3000;

async function fetchStatistics(stats) {
    const result = await rpc("/awesome_dashboard/statistics");

    for(let entry of Object.entries(result)) {
        if(stats[entry[0]] !== undefined) stats[entry[0]] = entry[1];
    }
}

export const statisticsService = {
    start() {
        let stats = reactive({average_quantity: 0, average_time: 0, nb_cancelled_orders: 0, nb_new_orders: 0, total_amount: 0, orders_by_size: {}});

        fetchStatistics(stats)
        setInterval(() => fetchStatistics(stats), fetchInterval);

        return { 
            loadStatistics() {
                return stats;
            }
        }
    }
}

registry.category("services").add("statistics", statisticsService);
