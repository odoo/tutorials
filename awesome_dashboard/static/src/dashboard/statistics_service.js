import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
    start(env) {

        const response = reactive({
            average_quantity: 0,
            average_time: 0,
            nb_cancelled_orders: 0,
            nb_new_orders: 0,
            total_amount: 0,
            orders_by_size: {
                m: 0,
                s: 0,
                xl: 0
            },
        })

        const loadStatistics = (async () => {
            try {
                const result = await rpc("/awesome_dashboard/statistics");
                for (const key in result) {
                    response[key] = result[key];
                }
            } catch (error) {
                console.log("Error while fetching data from statistics!!")
            }
        });

        loadStatistics();

        const startInterval = () => {
            return setInterval(loadStatistics, 600 * 1000);
        }

        return {
            response,
            startInterval,
        };
    }
};

registry.category("services").add("statisticsService", statisticsService);
