/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start() {
        const statistics = reactive({});
        
        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, result);
        }
        
        loadStatistics();

        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
