import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";
//import { memoize } from "@web/core/utils/functions";

//const loadStatistics = memoize(
//    () => rpc("/awesome_dashboard/statistics"));

const statistics = reactive({});

async function loadStatistics(){
    try{
        const result = await rpc("/awesome_dashboard/statistics");

        Object.assign(statistics,result);
    } catch(error){
        console.error("failed to load dashboard statistics ",error);

    }
}

export const statisticsService = {
    start(){
       // return {loadStatistics };
       loadStatistics();

       setInterval(loadStatistics,10000);

       return statistics;
    }
};

registry.category("services").add("awesome_dashboard.statistics",statisticsService);
