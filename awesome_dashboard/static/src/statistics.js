import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";


export async function loadStatistics(){
    const statistics = await rpc("/awesome_dashboard/statistics");
    //console.log(statistics);
    //return statistics;

    const test = memoize(function loadStatistics(){
        return statistics;
    });
    return test;

    /*const statistics = memoize(async function loadStatistics(){
        return await rpc("/awesome_dashboard/statistics");
    });

    return statistics;*/

}

export const statisticsService = {
    start() {
        return { loadStatistics };
    }
};

registry.category("services").add("statistics", statisticsService);
