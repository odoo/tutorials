import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions";

// Cache statistics
/* 
const statisticsService = { 
    dependencies: [],
    start() {
        return {
            loadStatistics: memoize(async function () {
                return await rpc("/awesome_dashboard/statistics");
            }),
        };
    },
};
 */

// real life update
const statisticsService = {
    data: reactive({ stats: {} }),

    async fetchData(){
        const result = await rpc("/awesome_dashboard/statistics");
        
        Object.assign(this.data.stats,result);
    },

    start(){
        this.fetchData();
        setInterval(()=> this.fetchData(), 10000);
        return { stats: this.data.stats }
    },
}

registry.category("services").add("statistics", statisticsService);
