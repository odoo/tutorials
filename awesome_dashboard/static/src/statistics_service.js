/** @odoo-module **/

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

export const httpService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const loadStatisticsMemoized = memoize(async () => await rpc("/awesome_dashboard/statistics"));
        return {
            loadStatistics: loadStatisticsMemoized,
        };
    },
};

registry.category("services").add("statisticService", httpService);
