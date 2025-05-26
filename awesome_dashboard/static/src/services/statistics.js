/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const statisticsService = {
    start() {
        const stats = reactive({});

        // Function to load and update the stats
        const loadStatistics = async () => {
            const result = await rpc("/awesome_dashboard/statistics", {});
            Object.assign(stats, result); // update the reactive object in place
        };

        // Initial load
        loadStatistics();

        // Auto-refresh every 10 seconds
        setInterval(loadStatistics, 10000);

        return {
            statistics: stats,       // export the reactive state
            reload: loadStatistics,  // optional manual reload
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
