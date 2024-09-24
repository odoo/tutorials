/** @odoo-module **/

import {registry} from "@web/core/registry";
import {memoize} from "@web/core/utils/functions";


export async function loadStatistics(rpc) {
    return rpc("/awesome_dashboard/statistics");
}

export const statisticsService = {
    dependencies: ["rpc"],
    async: ["loadStatistics"],
    start(env, {rpc}) {
        return {
            loadStatistics: memoize(() => loadStatistics(rpc)),
        };
    }
}


registry.category("services").add("statistics_service", statisticsService);