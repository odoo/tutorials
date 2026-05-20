import {registry} from "@web/core/registry"
import {memoize} from "@web/core/utils/functions"
import {rpc} from "@web/core/network/rpc"

const statisticService = {
    start(){
        return {
            loadStatistics: memoize(()=> rpc("/awesome_dashboard/statistics")),
        }
    }
}

registry.category("service").add("awesome_dashboard.statistics", statisticService)
