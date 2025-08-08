import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


export const statisticsService = {
    start() {
        const statistics = reactive({isReady:false})

        async function loadStatistics() {

            const statisticsloaded = await rpc('/awesome_dashboard/statistics');
            Object.assign(statistics, statisticsloaded, {isReady: true})
            
        }
        
        setInterval(loadStatistics, 10000)
        
        return statistics;
    },
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService);