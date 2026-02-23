import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statisticsService = {
    start() {
        const statistics = reactive({});

        async function loadStatistics() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates);
        }

        setInterval(loadStatistics, 10000);
        loadStatistics();

        return {
            statistics
        };
    }
};

registry.category("services").add("statistics", statisticsService);