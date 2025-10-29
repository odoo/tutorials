/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start() {
        const statistics = reactive({});

        async function loadStatistics(){
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics,data);
        }

        loadStatistics();
        setInterval(loadStatistics, 10*60*1000);

        return {
            statistics,
        };
    },
};

// Register the service
registry.category("services").add("awesome_dashboard.statistics", statisticsService);