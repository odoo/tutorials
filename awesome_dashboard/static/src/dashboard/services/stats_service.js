import { registry } from "@web/core/registry"
import { reactive } from "@odoo/owl"
import { rpc } from "@web/core/network/rpc"

const STATS_REFRESH_TIME = 10000

const statsService = {
    start(){
        const stats = reactive({ isReady: false })

        async function fetchStats() {
            const latestStats = await rpc("/awesome_dashboard/statistics")
            Object.assign(stats,  { isReady: true, ...latestStats })
        }

        fetchStats()
        setInterval(fetchStats, STATS_REFRESH_TIME)

        return stats
    }
}

registry.category("services").add("awesome_dashboard.statistics", statsService)
