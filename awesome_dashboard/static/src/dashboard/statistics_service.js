/** @odoo-module **/

import { registry } from "@web/core/registry";

export const statisticsService = {
    dependencies: ["rpc"],

    start(env, {rpc}) {
        let obj2 = rpc("/awesome_dashboard/statistics");
        setInterval(async () => {
            obj2 = rpc("/awesome_dashboard/statistics");
        }, 3000);
        return {
            loadStatistics : () => obj2,
        };
    },
};

registry.category("services").add("statistics_service", statisticsService);
