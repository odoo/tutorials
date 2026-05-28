import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


const statisticsService = {
    start() {
        let stats = reactive({})

        async function getStats() {
            let updates = await rpc("/awesome_dashboard/statistics");
            Object.assign(stats, updates);
        }

        getStats()
        setInterval(getStats, 10*1000)

        return stats
    }
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
