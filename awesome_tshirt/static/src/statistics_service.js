/** @odoo-module */

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

export const tshirtStatisticsService = {
    dependencies: ["rpc"],
    async start(env, { rpc }) {
        return {
            get: memoize(async function () {
                return await rpc("/awesome_tshirt/statistics");
            })
        };
    },
};

registry.category("services").add("tshirtStatisticsService", tshirtStatisticsService);
