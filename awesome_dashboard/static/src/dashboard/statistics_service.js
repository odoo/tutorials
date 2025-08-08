import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
//import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";


export const statisticsService = {
    
    data: reactive({ stats: {} }),
    async fetchData(){
        const result = await rpc("/awesome_dashboard/statistics");

        Object.assign(this.data.stats,result);
    },

    start(){
        this.fetchData();
        setInterval(()=> this.fetchData(), 1000000);
        return { stats: this.data.stats }
    },
}

registry.category("services").add("statistics", statisticsService);

