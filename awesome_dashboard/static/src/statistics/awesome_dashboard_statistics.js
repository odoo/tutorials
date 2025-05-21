/** @odoo-module **/

import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";

const getStatistics = memoize(async () => await rpc("/awesome_dashboard/statistics"));

export const awesomeDashboardStatisticsService = {
    start() {
        return { getStatistics };
    },
};
registry.category("services").add("awesome_dashboard_statistics", awesomeDashboardStatisticsService);
