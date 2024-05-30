/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

export const statisticsService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const statistics = reactive({ isReady: false });

        async function loadStatistics(){
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true });
        };

        setInterval(loadStatistics, 5000);
        
        loadStatistics()

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);