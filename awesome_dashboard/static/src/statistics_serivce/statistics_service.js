/** @odoo-module **/

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions"

export const statisticsService = {
    dependencies: ["rpc"],
    start(env, { rpc }){
        const  memoizedLoadStatistics = memoize(() => rpc('/awesome_dashboard/statistics'))
        return {
            loadStatistics(){
                return memoizedLoadStatistics()
            }
        }
    }
}

registry.category("services").add("statisticsService", statisticsService)


