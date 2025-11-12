/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const awesomeDashboardStatisticsService = {
    start() {
        const loadStatistics = reactive({ isReady: false });
        async function loadData() {
            const updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(loadStatistics, updates, { isReady: true });
        }
        setInterval(loadData, 10*60*1000);
        loadData();
        return loadStatistics;
    },
};

registry.category("services").add("awesome_dashboard.statistics",awesomeDashboardStatisticsService);
