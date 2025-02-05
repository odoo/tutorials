/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export const statisticsService = {
    async start() {
        const statistics = reactive({ dashboard_items: {} });
        const fetchStatistics = async () => {
            const newData = await rpc("/awesome_dashboard/statistics", {});
            Object.assign(statistics.dashboard_items, newData);
            
        };
        await fetchStatistics();
        const intervalId = setInterval(fetchStatistics, 10000);
        return {
            statistics,
            stop: () => clearInterval(intervalId),
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
