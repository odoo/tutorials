/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";


const statistics = reactive({ data: null }); 

//Memoize
// const loadStatistics = memoize(async () => {
//     statistics.data =  await rpc("/awesome_dashboard/statistics", {})
// });

const loadStatistics = (async () => {
    statistics.data =  await rpc("/awesome_dashboard/statistics", {})
});

const statisticsService = {
    start(){
        loadStatistics()
        setInterval(loadStatistics, 10 * 1000);
        return { statistics } 
    }
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
