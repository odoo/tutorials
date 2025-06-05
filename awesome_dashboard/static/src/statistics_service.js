/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

const statisticsService = {
    start() {
        const loadStatistics = memoize(async () => {
            console.log("Loading statistics from server...");
            const data = await rpc("/awesome_dashboard/statistics");
            console.log("Statistics loaded:", data);
            return data;
        });

        return {
            loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);