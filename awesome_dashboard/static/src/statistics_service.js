/** @odoo-module **/

import { memoize } from "@web/core/utils/functions";
import { registry } from "@web/core/registry";

export const statistics = {
    dependencies: ['rpc'],
    start(env, { rpc }) {
        return {
            loadStatistics: memoize(() => {
                return rpc("/awesome_dashboard/statistics")
            })
        }
    }
}

registry.category("services").add("statistics", statistics)

