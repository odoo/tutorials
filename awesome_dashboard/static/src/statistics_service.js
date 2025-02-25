/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

export const loadStatistics = memoize(async () => {
    try {
        return await rpc("/awesome_dashboard/statistics");
    } catch (error) {
        console.error("Error fetching statistics:", error);
        return {};
    }
});

export const statisticsService = {
    dependencies: [],
    start() {
        return {
            loadStatistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
