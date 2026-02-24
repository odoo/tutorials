/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

export const loadStatistics = memoize(async function () {
    return await rpc("/awesome_dashboard/statistics", {});
});