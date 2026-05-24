import { registry } from "@web/core/registry"
// import {memoize} from "@web/core/utils/functions"
import { rpc } from "@web/core/network/rpc"
import { reactive } from "@odoo/owl"

const statisticService = {
    start() {
        const statistics = reactive({ isReady: false })

        async function loadData() {
            const update = await rpc("/awesome_dashboard/statistics");
            Object.assign(statistics, update, {
                isReady: true
            })
        }

        setInterval(loadData, 60 * 60)
        loadData();

        return statistics
    }
}

registry.category("services").add("awesome_dashboard.statistics", statisticService)
