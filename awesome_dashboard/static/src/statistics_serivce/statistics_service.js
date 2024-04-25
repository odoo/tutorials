/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl"

export const statisticsService = {
    dependencies: ["rpc"],
    start(env, { rpc }){
        const statistics = reactive({isReady: false})
        async function loadData(){
            const updates = await rpc('/awesome_dashboard/statistics')
            Object.assign(statistics, updates, {isReady: true})
        }
        setInterval(loadData, 10 * 1000)

        loadData()
        
        return statistics

    }
}

registry.category("services").add("statisticsService", statisticsService)


