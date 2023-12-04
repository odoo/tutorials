/** @odoo-module **/

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

export const statisticsService = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const loadStatistics = async () => {
            const statistics = await rpc("/awesome_tshirt/statistics");
            return statistics;
        }
        return {
            loadStatistics: memoize(loadStatistics)
        }
    },
};
registry.category("services").add("statisticsService", statisticsService);
