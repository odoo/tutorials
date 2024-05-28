/** @odoo-module **/

import { memoize } from "@web/core/utils/functions";
import { registry } from "@web/core/registry";

const statisticsService = {
    dependencies: ["rpc"],
    async: ["fetchStatistics"],
    start(env, { rpc }) {
        return {
            fetchStatistics: memoize(() => rpc("/awesome_dashboard/statistics"))
        };
    }
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
