/** @odoo-module **/

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

// Memoized loadStatistics: will fetch only once
// const loadStatistics = memoize(async () => {
//     return await rpc("/awesome_dashboard/statistics");
// });

export const statisticsService = {
    dependencies: [],
    async start() {
        const statistics = reactive({});

        const updateStatistics = async () => {
            const data = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, data);
        };

        await updateStatistics();
        setInterval(updateStatistics, 10000);

        return {
            statistics,
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);