/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

const loadStatistics = async() => {
    const result = await rpc("/awesome_dashboard/statistics");
    return result;
}

export const loadStatService = {
    start () {
        return {
            loadStatistics: memoize(loadStatistics)
        }
    }
}

registry.category("services").add("awesome_dashboard.statistics", loadStatService);
