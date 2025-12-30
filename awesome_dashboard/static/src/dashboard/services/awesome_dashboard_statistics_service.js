import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

export const awesomeDashboardStatisticsService = {
    async: ["loadStatistics"],
    start() {
        const state = reactive({ stats: null})
        const fetchStats =  async ()=>{
            state.stats = await rpc("/awesome_dashboard/statistics")
        }
        fetchStats()
        const loadStatistics = () => setInterval(fetchStats , 10000);
        loadStatistics()
        return {
            state
        }
    },
}

registry.category("services").add("awesome_dashboard.statistics", awesomeDashboardStatisticsService);
