/** @odoo-module **/

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";

// Memoized loadStatistics: will fetch only once
const loadStatistics = memoize(async () => {
    return await rpc("/awesome_dashboard/statistics");
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
