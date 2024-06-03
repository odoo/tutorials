/** @odoo-module **/

import { memoize } from "@web/core/utils/functions";
import { registry } from "@web/core/registry";

const statisticsService = {
    dependencies: ["rpc"],
    async: ["loadStatistics"],
    start(env, { rpc }) {
        return {loadStatistics: memoize(() => rpc("/awesome_dashboard/statistics"))};
    },
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
