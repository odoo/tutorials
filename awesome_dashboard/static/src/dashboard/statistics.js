import { reactive } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export const statisticsService = {
    start() {
        let statistics = reactive({ value: false });
        
        async function loadStatistics() {
            const a = await rpc("/awesome_dashboard/statistics")
            Object.assign(statistics, a, {value: true})
        };

        setInterval(loadStatistics, 20000);

        loadStatistics();

        return statistics;
    }
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService)
