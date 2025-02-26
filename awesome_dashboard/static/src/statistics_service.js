/** @odoo-module **/

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { rpc } from "@web/core/network/rpc";

const StatisticsService = {
    async: ["loadData"],
    start(){
        return {
            loadData: memoize(()=> rpc("/awesome_dashboard/statistics"))
        }
    }
}
registry.category("services").add("awesome_dashboard.statistics", StatisticsService);
