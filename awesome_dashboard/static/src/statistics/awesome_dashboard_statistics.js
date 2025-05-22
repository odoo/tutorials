/** @odoo-module **/

import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

export const awesomeDashboardStatisticsService = {
    start() {
        const stats = reactive({ data: null });

        // Get a new memoized function for fetching statistics
        const getMemoizeFetch = () => {
            return memoize(async () => {
                return await rpc("/awesome_dashboard/statistics");
            });
        };

        // Fetch statistics
        const fetchStatistics = async () => {
            const memoizedFetch = getMemoizeFetch();
            stats.data = await memoizedFetch();
        };

        // Setup interval
        fetchStatistics();
        setInterval(fetchStatistics, 600000);

        return stats;
    },
};
registry.category("services").add("awesome_dashboard_statistics", awesomeDashboardStatisticsService);
