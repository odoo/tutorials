/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statistics = {
    start() {
        const stats = reactive({});
        const loadStatistics = async () => {
            try {
                const data = await rpc("/awesome_dashboard/statistics");
                console.log('Statistics loaded:', data);
                Object.assign(stats, data);
            } catch (error) {
                console.error('Error loading statistics:', error);
            }
        };
        loadStatistics();
        setInterval(loadStatistics, 60000);

        return {
            stats,
            loadStatistics};
    },
};

registry.category("services").add("awesome_dashboard.statistics", statistics);
