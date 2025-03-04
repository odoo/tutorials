/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    start(){
        const statistics = reactive({ isReady: false });
        async function loadStatistics(){
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, updates, { isReady: true});
        }

        setInterval(loadStatistics, 60*1000);
        loadStatistics();
        return statistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
