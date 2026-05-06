import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const StatisticsService = {
    start(env){
        const stats = reactive({data: {}})
        async function loadStatistics(){
            const result = await rpc("/awesome_dashboard/statistics")
            Object.assign(stats.data, result)
        }
        loadStatistics()
        setInterval(loadStatistics, 600000)
        return stats;
    }
}

registry.category("services").add("awesome_dashboard.statistics_service", StatisticsService)
