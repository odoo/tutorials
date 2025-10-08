import { reactive } from "@odoo/owl"
import { registry } from "@web/core/registry"
import { rpc } from "@web/core/network/rpc"

const statisticsService = {

    start() {
        const statistics = reactive({ isReady: false });
        async function handleData() {
            const result = await rpc("/awesome_dashboard/statistics")
            Object.assign(statistics, result, { isReady: true })
        }

        setInterval(handleData, 10 * 60 * 1000)
        handleData()

        return statistics;
    }
}

registry.category("services").add("awesome_dashboard.statistics", statisticsService)
