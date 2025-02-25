import {registry} from '@web/core/registry';
import {rpc} from '@web/core/network/rpc';
import {memoize} from '@web/core/utils/functions';
import { reactive } from "@odoo/owl";
const statistics = reactive({stats:{}})
async function fetchStatistics(){
    console.log("Fetching data from server!!")
    const result=await rpc('/awesome_dashboard/statistics',{});
    Object.assign(statistics.stats,result);
}

//const loadStatistics = memoize(fetchStatistics);


export const statisticsService = {
    dependencies:[],
    start(){
        fetchStatistics();
        setInterval(fetchStatistics,100000)
        return {stats:statistics.stats}
    }
}

registry.category("services").add("awesome_dashboard.statistics",statisticsService)
