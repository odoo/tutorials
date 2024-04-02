/** @odoo-module **/

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

export const Statistics = {
    
    dependencies: ["rpc"],
    async: ["loadStatistics"],
    start(env, { rpc }) {
        return {
            loadStatistics: memoize(() => rpc("/awesome_dashboard/statistics"))
        }
    }
};

registry.category("services").add("awesome_dashboard.statistics", Statistics);
