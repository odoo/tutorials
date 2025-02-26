import {registry} from '@web/core/registry';
import {rpc} from '@web/core/network/rpc';
import { reactive } from "@odoo/owl";

const statistics = reactive({stats:{}})

async function fetchStatistics(){
    console.log("Fetching data from server!!")
    const result=await rpc('/awesome_dashboard/statistics',{});
    // console.log(result)
    statistics.stats=result
    return statistics.stats
}

const loadStatistics = fetchStatistics;


export const statisticsService = {
    dependencies:[],
    start(){
        
        setInterval(loadStatistics,5000)
        return {loadStatistics}
    }
}

registry.category("services").add("awesome_dashboard.statistics",statisticsService)
